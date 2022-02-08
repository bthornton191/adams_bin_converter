# Adams Bin Converter

## New Features in v0.0.2
1. Added feature to recognize version in bin file.
2. Added feature to get multiple models out of a single .bin file

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
> Note: The newly created command file will be named after the model contained by the .bin file. 
> If the .bin file contains **multiple models** then the program will create muiltiple .cmd files.

### Letting the program find the path to the correct mdi.bat file based on the .bin file version \***NEW**\*
In order for this to work you must tell the script where all of your adams installations are 
located (e.g. C:/Program Files/MSC.Software/Adams). Adams will look for this location in the 
following order:
1. The `ADAMS_INSTALL_DIR` variable at the top of the module
2. A `ADAMS_INSTALL_DIR` environment variable

### Specifying the path to the mdi.bat file as an argument
There are several options for telling **adams_bin_converter.py** which installation of adams to use. 
The simplest is supplying the path as an argument to the command line interface. You can do this 
using the `--p` flag.
```bash
> python adams_bin_converter.py --p "C:\Program Files\MSC.Software\Adams\2021_2_2_826892\common\mdi.bat" file_1.bin
```
> Note: The `--p` flag overrides the above method. However, if a valid mdi.bat file is not provided, 
> the program will revert to determining the correct mdi.bat file based on the version of the .bin
> files.

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
# NOTE: You must use forward slashes (/) or double back slashes (\\) in the file path above.
```
> Note: The program will attempt all methods above before trying this method

### Specifying the path to the mdi.bat file using an environment variable
You can permentantly specify the path to the mdi.bat file by setting the `ADAMS_LAUNCH_COMMAND` 
environment variable using the following syntax:
```bash
> setx ADAMS_LAUNCH_COMMAND "C:\Program Files\MSC.Software\Adams\2021_2_2_826892\common\mdi.bat"
```
> Note: The program will attempt all methods above before trying this method

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
