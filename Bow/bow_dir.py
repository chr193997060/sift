import sys
import os
def bow_path():
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)

if __name__=='__main__':
    print(bow_path())
