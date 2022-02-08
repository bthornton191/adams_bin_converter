from __future__ import annotations
#!python
import os
import argparse
from pathlib import Path
from random import random
import subprocess
import platform
from time import sleep
import re
from dataclasses import dataclass, field
from typing import Tuple, Union, List
import unicodedata

SCRIPT_NAME = '_bin_converter.py'
ADAMS_LAUNCH_COMMAND = Path('<adams_install_dir>/<version_dir>/common/mdi.bat')
ADAMS_INSTALL_DIR = Path('C:/Program Files/MSC.Software/Adams')

ERR_TEXT = (
    'You must (a) pass the full path to mdi.bat to the adams_launch_command'
    'argument, (b) set the ADAMS_LAUNCH_COMMAND environment variable ' 
    'to the full path to your mdi.bat file, or (c), set the'
    'ADAMS_LAUNCH_COMMAND variable at the top of this module to the full'
    'path to your mdi.bat file. The mdi.bat file located at '
    '<adams_install_dir>/<version_dir>/common/mdi.bat. (d) Set the '
    'ADAMS_INSTALL_DIR environment variable equal to the full path to '
    'the directory that contains all versions of adams (i.e. '
    'C:\Program Files\MSC.Software\Adams), or (e) set the '
    'ADAMS_INSTALL_DIR variable at the top of this module to the full '
    'path to the directory that contains all versions of adams (i.e. '
    'C:\Program Files\MSC.Software\Adams)'
)


@dataclass
class Version():
    year: int
    release: int
    update: int = 0
    build: int = 0
    other: Tuple[str] = field(default_factory=tuple)

    def __ge__(self, other: Version):
        if self == other:
            return True
        else:
            return self.__gt__(self, other)

    def __gt__(self, other: Version):
        chronological = sorted([self, other], key=lambda v: (v.year, v.release, v.update, v.build))
        return chronological.index(self) == 1

    def __le__(self, other: Version):
        if self == other:
            return True
        else:
            return self.__lt__(self, other)

    def __lt__(self, other: Version):
        chronological = sorted([self, other], key=lambda v: (v.year, v.release, v.update, v.build))
        return chronological.index(self) == 0
    
    def __hash__(self) -> int:
        return hash(tuple(self.__dict__.values()))

    def get_closest_version(self, vers: List[Version], _comp='year'):
        """Gets the closest version to `:arg:ver` in `:arg:vers`. If a matching year does not exist, 
        will take the next highest year. An exception is raised if a higher year does not exist. For 
        release, update and build, it also looks for the next highest if a match does not exist. Unlike,
        year, it will allow a lower release, update, or build if a higher one does not exist.

        Parameters
        ----------
        ver : Version
            A version to find a match for
        vers : List[Version]
            A list of versions to search

        Returns
        -------
        Version
            The closest match to `:arg:ver` in `:arg:vers`

        Raises
        ------
        AdamsVersionError
            Raised if all the versions in `:arg:vers` are older than `:arg:ver`
        """
        vers = sorted(vers)
        # Get all with the same comp
        vers_with_same = list(filter(lambda v:getattr(v, _comp)==getattr(self, _comp), vers))

        # Check if there are any with the same comp
        if vers_with_same != []:
            # If there are any versions with the same comp, 
            # Check if there is exactly one        
            if len(vers_with_same) == 1:
                # If there is exactly one
                return vers_with_same[0]

            else:
                comps = list(self.__dict__.keys())
                next_comp = comps[comps.index(_comp)+1]
                return self.get_closest_version(vers_with_same, next_comp)

        else:
            # If no versions with the same comp exist, get all higher versions
            higher_vers = [v for v in vers if v > self]
            
            if higher_vers != []:
                # If there are versions higher than the target, take the first that is higher
                return higher_vers[0]
            
            elif _comp != 'year':
                # If there are no versions higher than the target, and we *ARE NOT* comparing year, 
                # take the next highest one
                return vers[-1]
            
            elif  _comp == 'year':
                # If there are no versions higher than the target, and we *ARE* comparing year,
                # raise an error
                raise AdamsVersionError(f'No acceptable versions exist for {self}!')

    @classmethod
    def from_install_dir(cls, install_dir: Union[Path, str]):
        install_dir = Path(install_dir)
        comps = [comp for comp in re.split('[_\\.]', install_dir.stem)]

        year, release, update, build, other = cls._decompose(comps)
        return cls(year, release, update, build, other)
    
    @classmethod
    def from_bin_file(cls, bin_file: Union[Path, str]):
        with Path(bin_file).open('rb') as fid:
            line = fid.readline()

        text = ''.join([ch for ch in line.decode('ascii', errors='ignore') if unicodedata.category(ch)[0]!="C"])
        comps = re.findall('version\\s([\\d\\.]*)', text, flags=re.IGNORECASE)[0].split('.')
        
        year, release, update, build, other = cls._decompose(comps)
        return cls(year, release, update, build, other)

    @staticmethod
    def _decompose(comps: List[str]):
        year = int(comps[0])
        
        # If there is an release
        if len(comps) > 1 and len(comps[1]) <= 2:
            release = int(comps[1])
        else:
            release = 0
        
        # If there is an update
        if len(comps) > 2 and len(comps[2]) <= 2:
            update = int(comps[2])
        else:
            update = 0

        # If there is a build number at the and it would be longer than 2 digits
        if len(comps[-1]) > 4:
            build = int(comps[-1])
        else:
            build = 0

        # Store any other components in a list
        if len(comps) > 3:
            other = (int(comp) for comp in comps[3:] if len(comp) <= 2)
        else:
            other = ()
        
        return year, release, update, build, other

    @staticmethod
    def get_installed_version_dirs(adams_install_dir: Path):
        return [d for d in Path(adams_install_dir).glob('*/') if re.fullmatch('\\d{4}(_\\d+)+', d.stem)]
    
    @classmethod
    def get_installed_versions(cls, adams_install_dir: Union[Path, str]) -> Path:
        adams_install_dir = Path(adams_install_dir)
        return {cls.from_install_dir(d): d for d in cls.get_installed_version_dirs(adams_install_dir)}

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

        # Loop over all the models in the databas
        fid.write(f'for mod in Adams.Models.values():\n')

        # Write the command file
        fid.write(f'   Adams.write_command_file(file_name=f"{{mod.name}}.cmd", model=mod)\n')

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

