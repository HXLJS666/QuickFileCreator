"""
QuickFileCreator - 主程序入口

详细技术文档见: TECHNICAL.md#主程序-mainpy
"""

import sys
import threading
import keyboard
import pystray
from PIL import Image, ImageDraw
import config
from ui import show_quick_create


def create_tray_icon_image():
    """创建托盘图标图像，详见 TECHNICAL.md#托盘图标创建"""
    img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([8, 8, 56, 56], fill='#0078d4', outline='#005a9e', width=2)
    draw.rectangle([16, 20, 48, 28], fill='white')
    draw.rectangle([16, 36, 48, 44], fill='white')
    return img


class QuickFileCreator:
    """应用程序主类，详见 TECHNICAL.md#QuickFileCreator-类"""
    
    def __init__(self):
        self.running = False           # 应用程序运行状态标志
        self.window_thread = None      # 输入窗口线程引用
        self.tray_icon = None          # 托盘图标对象
        
    def on_hotkey(self):
        """快捷键触发回调，详见 TECHNICAL.md#快捷键处理流程"""
        if self.window_thread and self.window_thread.is_alive():
            return
        self.window_thread = threading.Thread(target=show_quick_create, daemon=True)
        self.window_thread.start()
        
    def on_exit(self, icon=None, item=None):
        """退出程序回调"""
        self.running = False
        if self.tray_icon:
            self.tray_icon.stop()
        keyboard.unhook_all()
        
    def create_tray_menu(self):
        """创建托盘右键菜单，详见 TECHNICAL.md#托盘菜单结构"""
        return pystray.Menu(
            pystray.MenuItem(f"快捷键: {config.HOTKEY}", lambda: None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("退出", self.on_exit)
        )
        
    def run(self):
        """启动应用程序"""
        keyboard.add_hotkey(config.HOTKEY, self.on_hotkey)
        
        icon_image = create_tray_icon_image()
        self.tray_icon = pystray.Icon(
            "QuickFileCreator",
            icon_image,
            "快速文件创建工具",
            menu=self.create_tray_menu()
        )
        
        self.running = True
        self.tray_icon.run()


def main():
    """程序入口函数"""
    app = QuickFileCreator()
    app.run()


if __name__ == '__main__':
    main()
