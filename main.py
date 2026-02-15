"""
QuickFileCreator - 主程序入口

本模块负责：
1. 创建系统托盘图标和菜单
2. 注册全局快捷键监听
3. 管理应用程序生命周期

工作原理：
- 使用 pystray 库创建系统托盘图标
- 使用 keyboard 库监听全局快捷键
- 当快捷键触发时，在新线程中创建输入窗口
"""

import sys
import threading
import keyboard
import pystray
from PIL import Image, ImageDraw
import config
from ui import show_quick_create


def create_tray_icon_image():
    """
    创建托盘图标图像
    
    使用 Pillow 库绘制一个简单的图标：
    - 蓝色圆角矩形背景
    - 白色横线表示"文件"图标
    
    Returns:
        PIL.Image: 64x64 像素的 RGBA 图像对象
    """
    # 创建 64x64 透明背景图像
    img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制蓝色圆角矩形背景（模拟文件图标）
    draw.rectangle([8, 8, 56, 56], fill='#0078d4', outline='#005a9e', width=2)
    
    # 绘制白色横线（表示文件内容）
    draw.rectangle([16, 20, 48, 28], fill='white')
    draw.rectangle([16, 36, 48, 44], fill='white')
    
    return img


class QuickFileCreator:
    """
    快速文件创建器主类
    
    负责管理整个应用程序的生命周期，包括：
    - 系统托盘图标的创建和管理
    - 全局快捷键的注册和响应
    - 输入窗口的创建和销毁
    """
    
    def __init__(self):
        """初始化应用程序状态"""
        self.running = False           # 应用程序运行状态标志
        self.window_thread = None      # 输入窗口线程引用
        self.tray_icon = None          # 托盘图标对象
        
    def on_hotkey(self):
        """
        快捷键触发回调函数
        
        当用户按下 Ctrl+Alt+N 时被调用。
        
        工作原理：
        1. 检查是否已有输入窗口在显示（防止重复弹出）
        2. 如果没有，创建新的守护线程来显示输入窗口
        3. 使用守护线程确保主程序退出时窗口线程也会结束
        """
        # 如果窗口线程存在且仍在运行，则不创建新窗口
        if self.window_thread and self.window_thread.is_alive():
            return
        
        # 创建守护线程运行输入窗口
        # daemon=True 表示主程序退出时此线程也会自动结束
        self.window_thread = threading.Thread(target=show_quick_create, daemon=True)
        self.window_thread.start()
        
    def on_exit(self, icon=None, item=None):
        """
        退出程序回调函数
        
        当用户点击托盘菜单的"退出"时被调用。
        
        Args:
            icon: pystray 图标对象（可选）
            item: 菜单项对象（可选）
        
        工作原理：
        1. 设置运行状态为 False
        2. 停止托盘图标事件循环
        3. 解除所有键盘钩子
        """
        self.running = False
        if self.tray_icon:
            self.tray_icon.stop()      # 停止托盘图标事件循环
        keyboard.unhook_all()          # 清除所有键盘钩子
        
    def create_tray_menu(self):
        """
        创建托盘右键菜单
        
        Returns:
            pystray.Menu: 托盘菜单对象
        
        菜单结构：
        - 快捷键提示（禁用状态，仅展示）
        - 分隔线
        - 退出按钮
        """
        return pystray.Menu(
            # 显示当前快捷键（enabled=False 使其不可点击）
            pystray.MenuItem(f"快捷键: {config.HOTKEY}", lambda: None, enabled=False),
            pystray.Menu.SEPARATOR,    # 分隔线
            pystray.MenuItem("退出", self.on_exit)  # 退出按钮
        )
        
    def run(self):
        """
        启动应用程序
        
        工作原理：
        1. 注册全局快捷键监听
        2. 创建托盘图标
        3. 进入托盘图标事件循环（阻塞）
        
        事件循环会持续运行直到用户点击"退出"
        """
        # 注册全局快捷键，绑定到 on_hotkey 回调
        keyboard.add_hotkey(config.HOTKEY, self.on_hotkey)
        
        # 创建托盘图标
        icon_image = create_tray_icon_image()
        self.tray_icon = pystray.Icon(
            "QuickFileCreator",                    # 图标唯一标识
            icon_image,                            # 图标图像
            "快速文件创建工具",                    # 鼠标悬停提示
            menu=self.create_tray_menu()           # 右键菜单
        )
        
        # 设置运行状态并进入事件循环
        self.running = True
        self.tray_icon.run()  # 阻塞运行，直到调用 stop()


def main():
    """程序入口函数"""
    app = QuickFileCreator()
    app.run()


if __name__ == '__main__':
    main()
