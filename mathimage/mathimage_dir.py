import sys
import os
def mathimage_path():
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)

if __name__=='__main__':
    print(mathimage_path())
