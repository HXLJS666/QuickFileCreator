"""
QuickFileCreator - 资源管理器路径获取模块

本模块负责：
1. 检测当前活动的资源管理器窗口
2. 通过 COM 接口获取资源管理器当前显示的路径
3. 如果没有资源管理器窗口，返回桌面路径

工作原理：
- 使用 pythoncom 初始化 COM 环境
- 通过 win32gui 获取前台窗口信息
- 使用 Shell.Application COM 对象访问资源管理器窗口集合
- 从 LocationURL 属性解析出文件路径
"""

import os
import urllib.parse
import pythoncom
import win32gui
import win32api
import win32process
import win32com.client


def get_explorer_path():
    """
    获取资源管理器当前路径
    
    工作流程：
    1. 初始化 COM 环境（必须在使用 COM 对象前调用）
    2. 获取前台窗口句柄和进程信息
    3. 判断前台窗口是否为资源管理器
    4. 如果是，从 Shell.Application 获取该窗口的路径
    5. 如果不是，遍历所有资源管理器窗口获取第一个有效路径
    
    Returns:
        str: 资源管理器当前路径，如果获取失败返回 None
    
    技术细节：
    - pythoncom.CoInitialize() 初始化 COM 线程环境
    - win32process.GetWindowThreadProcessId 获取窗口所属进程 ID
    - win32process.GetModuleFileNameEx 获取进程的可执行文件路径
    - Shell.Application.Windows() 返回所有资源管理器和 IE 窗口集合
    - LocationURL 返回 file:///C:/path 格式的 URL
    """
    try:
        # 初始化 COM 环境（每个线程使用 COM 前必须调用）
        pythoncom.CoInitialize()
        
        # 获取前台窗口句柄
        hwnd = win32gui.GetForegroundWindow()
        
        # 获取窗口所属进程 ID
        # GetWindowThreadProcessId 返回 (线程ID, 进程ID)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        
        # 打开进程句柄
        # 0x400 = PROCESS_QUERY_INFORMATION（查询信息权限）
        # 0x10 = PROCESS_VM_READ（读取内存权限）
        hndl = win32api.OpenProcess(0x400 | 0x10, False, pid)
        
        # 获取进程的可执行文件完整路径
        path = win32process.GetModuleFileNameEx(hndl, 0)

        # 判断前台窗口是否为资源管理器
        if "explorer.exe" in path.lower():
            # 创建 Shell.Application COM 对象
            shell = win32com.client.Dispatch("Shell.Application")
            
            # 获取所有资源管理器窗口集合
            windows = shell.Windows()
            
            # 遍历窗口集合，找到匹配的前台窗口
            for i in range(windows.Count):
                window = windows.Item(i)
                
                # 比较 HWND 找到当前前台窗口
                if window.HWND == hwnd:
                    # 获取 LocationURL（格式：file:///C:/Users/...）
                    location_url = window.LocationURL.replace("file:///", "")
                    
                    # URL 解码并转换路径分隔符
                    decoded_path = urllib.parse.unquote(location_url)
                    return decoded_path.replace("/", "\\")
        
        # 如果前台不是资源管理器，遍历所有资源管理器窗口
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
        # 清理 COM 环境（必须与 CoInitialize 配对）
        pythoncom.CoUninitialize()


def get_all_explorer_windows():
    """
    获取所有资源管理器窗口句柄
    
    使用 EnumWindows 枚举所有顶层窗口，
    筛选出类名为 CabinetWClass 或 ExploreWClass 的窗口。
    
    Windows 资源管理器窗口类名：
    - CabinetWClass: Windows 7+ 的资源管理器窗口
    - ExploreWClass: 旧版资源管理器窗口（兼容性）
    
    Returns:
        list: 资源管理器窗口句柄列表
    """
    windows = []
    
    def callback(hwnd, _):
        """
        枚举窗口回调函数
        
        Args:
            hwnd: 窗口句柄
            _: 额外参数（未使用）
        
        Returns:
            bool: True 继续枚举，False 停止枚举
        """
        # 只处理可见窗口
        if win32gui.IsWindowVisible(hwnd):
            # 获取窗口类名
            class_name = win32gui.GetClassName(hwnd)
            
            # 检查是否为资源管理器窗口
            if class_name in ('CabinetWClass', 'ExploreWClass'):
                windows.append(hwnd)
        
        # 返回 True 继续枚举
        return True
    
    # 枚举所有顶层窗口
    win32gui.EnumWindows(callback, None)
    
    return windows


def get_desktop_path():
    """
    获取用户桌面路径
    
    使用 os.path.expanduser 获取用户主目录，
    然后拼接 Desktop 子目录。
    
    Returns:
        str: 桌面完整路径
    """
    return os.path.join(os.path.expanduser('~'), 'Desktop')


def get_current_path():
    """
    获取当前有效路径
    
    尝试获取资源管理器路径，如果失败则返回桌面路径。
    这是模块的主要对外接口。
    
    Returns:
        str: 当前资源管理器路径或桌面路径
    """
    path = get_explorer_path()
    
    # 验证路径是否存在且为目录
    if path and os.path.isdir(path):
        return path
    
    # 获取失败时返回桌面路径
    return get_desktop_path()
