"""
QuickFileCreator - 用户界面模块

详细技术文档见: TECHNICAL.md#用户界面-uipy
"""

import tkinter as tk
from tkinter import ttk
import config
from file_creator import create_item, is_valid_name
from explorer import get_current_path


class QuickCreateWindow:
    """快速创建窗口类，详见 TECHNICAL.md#窗口特性"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-toolwindow', True)
        self.error_timer = None
        
        self._setup_window()
        self._setup_ui()
        self._bind_events()
        self._force_focus()
        
    def _setup_window(self):
        """设置窗口位置和大小"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - config.WINDOW_WIDTH) // 2
        y = (screen_height - config.WINDOW_HEIGHT) // 2
        self.root.geometry(f'{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+{x}+{y}')
        self.root.configure(bg=config.WINDOW_BG_COLOR)
        
    def _setup_ui(self):
        """创建用户界面组件"""
        self.error_frame = tk.Frame(
            self.root,
            bg='#c42b1c',
            height=30
        )
        self.error_frame.pack(fill='x', padx=5, pady=(5, 0))
        self.error_frame.pack_forget()
        
        self.error_label = tk.Label(
            self.error_frame,
            text='',
            bg='#c42b1c',
            fg='white',
            font=('Microsoft YaHei UI', 10)
        )
        self.error_label.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.entry = tk.Entry(
            self.root,
            font=config.ENTRY_FONT,
            bg=config.ENTRY_BG_COLOR,
            fg=config.ENTRY_FG_COLOR,
            insertbackground=config.ENTRY_FG_COLOR,
            relief='flat',
            highlightthickness=1,
            highlightbackground='#555555',
            highlightcolor='#0078d4'
        )
        self.entry.pack(fill='both', expand=True, padx=5, pady=5)
        self.entry.insert(0, config.PLACEHOLDER_TEXT)
        self.entry.config(fg=config.PLACEHOLDER_COLOR)
        
    def _bind_events(self):
        """绑定事件处理"""
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        self.entry.bind('<Return>', self._on_enter)
        self.entry.bind('<Escape>', self._on_escape)
        self.root.bind('<Button-1>', self._on_click_outside)
        
    def _on_focus_in(self, event):
        """输入框获得焦点时清除占位符"""
        if self.entry.get() == config.PLACEHOLDER_TEXT:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=config.ENTRY_FG_COLOR)
            
    def _on_focus_out(self, event):
        """输入框失去焦点时恢复占位符"""
        if not self.entry.get():
            self.entry.insert(0, config.PLACEHOLDER_TEXT)
            self.entry.config(fg=config.PLACEHOLDER_COLOR)
            
    def _on_enter(self, event):
        """按下 Enter 键创建文件"""
        name = self.entry.get()
        
        if not name or name == config.PLACEHOLDER_TEXT:
            self._show_error("名称不能为空")
            return "break"
        
        valid, error = is_valid_name(name)
        if not valid:
            self._show_error(error)
            return "break"
        
        current_path = get_current_path()
        success, message = create_item(current_path, name)
        
        if success:
            self._close()
        else:
            self._show_error(message)
        
        return "break"
        
    def _on_escape(self, event):
        """按下 Escape 键取消"""
        self.root.quit()
        self.root.destroy()
        return "break"
        
    def _on_click_outside(self, event):
        """点击窗口外部关闭"""
        widget = event.widget
        if widget == self.root:
            self._close()
            
    def _show_error(self, message):
        """显示错误提示"""
        if self.error_timer:
            self.root.after_cancel(self.error_timer)
        
        self.error_label.config(text=message)
        self.error_frame.pack(fill='x', padx=5, pady=(5, 0))
        
        self.root.geometry(f'{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT + 40}')
        
        self._reposition_window()
        
        self.entry.focus_set()
        self.entry.select_range(0, tk.END)
        
        self.error_timer = self.root.after(3000, self._hide_error)
        
    def _hide_error(self):
        """隐藏错误提示"""
        self.error_frame.pack_forget()
        self.root.geometry(f'{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}')
        self._reposition_window()
        self.error_timer = None
        
    def _reposition_window(self):
        """重新定位窗口到屏幕中央"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def _force_focus(self):
        """强制窗口获取焦点"""
        self.root.after(50, self._do_force_focus)
        
    def _do_force_focus(self):
        """执行焦点获取"""
        try:
            import ctypes
            import pygetwindow as gw
            import pyautogui
            
            hwnd = self.root.winfo_id()
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            ctypes.windll.user32.ShowWindow(hwnd, 9)
            ctypes.windll.user32.SetFocus(hwnd)
            
            x = self.root.winfo_x() + 10
            y = self.root.winfo_y() + 10
            pyautogui.click(x, y)
        except Exception:
            pass
        
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.entry.focus_set()
        self.entry.select_range(0, tk.END)
        
        if self.entry.get() == config.PLACEHOLDER_TEXT:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=config.ENTRY_FG_COLOR)
        
    def _close(self):
        """关闭窗口"""
        self.root.quit()
        self.root.destroy()
        
    def show(self):
        """显示窗口并进入事件循环"""
        self.entry.focus_set()
        self.root.mainloop()


def show_quick_create():
    """创建并显示快速创建窗口"""
    window = QuickCreateWindow()
    window.show()
