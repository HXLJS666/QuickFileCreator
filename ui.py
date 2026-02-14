import tkinter as tk
from tkinter import ttk
import config
from file_creator import create_item, is_valid_name
from explorer import get_current_path


class QuickCreateWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-toolwindow', True)
        
        self._setup_window()
        self._setup_ui()
        self._bind_events()
        self._force_focus()
        
    def _setup_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - config.WINDOW_WIDTH) // 2
        y = (screen_height - config.WINDOW_HEIGHT) // 2
        self.root.geometry(f'{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+{x}+{y}')
        self.root.configure(bg=config.WINDOW_BG_COLOR)
        
    def _setup_ui(self):
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
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        self.entry.bind('<Return>', self._on_enter)
        self.entry.bind('<Escape>', self._on_escape)
        self.root.bind('<Button-1>', self._on_click_outside)
        
    def _on_focus_in(self, event):
        if self.entry.get() == config.PLACEHOLDER_TEXT:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=config.ENTRY_FG_COLOR)
            
    def _on_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, config.PLACEHOLDER_TEXT)
            self.entry.config(fg=config.PLACEHOLDER_COLOR)
            
    def _on_enter(self, event):
        name = self.entry.get()
        if name and name != config.PLACEHOLDER_TEXT:
            valid, error = is_valid_name(name)
            if valid:
                current_path = get_current_path()
                success, message = create_item(current_path, name)
                self._show_feedback(success, message)
            else:
                self._show_feedback(False, error)
        self.root.quit()
        self.root.destroy()
        return "break"
        
    def _on_escape(self, event):
        self.root.quit()
        self.root.destroy()
        return "break"
        
    def _on_click_outside(self, event):
        widget = event.widget
        if widget == self.root:
            self._close()
            
    def _show_feedback(self, success, message):
        pass
        
    def _force_focus(self):
        self.root.after(50, self._do_force_focus)
        
    def _do_force_focus(self):
        try:
            import ctypes
            ctypes.windll.user32.SetForegroundWindow(self.root.winfo_id())
            ctypes.windll.user32.ShowWindow(self.root.winfo_id(), 9)  # SW_RESTORE
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
        self.root.destroy()
        
    def show(self):
        self.entry.focus_set()
        self.root.mainloop()


def show_quick_create():
    window = QuickCreateWindow()
    window.show()
