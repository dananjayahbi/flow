#!/usr/bin/env python3
"""
GitHub Copilot Mid-Chat Review Flow
=====================================

This script creates an interactive checkpoint in GitHub Copilot conversations.
It pauses the conversation, asks for user feedback, and continues based on input.
"""

import sys
import os
from datetime import datetime
import json
import threading
import queue
from tkinter import messagebox

try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    from ttkbootstrap.scrolled import ScrolledText
    TTK_AVAILABLE = True
    print("✅ ttkbootstrap available - Using modern UI")
except ImportError:
    import tkinter as tk
    from tkinter import ttk, scrolledtext
    TTK_AVAILABLE = False
    print("⚠️  ttkbootstrap not available - Using standard tkinter")
    print("💡 Install with: pip install ttkbootstrap")

class InstructionGUI:
    """Modern GUI for entering detailed instructions using ttkbootstrap"""
    
    def __init__(self, initial_text="", result_queue=None):
        self.result_queue = result_queue
        self.result = None
        self.window_closed = False
        
        # Check ttkbootstrap availability for this instance
        self.ttk_available = self._check_ttkbootstrap()
        
        if self.ttk_available:
            import ttkbootstrap as ttk
            self.root = ttk.Window(
                title="GitHub Copilot - Detailed Instructions",
                themename="darkly",  # Modern dark theme
                size=(800, 600),
                resizable=(True, True)
            )
        else:
            import tkinter as tk
            self.root = tk.Tk()
            self.root.title("GitHub Copilot - Detailed Instructions") 
            self.root.geometry("800x600")
            self.root.resizable(True, True)
            
        self.setup_gui(initial_text)
    
    def _check_ttkbootstrap(self):
        """Check if ttkbootstrap is available for this instance"""
        try:
            import ttkbootstrap
            return True
        except ImportError:
            return False
        
    def setup_gui(self, initial_text):
        """Setup the modern GUI components"""
        
        if self.ttk_available:
            # Modern ttkbootstrap interface
            self.setup_modern_gui(initial_text)
        else:
            # Fallback to standard tkinter
            self.setup_fallback_gui(initial_text)
    
    def setup_modern_gui(self, initial_text):
        """Setup modern ttkbootstrap GUI"""
        import ttkbootstrap as ttk
        from ttkbootstrap.constants import BOTH, X, LEFT, RIGHT
        from ttkbootstrap.scrolled import ScrolledText
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Main container with padding
        main_container = ttk.Frame(self.root, padding=20)
        main_container.pack(fill=BOTH, expand=True)
        
        # Header section with modern styling
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=X, pady=(0, 20))
        
        # Title with modern typography
        title_label = ttk.Label(
            header_frame,
            text="📝 GitHub Copilot - Detailed Instructions",
            font=('Segoe UI', 16, 'bold'),
            bootstyle="inverse-primary"
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = ttk.Label(
            header_frame,
            text="Write your detailed instructions below. Use the formatting buttons for better structure.",
            font=('Segoe UI', 10),
            bootstyle="secondary"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Modern toolbar with grouped buttons
        toolbar_frame = ttk.Frame(main_container)
        toolbar_frame.pack(fill=X, pady=(0, 15))
        
        # Formatting button group
        format_group = ttk.LabelFrame(toolbar_frame, text="Formatting", padding=10, bootstyle="primary")
        format_group.pack(side=LEFT, fill='y', padx=(0, 10))
        
        # Row 1 of formatting buttons
        format_row1 = ttk.Frame(format_group)
        format_row1.pack(fill=X, pady=(0, 5))
        
        ttk.Button(format_row1, text="• Bullet", command=self.add_bullet, 
                  bootstyle="info-outline", width=12).pack(side=LEFT, padx=(0, 5))
        ttk.Button(format_row1, text="1. Number", command=self.add_number, 
                  bootstyle="info-outline", width=12).pack(side=LEFT, padx=(0, 5))
        ttk.Button(format_row1, text="→ Sub-item", command=self.add_subitem, 
                  bootstyle="secondary-outline", width=12).pack(side=LEFT)
        
        # Row 2 of formatting buttons
        format_row2 = ttk.Frame(format_group)
        format_row2.pack(fill=X)
        
        ttk.Button(format_row2, text="--- Separator", command=self.add_separator, 
                  bootstyle="secondary-outline", width=12).pack(side=LEFT, padx=(0, 5))
        ttk.Button(format_row2, text="✓ Checkbox", command=self.add_checkbox, 
                  bootstyle="success-outline", width=12).pack(side=LEFT, padx=(0, 5))
        ttk.Button(format_row2, text="🗑️ Clear", command=self.clear_text, 
                  bootstyle="danger-outline", width=12).pack(side=LEFT)
        
        # Action button group
        action_group = ttk.LabelFrame(toolbar_frame, text="Actions", padding=10, bootstyle="success")
        action_group.pack(side=RIGHT, fill='y')
        
        ttk.Button(action_group, text="✅ Add to Terminal", command=self.add_to_terminal,
                  bootstyle="success", width=16).pack(pady=(0, 5))
        ttk.Button(action_group, text="❌ Cancel", command=self.cancel,
                  bootstyle="danger", width=16).pack()
        
        # Text area with modern styling
        text_frame = ttk.Frame(main_container)
        text_frame.pack(fill=BOTH, expand=True, pady=(0, 15))
        
        # Modern scrolled text area
        self.text_area = ScrolledText(
            text_frame,
            wrap="word",
            height=20,
            font=('Consolas', 11),
            bootstyle="secondary"
        )
        self.text_area.pack(fill=BOTH, expand=True)
        
        # Insert initial text if provided
        if initial_text:
            self.text_area.insert("1.0", initial_text)
            
        # Modern status bar
        status_frame = ttk.Frame(main_container)
        status_frame.pack(fill=X)
        
        self.status_label = ttk.Label(
            status_frame,
            text="💡 Shortcuts: Ctrl+Enter (Submit) | Escape (Cancel) | Ctrl+L (Clear)",
            font=('Segoe UI', 9),
            bootstyle="secondary"
        )
        self.status_label.pack()
        
        # Set window close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        
        # Keyboard shortcuts
        self.root.bind('<Control-Return>', lambda e: self.add_to_terminal())
        self.root.bind('<Escape>', lambda e: self.cancel())
        self.root.bind('<Control-l>', lambda e: self.clear_text())
        
        # Focus on text area
        self.text_area.focus_set()
        
        # Center window
        self.center_window()
    
    def setup_fallback_gui(self, initial_text):
        """Fallback GUI using standard tkinter"""
        import tkinter as tk
        from tkinter import scrolledtext
        
        # Configure colors for fallback
        bg_color = '#2b2b2b'
        fg_color = '#ffffff'
        self.root.configure(bg=bg_color)
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=15, pady=15, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, 
                              text="📝 GitHub Copilot - Detailed Instructions", 
                              font=('Arial', 14, 'bold'),
                              bg=bg_color, fg=fg_color)
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(main_frame, 
                                 text="Write your detailed instructions below. Use the formatting buttons for better structure.",
                                 font=('Arial', 10),
                                 bg=bg_color, fg='#cccccc')
        subtitle_label.pack(pady=(0, 10))
        
        # Simple toolbar
        toolbar_frame = tk.Frame(main_frame, bg=bg_color)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Formatting buttons - Row 1
        button_row1 = tk.Frame(toolbar_frame, bg=bg_color)
        button_row1.pack(fill=tk.X, pady=(0, 5))
        
        tk.Button(button_row1, text="• Bullet", command=self.add_bullet, 
                 bg='#3498db', fg='white', width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(button_row1, text="1. Number", command=self.add_number, 
                 bg='#3498db', fg='white', width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(button_row1, text="→ Sub-item", command=self.add_subitem, 
                 bg='#9b59b6', fg='white', width=12).pack(side=tk.LEFT, padx=2)
        
        # Formatting buttons - Row 2
        button_row2 = tk.Frame(toolbar_frame, bg=bg_color)
        button_row2.pack(fill=tk.X)
        
        tk.Button(button_row2, text="--- Separator", command=self.add_separator, 
                 bg='#95a5a6', fg='white', width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(button_row2, text="✓ Checkbox", command=self.add_checkbox, 
                 bg='#27ae60', fg='white', width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(button_row2, text="🗑️ Clear", command=self.clear_text, 
                 bg='#e74c3c', fg='white', width=12).pack(side=tk.LEFT, padx=2)
        
        # Text area
        self.text_area = scrolledtext.ScrolledText(main_frame, 
                                                  wrap=tk.WORD, 
                                                  height=18,
                                                  font=('Consolas', 11),
                                                  bg='#1e1e1e', fg=fg_color,
                                                  insertbackground='#3498db',
                                                  selectbackground='#4a4a4a')
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        if initial_text:
            self.text_area.insert(tk.END, initial_text)
            
        # Action buttons
        button_frame = tk.Frame(main_frame, bg=bg_color)
        button_frame.pack(fill=tk.X)
        
        tk.Button(button_frame, text="✅ Add to Terminal", command=self.add_to_terminal,
                 bg='#27ae60', fg='white', font=('Arial', 11, 'bold'), 
                 padx=20, pady=8).pack(side=tk.RIGHT, padx=(5, 0))
        tk.Button(button_frame, text="❌ Cancel", command=self.cancel,
                 bg='#e74c3c', fg='white', font=('Arial', 11), 
                 padx=20, pady=8).pack(side=tk.RIGHT)
        
        # Status bar
        status_label = tk.Label(main_frame,
                               text="💡 Shortcuts: Ctrl+Enter (Submit) | Escape (Cancel) | Ctrl+L (Clear)",
                               font=('Arial', 9),
                               fg='#cccccc', bg=bg_color)
        status_label.pack(pady=(10, 0))
        
        # Set window close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        
        # Keyboard shortcuts
        self.root.bind('<Control-Return>', lambda e: self.add_to_terminal())
        self.root.bind('<Escape>', lambda e: self.cancel())
        self.root.bind('<Control-l>', lambda e: self.clear_text())
        
        self.text_area.focus_set()
        self.center_window()
        
    def add_bullet(self):
        """Insert bullet point"""
        if self.ttk_available:
            cursor_pos = self.text_area.index("insert")
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        else:
            import tkinter as tk
            cursor_pos = self.text_area.index(tk.INSERT)
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        
        if line_content.strip() == '':
            self.text_area.insert("insert" if self.ttk_available else tk.INSERT, "• ")
        else:
            self.text_area.insert("insert" if self.ttk_available else tk.INSERT, "\n• ")
        self.text_area.focus_set()
        
    def add_number(self):
        """Insert numbered list item"""
        if self.ttk_available:
            cursor_pos = self.text_area.index("insert")
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        else:
            import tkinter as tk
            cursor_pos = self.text_area.index(tk.INSERT)
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        
        if line_content.strip() == '':
            self.text_area.insert("insert" if self.ttk_available else tk.INSERT, "1. ")
        else:
            self.text_area.insert("insert" if self.ttk_available else tk.INSERT, "\n1. ")
        self.text_area.focus_set()
        
    def add_subitem(self):
        """Insert sub-item"""
        if self.ttk_available:
            cursor_pos = self.text_area.index("insert")
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        else:
            import tkinter as tk
            cursor_pos = self.text_area.index(tk.INSERT)
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        
        if line_content.strip() == '':
            self.text_area.insert("insert" if self.ttk_available else tk.INSERT, "  → ")
        else:
            self.text_area.insert("insert" if self.ttk_available else tk.INSERT, "\n  → ")
        self.text_area.focus_set()
        
    def add_separator(self):
        """Insert separator line"""
        if self.ttk_available:
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
            self.text_area.insert("insert" if self.ttk_available else tk.INSERT, separator + "\n")
        else:
            self.text_area.insert("insert" if self.ttk_available else tk.INSERT, "\n" + separator + "\n")
        self.text_area.focus_set()
        
    def add_checkbox(self):
        """Insert checkbox item"""
        if self.ttk_available:
            cursor_pos = self.text_area.index("insert")
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        else:
            import tkinter as tk
            cursor_pos = self.text_area.index(tk.INSERT)
            line_start = cursor_pos.split('.')[0] + '.0'
            line_content = self.text_area.get(line_start, cursor_pos)
        
        if line_content.strip() == '':
            self.text_area.insert("insert" if self.ttk_available else tk.INSERT, "☐ ")
        else:
            self.text_area.insert("insert" if self.ttk_available else tk.INSERT, "\n☐ ")
        self.text_area.focus_set()
        
    def clear_text(self):
        """Clear all text"""
        if messagebox.askquestion("Clear Text", "Are you sure you want to clear all text?") == 'yes':
            if self.ttk_available:
                self.text_area.delete("1.0", "end")
            else:
                import tkinter as tk
                self.text_area.delete(1.0, tk.END)
            self.text_area.focus_set()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def add_to_terminal(self):
        """Add content to terminal and close GUI"""
        if self.ttk_available:
            content = self.text_area.get("1.0", "end-1c").strip()
        else:
            import tkinter as tk
            content = self.text_area.get(1.0, tk.END).strip()
            
        if not content:
            messagebox.showwarning("Empty Content", "Please enter some instructions before adding to terminal.")
            return
            
        self.result = content
        if self.result_queue:
            self.result_queue.put(content)
        
        self.cleanup()
        
    def cancel(self):
        """Cancel GUI and close window"""
        self.result = None
        if self.result_queue:
            self.result_queue.put(None)
        self.cleanup()
        
    def cleanup(self):
        """Properly cleanup the GUI window"""
        if not self.window_closed and self.root:
            try:
                self.window_closed = True
                # Unbind all events to prevent background errors
                try:
                    self.root.unbind_all('<Control-Return>')
                    self.root.unbind_all('<Escape>')
                    self.root.unbind_all('<Control-l>')
                except:
                    pass
                
                # Update to flush all pending events
                try:
                    self.root.update()
                except:
                    pass
                
                # Withdraw window before destroying
                try:
                    self.root.withdraw()
                except:
                    pass
                
                # Quit mainloop
                try:
                    self.root.quit()
                except:
                    pass
                
                # Destroy window
                try:
                    self.root.destroy()
                except:
                    pass
                
                # Clear references
                self.root = None
                self.text_area = None
                
            except Exception:
                pass  # Ensure no exceptions escape
        
    def run(self):
        """Run the GUI"""
        try:
            # Ensure window is ready
            self.root.update_idletasks()
            self.root.mainloop()
            return self.result
        except Exception as e:
            print(f"⚠️  GUI Error: {e}")
            return None
        finally:
            # Ensure cleanup even if there's an error
            self.cleanup()
            # Additional delay to ensure all cleanup is complete
            import time
            time.sleep(0.1)

def print_banner():
    """Print the review banner"""
    print("\n" + "="*50)
    print("🔄 GITHUB COPILOT REVIEW CHECKPOINT")
    print("="*50)
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📍 Current task completed")
    print("-"*50)

def get_user_input():
    """Get user feedback and instructions"""
    print("\n💬 What would you like to do next?")
    print("\n📋 Options:")
    print("   🔄 Continue: Describe changes, improvements, or new features")
    print("   ✅ Finish: Type 'done' or 'finish' to complete session")
    print("   ❓ Help: Type 'help' for more options")
    print("   📝 GUI: Type 'gui' or 'edit' to open detailed instruction editor")
    print("\n" + "-"*50)
    
    while True:
        try:
            user_input = input("\n👤 Your instruction (or 'gui' for editor): ").strip()
            
            if not user_input:
                print("⚠️  Please enter an instruction...")
                continue
            
            # Check if user wants to open GUI
            if user_input.lower() in ['gui', 'edit', 'editor']:
                current_content = ""
                
                while True:  # Loop for GUI editing
                    print("🔄 Opening GUI editor...")
                    try:
                        # Use subprocess to completely isolate GUI
                        import subprocess
                        import sys
                        
                        # Path to the GUI helper script
                        gui_helper_path = os.path.join(os.path.dirname(__file__), 'gui_helper.py')
                        
                        # Run GUI in separate process
                        result = subprocess.run(
                            [sys.executable, gui_helper_path, current_content],
                            capture_output=True,
                            text=True,
                            timeout=300  # 5 minute timeout
                        )
                        
                        # Parse result
                        if result.returncode == 0:
                            output = result.stdout.strip()
                            if "GUI_RESULT_CANCELLED" in output:
                                print("❌ GUI cancelled by user")
                                break
                            elif "GUI_RESULT_START" in output and "GUI_RESULT_END" in output:
                                # Extract content between markers
                                start_idx = output.find("GUI_RESULT_START") + len("GUI_RESULT_START")
                                end_idx = output.find("GUI_RESULT_END")
                                content = output[start_idx:end_idx].strip()
                                
                                if content:
                                    current_content = content
                                    print(f"\n✅ Instructions received from GUI:")
                                    print("=" * 60)
                                    print(content)
                                    print("=" * 60)
                                    print("📋 Press Enter to execute these instructions")
                                    print("    or type 'edit' and press Enter to modify them...")
                                    
                                    # Wait for user choice
                                    choice = input("👤 Your choice: ").strip().lower()
                                    
                                    if choice == 'edit':
                                        print("🔄 Reopening GUI editor with current content...")
                                        continue  # Continue the GUI editing loop
                                    else:
                                        # User pressed Enter or typed something else - execute instructions
                                        return content
                                else:
                                    print("⚠️  No content received from GUI")
                                    break
                            else:
                                print("⚠️  Unexpected GUI output")
                                break
                        else:
                            print(f"⚠️  GUI process failed: {result.stderr}")
                            break
                            
                    except subprocess.TimeoutExpired:
                        print("⚠️  GUI timed out")
                        break
                    except Exception as e:
                        print(f"⚠️  Error running GUI: {e}")
                        # Fallback to terminal input
                        break
                
                # If we get here, GUI was cancelled or failed, continue with normal input
                continue  # Continue main input loop
            
            return user_input
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Session interrupted by user")
            return "finish"
        except EOFError:
            print("\n\n⚠️  Input stream ended")
            return "finish"

def process_input(user_input):
    """Process and categorize user input"""
    input_lower = user_input.lower().strip()
    
    # Check for finish commands - only standalone words "done" or "finish"
    import re
    finish_keywords = ['done', 'finish']
    for keyword in finish_keywords:
        # Use word boundaries to match only standalone words
        if re.search(r'\b' + re.escape(keyword) + r'\b', input_lower):
            return 'finish', user_input
    
    # Check for help
    if 'help' in input_lower:
        return 'help', user_input
    
    # Check for GUI keywords (handled in get_user_input, but adding here for completeness)
    gui_keywords = ['gui', 'edit', 'editor']
    if input_lower in gui_keywords:
        return 'continue', user_input  # This should be handled in get_user_input
    
    # Default to continue
    return 'continue', user_input

def show_help():
    """Show help information"""
    print("\n" + "="*50)
    print("📚 HELP - How to use this review checkpoint:")
    print("="*50)
    print("\n🔄 TO CONTINUE:")
    print("   - Describe what you want to change or add")
    print("   - Example: 'Add a dark mode toggle'")
    print("   - Example: 'Fix the responsive design issues'")
    print("   - Example: 'Add more animations'")
    
    print("\n📝 DETAILED INSTRUCTIONS (GUI):")
    print("   - Type: 'gui', 'edit', or 'editor' to open GUI")
    print("   - Write detailed instructions with bullets and formatting")
    print("   - After submitting, you can type 'edit' to modify the same content")
    print("   - Use Ctrl+Enter to quickly submit from GUI")
    
    print("\n✅ TO FINISH:")
    print("   - Type: 'done' or 'finish' (as standalone words)")
    print("   - The session will end with a summary")
    
    print("\n💡 TIPS:")
    print("   - Use GUI for complex, multi-step instructions")
    print("   - After GUI input, you can edit the same content multiple times")
    print("   - Be specific about what you want")
    print("   - You can ask for multiple changes at once")
    print("   - GitHub Copilot will continue from where it left off")
    print("\n" + "-"*50)

def generate_response(action, user_input):
    """Generate appropriate response for GitHub Copilot"""
    if action == 'finish':
        return f"""
🎯 SESSION ENDING

User has chosen to finish the session.
Final instruction: "{user_input}"

===== SUMMARY REQUEST =====
Please provide a comprehensive summary of:
1. What was accomplished in this session
2. Files created or modified
3. Key features implemented
4. Any remaining tasks or suggestions

Thank you for the productive session! 🎉
"""
    
    elif action == 'continue':
        return f"""
🚀 CONTINUING SESSION

User wants to continue with: "{user_input}"

===== NEXT STEPS =====
Please implement the following request:
{user_input}

Continue working on this task and run the flow again when ready for the next review checkpoint.
"""
    
    else:  # help was shown, continue
        return """
📚 Help information displayed to user.
Please wait for user to provide their actual instruction...
"""

def save_session_log(action, user_input):
    """Save session interaction to log file"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'user_input': user_input
    }
    
    log_file = os.path.join(os.path.dirname(__file__), 'session_log.json')
    
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
            
    except Exception as e:
        print(f"⚠️  Could not save log: {e}")

def main():
    """Main flow execution"""
    try:
        print_banner()
        
        while True:
            user_input = get_user_input()
            action, processed_input = process_input(user_input)
            
            if action == 'help':
                show_help()
                continue  # Ask for input again after showing help
            
            # Save to log
            save_session_log(action, processed_input)
            
            # Generate and print response for GitHub Copilot
            response = generate_response(action, processed_input)
            print("\n" + "="*50)
            print("📤 RESPONSE FOR GITHUB COPILOT:")
            print("="*50)
            print(response)
            print("="*50)
            
            # Exit after providing response
            break
            
    except Exception as e:
        print(f"\n❌ Error in flow script: {e}")
        print("\n🔄 Defaulting to continue session...")
        print("Please try again or contact support.")
        sys.exit(1)

if __name__ == "__main__":
    main()
