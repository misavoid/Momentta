import platform
import subprocess
from typing import Optional


def get_active_application():
    if platform.system() == 'Windows':
        return get_active_application_windows()
    elif platform.system() == 'Darwin':  # This is for macOS.
        return get_active_application_mac()
    elif platform.system() == 'Linux':
        return get_active_application_linux()
    else:
        raise Exception('Unsupported platform: ' + platform.system())


def get_active_application_windows() -> Optional[str]:
    # Your implementation for Windows goes here
    pass


def get_active_application_mac() -> Optional[str]:
    script = '''
    global frontApp, frontAppName, windowTitle

    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        set frontAppName to name of frontApp
        tell process frontAppName
            tell (1st window whose value of attribute "AXMain" is true)
            end tell
        end tell
    end tell

    return frontAppName 
    '''

    try:
        # Running the AppleScript
        output = subprocess.check_output(["osascript", "-e", script]).decode("utf-8").strip()
        return output
    except subprocess.CalledProcessError:
        return None



def get_active_application_linux() -> Optional[str]:
    # Your implementation for Linux goes here
    pass
