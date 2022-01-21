# Adams Bin Converter

## Installation

### Option 1: Download the standalone script

1. Download the code base as a zip file using the green **Code** button above.
3. Extract **adams_bin_converter.py**


### Option 2: Install with pip
```
> pip install git+https://github.com/bthornton191/adams_bin_converter
```
## Command Line Usage
Convert a **.bin** file to a **.cmd** file using the following command line syntax:
```bash
> python adams_bin_converter.py file_1.bin
```
You may convert multiple **.bin** files like so:
```bash
> python adams_bin_converter.py file_1.bin file_2.bin
```
Use the following syntax **if you installed via pip**.
```bash
> python -m adams_bin_converter file1.bin
```
### Specifying the path to the mdi.bat file as an argument
There are several options for telling **adams_bin_converter.py** which installation of adams to use. 
The simplest is supplying the path as an argument to the command line interface. You can do this 
using the `--p` flag.
```bash
> python adams_bin_converter.py --p "C:\Program Files\MSC.Software\Adams\2021_2_2_826892\common\mdi.bat" file_1.bin
```
### Specifying the path to the mdi.bat file using an environment variable
You can permentantly specify the path to the mdi.bat file by setting the `ADAMS_LAUNCH_COMMAND` 
environment variable using the following syntax:
```bash
> setx ADAMS_LAUNCH_COMMAND "C:\Program Files\MSC.Software\Adams\2021_2_2_826892\common\mdi.bat"
```
### Specifying the path to the mdi.bat file using a module variable
You can also permenantly specify the path to the mdi.bat file by setting the `ADAMS_LAUNCH_COMMAND` 
variable in the top of the **adams_bin_converter.py**. The head of **adams_bin_converter.py** is shown below.

```python
import os
import argparse
from pathlib import Path
from random import random
import subprocess
import platform
from time import sleep

SCRIPT_NAME = '_bin_converter.py'
ADAMS_LAUNCH_COMMAND = Path('<adams_install_dir>/<version_dir>/common/mdi.bat')

...
```
To permentantly set the path to the mdi.bat file you would change the line
```python
ADAMS_LAUNCH_COMMAND = Path('<adams_install_dir>/<version_dir>/common/mdi.bat')
```
to
```python
ADAMS_LAUNCH_COMMAND = Path('C:/Program Files/MSC.Software/Adams/2021_2_2_826892/common/mdi.bat')
```
> Note: You must use forward slashes (`/`) or double back slashes (`\\`) in the file path above.

## API Usage
You can accomplish the same tasks from within a python script as follows:
```python
from adams_bin_converter import convert

convert('path/bin_files/file_1.bin')
```
You can use the same methods described above to specify the path to the mdi.bat file. For instance
you can pass the path as an argument to the `convert` function like so:
```python
convert(
    bin_file = 'path/bin_files/file_1.bin',
    adams_launch_command = 'C:/Program Files/MSC.Software/Adams/2021_2_2_826892/common/mdi.bat'
)
```
