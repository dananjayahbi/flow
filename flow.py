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
    print("   ✅ Finish: Type 'done', 'finish', or 'end' to complete session")
    print("   ❓ Help: Type 'help' for more options")
    print("\n" + "-"*50)
    
    while True:
        try:
            user_input = input("\n👤 Your instruction: ").strip()
            
            if not user_input:
                print("⚠️  Please enter an instruction...")
                continue
                
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
    
    # Check for finish commands
    finish_keywords = ['done', 'finish', 'end', 'complete', 'stop', 'exit', 'quit']
    if any(keyword in input_lower for keyword in finish_keywords):
        return 'finish', user_input
    
    # Check for help
    if 'help' in input_lower:
        return 'help', user_input
    
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
    
    print("\n✅ TO FINISH:")
    print("   - Type: 'done', 'finish', 'end', or 'complete'")
    print("   - The session will end with a summary")
    
    print("\n💡 TIPS:")
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
