import os
import urllib.parse
import pythoncom
import win32gui
import win32api
import win32process
import win32com.client


def get_explorer_path():
    try:
        pythoncom.CoInitialize()
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        hndl = win32api.OpenProcess(0x400 | 0x10, False, pid)
        path = win32process.GetModuleFileNameEx(hndl, 0)

        if "explorer.exe" in path.lower():
            shell = win32com.client.Dispatch("Shell.Application")
            windows = shell.Windows()
            for i in range(windows.Count):
                window = windows.Item(i)
                if window.HWND == hwnd:
                    location_url = window.LocationURL.replace("file:///", "")
                    decoded_path = urllib.parse.unquote(location_url)
                    return decoded_path.replace("/", "\\")
        
        for hwnd in get_all_explorer_windows():
            shell = win32com.client.Dispatch("Shell.Application")
            windows = shell.Windows()
            for i in range(windows.Count):
                window = windows.Item(i)
                if window.HWND == hwnd:
                    location_url = window.LocationURL.replace("file:///", "")
                    decoded_path = urllib.parse.unquote(location_url)
                    return decoded_path.replace("/", "\\")
                    
        return None
    except Exception:
        return None
    finally:
        pythoncom.CoUninitialize()


def get_all_explorer_windows():
    windows = []
    
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            class_name = win32gui.GetClassName(hwnd)
            if class_name in ('CabinetWClass', 'ExploreWClass'):
                windows.append(hwnd)
        return True
    
    win32gui.EnumWindows(callback, None)
    return windows


def get_desktop_path():
    return os.path.join(os.path.expanduser('~'), 'Desktop')


def get_current_path():
    path = get_explorer_path()
    if path and os.path.isdir(path):
        return path
    return get_desktop_path()
