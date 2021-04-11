import sys
from cx_Freeze import setup, Executable

build_exe_options = {'packages': ['PyQt5', 'sys'],
                     'excludes': []
                     }
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(name='runFastApi',
      version='0.1',
      description='打印服务',
      options={'build_exe': build_exe_options},
      executables=[Executable('main.py', base=base)])
