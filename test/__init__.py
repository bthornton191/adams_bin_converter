import os
from pathlib import Path
TEST_GOOD_CMD_1 = Path("C:/Program Files/MSC.Software/Adams/2020_1_748966/common/mdi.bat")
TEST_GOOD_CMD_2 = Path("C:/Program Files/MSC.Software/Adams/2019_2/common/mdi.bat")
TEST_GOOD_CMD_3 = Path("C:/Program Files/MSC.Software/Adams/2018_1/common/mdi.bat")
TEST_BAD_CMD = Path("C:/Program Files/MSC.Software/Adams/drill_postprocess.bat")
TEST_FILE_DIR = Path('test/files')
CONVERTER_CMD = Path('adams_bin_converter.py')

def clear_test_file_dir():
    
    for ext in ['cmd', 'log', 'py', 'bak', 'loq']:
        for cmd_file in TEST_FILE_DIR.glob(f'*.{ext}'):
            try:
                os.remove(cmd_file)
            except PermissionError:
                pass
    
