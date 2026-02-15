"""
QuickFileCreator - 用户界面模块

本模块负责：
1. 创建极简的输入框窗口
2. 处理用户输入和键盘事件
3. 自动聚焦窗口以提供更好的用户体验

工作原理：
- 使用 tkinter 创建无边框窗口
- 通过 Windows API 和 pyautogui 强制窗口获取焦点
- 监听 Enter 和 Escape 键处理用户操作
"""

import tkinter as tk
from tkinter import ttk
import config
from file_creator import create_item, is_valid_name
from explorer import get_current_path


class QuickCreateWindow:
    """
    快速创建窗口类
    
    创建一个屏幕居中的极简输入框窗口，用于快速输入文件名。
    
    窗口特性：
    - 无边框（overrideredirect）
    - 始终置顶（topmost）
    - 屏幕居中显示
    - 深色主题
    """
    
    def __init__(self):
        """
        初始化窗口
        
        创建 tkinter 窗口并设置以下属性：
        - overrideredirect(True): 移除窗口边框和标题栏
        - topmost: 窗口始终显示在最前面
        - toolwindow: 工具窗口样式，不在任务栏显示
        """
        self.root = tk.Tk()
        self.root.overrideredirect(True)      # 移除窗口边框
        self.root.attributes('-topmost', True)  # 始终置顶
        self.root.attributes('-toolwindow', True)  # 工具窗口样式
        
        # 按顺序初始化窗口各组件
        self._setup_window()    # 设置窗口位置和大小
        self._setup_ui()        # 创建输入框
        self._bind_events()     # 绑定事件处理
        self._force_focus()     # 强制获取焦点
        
    def _setup_window(self):
        """
        设置窗口位置和大小
        
        计算屏幕中心位置，将窗口居中显示。
        使用 config.py 中定义的窗口尺寸和颜色。
        """
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 计算居中位置
        x = (screen_width - config.WINDOW_WIDTH) // 2
        y = (screen_height - config.WINDOW_HEIGHT) // 2
        
        # 设置窗口位置和大小
        self.root.geometry(f'{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+{x}+{y}')
        self.root.configure(bg=config.WINDOW_BG_COLOR)
        
    def _setup_ui(self):
        """
        创建用户界面组件
        
        创建一个输入框，设置以下样式：
        - 字体：微软雅黑 12号
        - 深色背景
        - 白色文字
        - 蓝色聚焦边框
        - 初始显示占位符文本
        """
        self.entry = tk.Entry(
            self.root,
            font=config.ENTRY_FONT,              # 字体设置
            bg=config.ENTRY_BG_COLOR,            # 背景色
            fg=config.ENTRY_FG_COLOR,            # 文字颜色
            insertbackground=config.ENTRY_FG_COLOR,  # 光标颜色
            relief='flat',                       # 无边框样式
            highlightthickness=1,                # 边框宽度
            highlightbackground='#555555',       # 默认边框颜色
            highlightcolor='#0078d4'             # 聚焦时边框颜色
        )
        
        # 填充窗口，留出 5px 边距
        self.entry.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 显示占位符文本
        self.entry.insert(0, config.PLACEHOLDER_TEXT)
        self.entry.config(fg=config.PLACEHOLDER_COLOR)
        
    def _bind_events(self):
        """
        绑定事件处理函数
        
        绑定以下事件：
        - <FocusIn>: 输入框获得焦点时清除占位符
        - <FocusOut>: 输入框失去焦点时恢复占位符
        - <Return>: 按下 Enter 键创建文件
        - <Escape>: 按下 Escape 键取消
        - <Button-1>: 点击窗口外部关闭
        """
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        self.entry.bind('<Return>', self._on_enter)
        self.entry.bind('<Escape>', self._on_escape)
        self.root.bind('<Button-1>', self._on_click_outside)
        
    def _on_focus_in(self, event):
        """
        输入框获得焦点时的处理
        
        如果当前显示的是占位符文本，则清除它并将文字颜色改为正常颜色。
        """
        if self.entry.get() == config.PLACEHOLDER_TEXT:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=config.ENTRY_FG_COLOR)
            
    def _on_focus_out(self, event):
        """
        输入框失去焦点时的处理
        
        如果输入框为空，则恢复显示占位符文本。
        """
        if not self.entry.get():
            self.entry.insert(0, config.PLACEHOLDER_TEXT)
            self.entry.config(fg=config.PLACEHOLDER_COLOR)
            
    def _on_enter(self, event):
        """
        按下 Enter 键时的处理
        
        工作流程：
        1. 获取用户输入的名称
        2. 验证名称是否合法
        3. 获取当前资源管理器路径
        4. 创建文件或文件夹
        5. 关闭窗口
        
        Returns:
            str: "break" 阻止事件继续传播
        """
        name = self.entry.get()
        
        # 检查是否为有效输入（非空且非占位符）
        if name and name != config.PLACEHOLDER_TEXT:
            # 验证名称合法性
            valid, error = is_valid_name(name)
            if valid:
                # 获取当前路径并创建项目
                current_path = get_current_path()
                success, message = create_item(current_path, name)
                self._show_feedback(success, message)
            else:
                self._show_feedback(False, error)
        
        # 关闭窗口
        self.root.quit()      # 退出 mainloop
        self.root.destroy()   # 销毁窗口
        return "break"        # 阻止事件传播
        
    def _on_escape(self, event):
        """
        按下 Escape 键时的处理
        
        直接关闭窗口，不执行任何创建操作。
        
        Returns:
            str: "break" 阻止事件继续传播
        """
        self.root.quit()
        self.root.destroy()
        return "break"
        
    def _on_click_outside(self, event):
        """
        点击窗口外部时的处理
        
        如果点击的是窗口本身（而非输入框），则关闭窗口。
        """
        widget = event.widget
        if widget == self.root:
            self._close()
            
    def _show_feedback(self, success, message):
        """
        显示操作结果反馈
        
        预留的反馈显示接口，目前未实现具体功能。
        可以扩展为显示 toast 通知或状态提示。
        
        Args:
            success: 操作是否成功
            message: 反馈消息
        """
        pass
        
    def _force_focus(self):
        """
        强制窗口获取焦点
        
        由于无边框窗口默认无法获取焦点，
        需要延迟执行焦点获取操作。
        
        使用 after() 延迟 50ms 执行，确保窗口已完全创建。
        """
        self.root.after(50, self._do_force_focus)
        
    def _do_force_focus(self):
        """
        执行强制焦点获取
        
        使用多种方法确保窗口获得焦点：
        1. Windows API: SetForegroundWindow, ShowWindow, SetFocus
        2. pyautogui: 模拟点击窗口区域
        3. tkinter: deiconify, lift, focus_force
        
        这种多重方法确保在各种情况下都能成功获取焦点。
        """
        try:
            import ctypes
            import pygetwindow as gw
            import pyautogui
            
            # 获取窗口句柄
            hwnd = self.root.winfo_id()
            
            # 使用 Windows API 强制窗口到前台
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE = 9
            ctypes.windll.user32.SetFocus(hwnd)
            
            # 使用 pyautogui 点击窗口区域激活窗口
            x = self.root.winfo_x() + 10
            y = self.root.winfo_y() + 10
            pyautogui.click(x, y)
        except Exception:
            pass
        
        # 使用 tkinter 方法确保焦点
        self.root.deiconify()       # 显示窗口
        self.root.lift()            # 提升窗口层级
        self.root.focus_force()     # 强制获取焦点
        self.entry.focus_set()      # 设置输入框焦点
        self.entry.select_range(0, tk.END)  # 全选文本
        
        # 如果显示的是占位符，则清除
        if self.entry.get() == config.PLACEHOLDER_TEXT:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=config.ENTRY_FG_COLOR)
        
    def _close(self):
        """关闭窗口"""
        self.root.destroy()
        
    def show(self):
        """
        显示窗口并进入事件循环
        
        设置输入框焦点后进入 tkinter 主事件循环。
        此方法会阻塞直到窗口关闭。
        """
        self.entry.focus_set()
        self.root.mainloop()


def show_quick_create():
    """
    创建并显示快速创建窗口
    
    这是模块的入口函数，由 main.py 中的线程调用。
    创建窗口实例并进入事件循环。
    """
    window = QuickCreateWindow()
    window.show()
