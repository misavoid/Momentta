import platform
import subprocess
from typing import Optional


def get_active_window_title():
    if platform.system() == 'Windows':
        return get_active_window_title_windows()
    elif platform.system() == 'Darwin':  # this is for MacOS
        return get_active_window_title_mac()
    elif platform.system() == 'Linux':
        return get_active_window_title_linux()
    else:
        raise Exception('Unsupported platform: ' + platform.system())


def get_active_window_title_windows() -> Optional[str]:
    # Your implementation for windows goes here
    pass


def get_active_window_title_mac():
    script = """
    global frontApp, frontAppName, windowTitle
    
    tell application \"System Events\"
        set frontApp to first application process whose frontmost is true
        set frontAppName to name of frontApp
        tell process frontAppName
            tell (1st window whose value of attribute \"AXMain\" is true)
                set windowTitle to value of attribute \"AXTitle\"
            end tell
        end tell
    end tell
    
    return windowTitle
    """
    try:
        # Running the AppleScript
        window_title = subprocess.check_output(["osascript", "-e", script]).decode("utf-8").strip()
        return window_title
    except subprocess.CalledProcessError:
        return None


def get_active_window_title_linux() -> Optional[str]:
    # Your implementation for linux goes here
    pass