def _get_adams_launch_command(adams_launch_command=None, bin_file: Path=None, silent=False):
    
    def _check(path):
        """Returns True if the path exists and is an mdi.bat file"""
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
    
    elif bin_file is not None:
        bin_ver = Version.from_bin_file(bin_file)
        install_dir = get_install_dir()
        vers = Version.get_installed_versions(install_dir)
        
        installed_ver = bin_ver.get_closest_version(list(vers.keys()))
        cmd = vers[installed_ver] / 'common/mdi.bat'

        if silent is False:
            print(f'Using {cmd} as the adams launch command. This path is based on the version in '
                f'{Path(bin_file).name}.')

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
        raise EnvironmentError(ERR_TEXT)

    return Path(cmd)


def get_install_dir():
    
    if Path(ADAMS_INSTALL_DIR).exists():
        install_dir = ADAMS_INSTALL_DIR

    elif 'ADAMS_INSTALL_DIR' in os.environ:
        install_dir = os.environ['ADAMS_INSTALL_DIR']
    
    else:
        raise EnvironmentError(ERR_TEXT)

    return install_dir


def convert(bin_file, adams_launch_command=None, get_version_from_bin=False):
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

    adams_launch_command = _get_adams_launch_command(
        adams_launch_command,
        bin_file=bin_file if get_version_from_bin is True else None,
    )   

    bin_file = Path(bin_file)
    complete_code = str(random())
    
    cmd_file = _write_script(bin_file, complete_code)
    _run_script(bin_file.parent, adams_launch_command, complete_code)
    _remove_script(bin_file.parent)

    return cmd_file

class AdamsVersionError(Exception):
    pass

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

    for bin_file in bin_files:
        
        # adams_launch_command = _get_adams_launch_command(
        #     adams_launch_command = args.adams_launch_command,
        #     bin_file = Path(bin_file) if args.adams_launch_command is None else None,
        #     silent = True,
        # )

        convert(
            bin_file,
            adams_launch_command=args.adams_launch_command,
            get_version_from_bin=True if args.adams_launch_command is None else False,
        )
