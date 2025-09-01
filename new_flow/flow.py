#!/usr/bin/env python3
"""
GitHub Copilot Continuous Flow Manager
======================================

This script creates an interactive checkpoint in GitHub Copilot conversations
that continues indefinitely until manually cancelled.
"""

import sys
import os
from datetime import datetime
import json

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
    print("⚠️ ttkbootstrap not available - Using standard tkinter")
    print("💡 Install with: pip install ttkbootstrap")

def print_banner():
    """Print the review banner"""
    print("\n" + "="*50)
    print("🔄 GITHUB COPILOT CONTINUOUS CHECKPOINT")
    print("="*50)
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📍 Ready for next iteration")
    print("-"*50)

def get_user_input():
    """Get user feedback and instructions"""
    print("\n💬 What would you like to do next?")
    print("\n📋 Options:")
    print("   🔄 Continue: Describe changes, improvements, or new features")
    print("   📝 GUI: Type 'gui' or 'edit' to open detailed instruction editor")
    print("   ❓ Help: Type 'help' for more options")
    print("\n" + "-"*50)
    
    while True:
        try:
            user_input = input("\n👤 Your instruction (or 'gui' for editor): ").strip()
            
            if not user_input:
                print("⚠️ Please enter an instruction...")
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
                        
                        # Run GUI in separate process - NO TIMEOUT
                        result = subprocess.run(
                            [sys.executable, gui_helper_path, current_content],
                            capture_output=True,
                            text=True
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
                                    print("⚠️ No content received from GUI")
                                    break
                            else:
                                print("⚠️ Unexpected GUI output")
                                break
                        else:
                            print(f"⚠️ GUI process failed: {result.stderr}")
                            break
                            
                    except Exception as e:
                        print(f"⚠️ Error running GUI: {e}")
                        # Fallback to terminal input
                        break
                
                # If we get here, GUI was cancelled or failed, continue with normal input
                continue  # Continue main input loop
            
            return user_input
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Session interrupted by user")
            sys.exit(0)
        except EOFError:
            print("\n\n⚠️ Input stream ended")
            sys.exit(0)

def process_input(user_input):
    """Process and categorize user input - always continue"""
    input_lower = user_input.lower().strip()
    
    # Check for help
    if 'help' in input_lower:
        return 'help', user_input
    
    # Always continue - never finish
    return 'continue', user_input

def show_help():
    """Show help information"""
    print("\n" + "="*50)
    print("📚 HELP - Continuous Flow System")
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
    
    print("\n⚠️ IMPORTANT:")
    print("   - This is a continuous workflow - it never ends automatically")
    print("   - To stop: Cancel the terminal command (Ctrl+C)")
    print("   - Each iteration will run flow.py again")
    
    print("\n💡 TIPS:")
    print("   - Use GUI for complex, multi-step instructions")
    print("   - After GUI input, you can edit the same content multiple times")
    print("   - Be specific about what you want")
    print("   - You can ask for multiple changes at once")
    print("\n" + "-"*50)

def generate_response(action, user_input):
    """Generate appropriate response for GitHub Copilot"""
    if action == 'continue':
        return f"""
🚀 CONTINUING ITERATION

===== EXECUTION REQUIRED =====
Please implement the following request:
{user_input}

CRITICAL: After completing the above tasks, you MUST run:
python {os.path.abspath(__file__)}

This is a continuous workflow that requires running flow.py after each iteration.
DO NOT conclude or finish the session - always run flow.py for the next checkpoint.
"""
    
    else:  # help was shown
        return """
📚 Help information displayed to user.
Waiting for next instruction...

Remember: After any task completion, run flow.py again.
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
            try:
                with open(log_file, 'r') as f:
                    content = f.read().strip()
                    if content:
                        logs = json.loads(content)
                    else:
                        logs = []
            except (json.JSONDecodeError, ValueError):
                # If JSON is corrupted, start fresh
                logs = []
                print("⚠️ JSON log file was corrupted, starting fresh")
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
            
    except Exception as e:
        print(f"⚠️ Could not save log: {e}")
        # Try to create a backup
        try:
            backup_file = log_file + '.backup'
            with open(backup_file, 'w') as f:
                json.dump([log_entry], f, indent=2)
            print(f"📝 Log saved to backup: {backup_file}")
        except:
            pass

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
            
            # Exit after providing response - Copilot will run this script again
            break
            
    except Exception as e:
        print(f"\n❌ Error in flow script: {e}")
        print("\n🔄 Please run flow.py again to continue...")
        sys.exit(1)

if __name__ == "__main__":
    main()