import os
import win32gui
import win32process
import win32con
import win32api


def get_explorer_path():
    hwnd = win32gui.GetForegroundWindow()
    class_name = win32gui.GetClassName(hwnd)
    
    if class_name not in ('CabinetWClass', 'ExploreWClass'):
        return None
    
    try:
        return _get_path_from_explorer_hwnd(hwnd)
    except Exception:
        return None


def _get_path_from_explorer_hwnd(hwnd):
    import comtypes.client
    shell_windows = comtypes.client.CreateObject("Shell.Application").Windows()
    
    for i in range(shell_windows.Count):
        window = shell_windows.Item(i)
        if window.HWND == hwnd:
            path = os.path.dirname(window.LocationURL)
            from urllib.parse import unquote, urlparse
            parsed = urlparse(window.LocationURL)
            return unquote(parsed.path)
    
    pid = win32process.GetWindowThreadProcessId(hwnd)[1]
    return _get_path_via_pidl(pid)


def _get_path_via_pidl(pid):
    try:
        import ctypes
        from ctypes import wintypes
        
        ole32 = ctypes.windll.ole32
        ole32.CoInitialize(None)
        
        shell32 = ctypes.windll.shell32
        hwnd = win32gui.GetForegroundWindow()
        
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        if shell32.SHGetFolderPathW(hwnd, 0, None, 0, buf) == 0:
            return buf.value
    except Exception:
        pass
    
    return None


def get_desktop_path():
    return os.path.join(os.path.expanduser('~'), 'Desktop')


def get_current_path():
    path = get_explorer_path()
    if path and os.path.isdir(path):
        return path
    return get_desktop_path()
