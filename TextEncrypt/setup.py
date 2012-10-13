# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

includes = ['re','win32clipboard']
excludes = []
includefiles = ['des_X2.dll','img','imageformats','pywintypes32.dll']

#['Microsoft.VC90.CRT.manifest','msvcm90.dll','msvcr90.dll','msvcp90.dll']

setup(
        name = "simple_PyQt4",
        version = "0.1",
        description = "Sample cx_Freeze PyQt4 script",
        executables = [Executable("TextEncrypt.py", base = base, icon = "img\\TextEncrypt.ico")],
    options = {"build_exe": {"includes":includes,"excludes":excludes, "include_files": includefiles}},
)

