#!python
import os
import argparse
from pathlib import Path
from random import random
import subprocess
import platform
from time import sleep

SCRIPT_NAME = '_bin_converter.py'
ADAMS_LAUNCH_COMMAND = Path('<adams_install_dir>/<version_dir>/common/mdi.bat')

def _write_script(bin_file, complete_code=''):
    """Writes an Adams View CMD script that opens an Adams View Binary (.bin) file 
    named `:arg:bin_file` and saves it as an Adams View Command (.cmd) file of the same base name.

    Parameters
    ----------
    bin_file : str or Path
        The filename of the Adams View Binary (.bin) file to be converted. 
    complete_code : str, optional
        A string to write to the end of the script to indicate completion, by default ''

    Returns
    -------
    Path
        Filename of the Adams View Command (.cmd) file that will be created by the script.

    """
    bin_file = Path(bin_file)
    cmd_file = bin_file.with_suffix('.cmd')

    with open(bin_file.parent / SCRIPT_NAME, 'w') as fid:

        # Echo the starting message
        fid.write(f'print("! -- SCRIPT STARTING {complete_code} --")\n')

        fid.write('import Adams\n')
        
        # Load the binary file
        fid.write(f'Adams.read_binary_file("{bin_file.name}")\n')

        # Write the command file
        fid.write(f'Adams.write_command_file(file_name = "{cmd_file.name}", model = Adams.getCurrentModel())\n')

        # Echo the completion message
        fid.write(f'print("! -- SCRIPT COMPLETE {complete_code} --")\n')

    return cmd_file

def _check_if_complete(sim_dir, complete_code = ''):
    """Checks the aview.log file in `:arg:cwd` to see if it has written the completion message.

    Parameters
    ----------
    cwd : str or Path
        Working directory
    complete_code : str, optional
        A string to write to the end of the script to indicate completion, by default ''

    Returns
    -------
    bool
        True if the completion message is found in the log file

    """
    log_file = Path(sim_dir) / 'aview.log'
    
    # Check if the log file exists
    if not log_file.exists():
        # If the log file does not exist yet
        result = False

    else:
        # If the log file does exist, examine the contents for completion
        with open(Path(sim_dir) / 'aview.log', 'r') as fid:
            text = fid.read()

        if f'! -- SCRIPT COMPLETE {complete_code} --' in text:
            result = True
        
        elif '! Command file is exhausted,' in text and f'! -- SCRIPT STARTING {complete_code} --' in text:
            raise RuntimeError('The Adams View Script did not execute properly!')
        
        else:
            result = False
    
    return result
    
def _wait_for_completion(sim_dir, complete_code = ''):
    """Waits for the script running in `:arg:sim_dir` to complete.

    Parameters
    ----------
    sim_dir : str or Path
        Directory in which the script is running
    complete_code : str, optional
        A string to write to the end of the script to indicate completion, by default ''

    """
    while True:
        
        # Check if the script has completed
        if _check_if_complete(sim_dir, complete_code) is True:
            
            # If the script has completed, Retrun 
            return
        
        else:

            # If the script has *NOT* completed, wait before repeating
            sleep(0.5)

def _run_script(sim_dir, adams_cmd, complete_code=''):
    
    # Check if the platform is Windows or Unix
    if platform.system() == 'Windows':

        # If the platform is Windows
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen(
            f'"{adams_cmd}" aview ru-standard b {SCRIPT_NAME}',
            cwd=sim_dir,
            startupinfo=startupinfo
        )

    else:
        
        # If the platform is Unix
        subprocess.Popen(
            [adams_cmd, '-c', 'aview', 'ru-standard', 'b', SCRIPT_NAME, 'exit'],
            cwd=sim_dir
        )
    
    # Wait for the script to complete before continuing
    _wait_for_completion(sim_dir, complete_code)

def _remove_script(sim_dir):
    os.remove(Path(sim_dir) / SCRIPT_NAME)

def _get_adams_launch_command(adams_launch_command=None, silent=False):
    
    def _check(path):
        path = Path(path)

        try:
            result = path.exists() and path.name == 'mdi.bat'
        except OSError:
            result = False
        
        return result
    
    if adams_launch_command is not None and _check(adams_launch_command):
        cmd = adams_launch_command
        if silent is False:
            print(f'Using {cmd} as the adams launch command. This path was passed as an argument.')

    elif _check(ADAMS_LAUNCH_COMMAND):
        cmd = ADAMS_LAUNCH_COMMAND
        if silent is False:
            print(f'Using {cmd} as the adams launch command. This path was taken from the'
            'ADAMS_LAUNCH_COMMAND module variable.')
    
    elif 'ADAMS_LAUNCH_COMMAND' in os.environ and _check(os.environ['ADAMS_LAUNCH_COMMAND']):
        cmd = os.environ['ADAMS_LAUNCH_COMMAND']
        if silent is False:
            print(f'Using {cmd} as the adams launch command. This path was taken from the '
                'ADAMS_LAUNCH_COMMAND environment variable.')
    
    else:
        raise EnvironmentError('You must (a) pass the full path to mdi.bat to the adams_launch_command'
                                'argument, (b) set the ADAMS_LAUNCH_COMMAND environment variable ' 
                                'to the full path to your mdi.bat file, or (c), set the'
                                'ADAMS_LAUNCH_COMMAND variable at the top of this module to the full'
                                'path to your mdi.bat file. The mdi.bat file located at '
                                '<adams_install_dir>/<version_dir>/common/mdi.bat')

    return Path(cmd)

def convert(bin_file, adams_launch_command=None):
    """Converts the Adams View Binary (.bin) file located at `:arg:bin_file` to an Adams View 
    Command (.cmd) file of the same base name.

    Parameters
    ----------
    bin_file : str or Path
        Path to the Adams View Binary (.bin) file to be converted
    adams_launch_command : str or Path, optional
        Path to the mdi.bat file in the local Adams installation, by default None

    Returns
    -------
    Path
        Path to the Adams View Command (.cmd) file that was created.
        
    """
    adams_launch_command = _get_adams_launch_command(adams_launch_command)   

    bin_file = Path(bin_file)
    complete_code = str(random())
    
    cmd_file = _write_script(bin_file, complete_code)
    _run_script(bin_file.parent, adams_launch_command, complete_code)
    _remove_script(bin_file.parent)

    return cmd_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Converts an Adams View Binary (.bin) files to an Adams View Command (.cmd) files.'
    )

    parser.add_argument(
        'bin_files',
        metavar = 'bin_file',
        type = str,
        nargs = '+',
        help = 'Adams View Binary file(s) to be converted to Adams View Command file(s).'
    )

    parser.add_argument(
        '--p',
        type = str,
        default = None,
        required = False,
        metavar = 'adams_path',
        dest = 'adams_launch_command',
        help =  'The full path to the mdi.bat file. The mdi.bat file is located at '
                '<adams_install_dir>/<version_dir>/common/mdi.bat. If this parameter is omitted, '
                'the application will check if the ADAMS_LAUNCH_COMMAND module variable points '
                'to an existing mdi.bat file. If the ADAMS_LAUNCH_COMMAND module variable points '
                'to an existing mdi.bat file, the application will use this as the Adams path. '
                'Othersise, it will check if the ADAMS_LAUNCH_COMMAND enviroment variable is set '
                'to an existing mdi.bat file. If it does not, the application will exit with an '
                'error.'
    )

    args = parser.parse_args()
    bin_files = args.bin_files
    adams_launch_command = _get_adams_launch_command(args.adams_launch_command, silent=True)

    for bin_file in bin_files:
        convert(bin_file, adams_launch_command)
