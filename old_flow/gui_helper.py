#!/usr/bin/env python3
"""
Standalone GUI helper for flow.py to avoid window destruction errors
"""
import sys
import os

# Try ttkbootstrap first, fallback to tkinter
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    from ttkbootstrap.scrolled import ScrolledText
    TTK_AVAILABLE = True
except ImportError:
    import tkinter as tk
    from tkinter import ttk, scrolledtext
    TTK_AVAILABLE = False

from tkinter import messagebox

class StandaloneGUI:
    def __init__(self, initial_text=""):
        self.initial_text = initial_text
        self.result = None
        
        if TTK_AVAILABLE:
            self.setup_modern_gui()
        else:
            self.setup_fallback_gui()
    
    def setup_modern_gui(self):
        """Setup modern ttkbootstrap GUI"""
        import ttkbootstrap as ttk
        
        self.root = ttk.Window(
            title="GitHub Copilot - Detailed Instructions",
            themename="darkly",
            size=(900, 700)
        )
        
        # Main container
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="📝 Detailed Instructions Editor",
            font=('Segoe UI', 16, 'bold'),
            bootstyle="info"
        )
        title_label.pack(pady=(0, 15))
        
        # Toolbar frame
        toolbar_frame = ttk.Frame(main_frame)
        toolbar_frame.pack(fill=X, pady=(0, 10))
        
        # Left toolbar
        left_toolbar = ttk.Frame(toolbar_frame)
        left_toolbar.pack(side=LEFT)
        
        # Formatting buttons
        ttk.Button(left_toolbar, text="• Bullet", command=self.add_bullet, bootstyle="outline-secondary", width=12).pack(side=LEFT, padx=(0, 5))
        ttk.Button(left_toolbar, text="1. Number", command=self.add_number, bootstyle="outline-secondary", width=12).pack(side=LEFT, padx=(0, 5))
        ttk.Button(left_toolbar, text="→ Subitem", command=self.add_subitem, bootstyle="outline-secondary", width=12).pack(side=LEFT, padx=(0, 5))
        ttk.Button(left_toolbar, text="☐ Checkbox", command=self.add_checkbox, bootstyle="outline-secondary", width=12).pack(side=LEFT, padx=(0, 5))
        
        # Right toolbar
        right_toolbar = ttk.Frame(toolbar_frame)
        right_toolbar.pack(side=RIGHT)
        
        ttk.Button(right_toolbar, text="--- Sep", command=self.add_separator, bootstyle="outline-warning", width=10).pack(side=LEFT, padx=(0, 5))
        ttk.Button(right_toolbar, text="🗑️ Clear", command=self.clear_text, bootstyle="outline-danger", width=10).pack(side=LEFT)
        
        # Text area
        self.text_area = ScrolledText(
            main_frame,
            height=20,
            font=('Consolas', 11),
            wrap='word'
        )
        self.text_area.pack(fill=BOTH, expand=True, pady=(0, 15))
        
        if self.initial_text:
            self.text_area.insert("1.0", self.initial_text)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=(0, 10))
        
        ttk.Button(button_frame, text="✅ Submit (Ctrl+Enter)", command=self.submit, bootstyle="success", width=25).pack(side=LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="❌ Cancel (Esc)", command=self.cancel, bootstyle="danger", width=25).pack(side=LEFT)
        
        # Status
        self.status_label = ttk.Label(
            main_frame,
            text="💡 Shortcuts: Ctrl+Enter (Submit) | Escape (Cancel) | Ctrl+L (Clear)",
            font=('Segoe UI', 9),
            bootstyle="secondary"
        )
        self.status_label.pack()
        
        # Bindings
        self.root.bind('<Control-Return>', lambda e: self.submit())
        self.root.bind('<Escape>', lambda e: self.cancel())
        self.root.bind('<Control-l>', lambda e: self.clear_text())
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        
        self.text_area.focus_set()
        self.center_window()
    
    def setup_fallback_gui(self):
        """Setup fallback tkinter GUI with dark styling"""
        import tkinter as tk
        from tkinter import scrolledtext
        
        self.root = tk.Tk()
        self.root.title("GitHub Copilot - Detailed Instructions")
        self.root.geometry("900x700")
        
        # Dark theme colors
        bg_color = '#2b2b2b'
        fg_color = '#ffffff'
        entry_bg = '#3c3c3c'
        button_bg = '#404040'
        
        self.root.configure(bg=bg_color)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg=bg_color, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="📝 Detailed Instructions Editor",
            font=('Arial', 16, 'bold'),
            fg='#4CAF50', bg=bg_color
        )
        title_label.pack(pady=(0, 15))
        
        # Toolbar
        toolbar_frame = tk.Frame(main_frame, bg=bg_color)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        buttons = [
            ("• Bullet", self.add_bullet),
            ("1. Number", self.add_number),
            ("→ Subitem", self.add_subitem),
            ("☐ Checkbox", self.add_checkbox),
            ("--- Sep", self.add_separator),
            ("🗑️ Clear", self.clear_text)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                toolbar_frame,
                text=text,
                command=command,
                bg=button_bg,
                fg=fg_color,
                relief=tk.FLAT,
                padx=10,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Text area
        self.text_area = scrolledtext.ScrolledText(
            main_frame,
            height=20,
            font=('Consolas', 11),
            bg=entry_bg,
            fg=fg_color,
            insertbackground=fg_color,
            wrap=tk.WORD
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        if self.initial_text:
            self.text_area.insert(1.0, self.initial_text)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=bg_color)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        submit_btn = tk.Button(
            button_frame,
            text="✅ Submit (Ctrl+Enter)",
            command=self.submit,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        )
        submit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text="❌ Cancel (Esc)",
            command=self.cancel,
            bg='#f44336',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        )
        cancel_btn.pack(side=tk.LEFT)
        
        # Status
        status_label = tk.Label(main_frame,
                               text="💡 Shortcuts: Ctrl+Enter (Submit) | Escape (Cancel) | Ctrl+L (Clear)",
                               font=('Arial', 9),
                               fg='#cccccc', bg=bg_color)
        status_label.pack(pady=(10, 0))
        
        # Bindings
        self.root.bind('<Control-Return>', lambda e: self.submit())
        self.root.bind('<Escape>', lambda e: self.cancel())
        self.root.bind('<Control-l>', lambda e: self.clear_text())
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        
        self.text_area.focus_set()
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Formatting methods
    def add_bullet(self):
        if TTK_AVAILABLE:
            cursor_pos = self.text_area.index("insert")
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        else:
            import tkinter as tk
            cursor_pos = self.text_area.index(tk.INSERT)
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        
        if line_content.strip() == '':
            self.text_area.insert("insert" if TTK_AVAILABLE else tk.INSERT, "• ")
        else:
            self.text_area.insert("insert" if TTK_AVAILABLE else tk.INSERT, "\n• ")
        self.text_area.focus_set()
    
    def add_number(self):
        if TTK_AVAILABLE:
            cursor_pos = self.text_area.index("insert")
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        else:
            import tkinter as tk
            cursor_pos = self.text_area.index(tk.INSERT)
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        
        if line_content.strip() == '':
            self.text_area.insert("insert" if TTK_AVAILABLE else tk.INSERT, "1. ")
        else:
            self.text_area.insert("insert" if TTK_AVAILABLE else tk.INSERT, "\n1. ")
        self.text_area.focus_set()
    
    def add_subitem(self):
        if TTK_AVAILABLE:
            cursor_pos = self.text_area.index("insert")
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        else:
            import tkinter as tk
            cursor_pos = self.text_area.index(tk.INSERT)
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        
        if line_content.strip() == '':
            self.text_area.insert("insert" if TTK_AVAILABLE else tk.INSERT, "  → ")
        else:
            self.text_area.insert("insert" if TTK_AVAILABLE else tk.INSERT, "\n  → ")
        self.text_area.focus_set()
    
    def add_checkbox(self):
        if TTK_AVAILABLE:
            cursor_pos = self.text_area.index("insert")
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        else:
            import tkinter as tk
            cursor_pos = self.text_area.index(tk.INSERT)
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        
        if line_content.strip() == '':
            self.text_area.insert("insert" if TTK_AVAILABLE else tk.INSERT, "☐ ")
        else:
            self.text_area.insert("insert" if TTK_AVAILABLE else tk.INSERT, "\n☐ ")
        self.text_area.focus_set()
    
    def add_separator(self):
        if TTK_AVAILABLE:
            cursor_pos = self.text_area.index("insert")
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        else:
            import tkinter as tk
            cursor_pos = self.text_area.index(tk.INSERT)
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        
        separator = "---"
        if line_content.strip() == '':
            self.text_area.insert("insert" if TTK_AVAILABLE else tk.INSERT, separator + "\n")
        else:
            self.text_area.insert("insert" if TTK_AVAILABLE else tk.INSERT, "\n" + separator + "\n")
        self.text_area.focus_set()
    
    def clear_text(self):
        if messagebox.askquestion("Clear Text", "Are you sure you want to clear all text?") == 'yes':
            if TTK_AVAILABLE:
                self.text_area.delete("1.0", "end")
            else:
                import tkinter as tk
                self.text_area.delete(1.0, tk.END)
            self.text_area.focus_set()
    
    def submit(self):
        if TTK_AVAILABLE:
            content = self.text_area.get("1.0", "end-1c").strip()
        else:
            import tkinter as tk
            content = self.text_area.get(1.0, tk.END).strip()
        
        if not content:
            messagebox.showwarning("Empty Content", "Please enter some instructions.")
            return
        
        # Print result to stdout so parent process can capture it
        print("GUI_RESULT_START")
        print(content)
        print("GUI_RESULT_END")
        
        self.root.quit()
        self.root.destroy()
    
    def cancel(self):
        print("GUI_RESULT_CANCELLED")
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    initial_text = sys.argv[1] if len(sys.argv) > 1 else ""
    gui = StandaloneGUI(initial_text)
    gui.run()
