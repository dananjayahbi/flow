# GitHub Copilot Interactive Flow System

This directory contains the interactive flow system for GitHub Copilot mid-chat reviews.

## How It Works

1. **GitHub Copilot completes a task**
2. **Automatically runs `python flow.py`** (via instructions)
3. **Script pauses and asks for user input** in terminal
4. **User provides feedback or instructions**
5. **Script returns formatted response** to GitHub Copilot
6. **Conversation continues naturally**

## Files

- `flow.py` - Main interactive flow script
- `session_log.json` - Automatic session logging
- `README.md` - This file

## Usage Examples

### Continue with Changes:
```
Your instruction: Add a dark mode toggle and improve the animations
```

### Finish Session:
```
Your instruction: done
```

### Get Help:
```
Your instruction: help
```

## Features

- ✅ Interactive terminal input
- ✅ Smart keyword detection (done/finish/end)
- ✅ Help system
- ✅ Session logging
- ✅ Error handling
- ✅ Formatted responses for GitHub Copilot
- ✅ Timestamp tracking

## Integration

Create an instruction file `important.instructions.md` in github copilot settings with the content of `important.instructions.md` in this directory (You can add more trigger scenarios as needed).

*Note : Make sure update the flow.py or flow.js file path in the instructions file.*

The script will handle the rest automatically!

## Benefits

1. **Guaranteed execution** - Always runs when GitHub Copilot finishes
2. **Interactive control** - Real-time user feedback
3. **Flexible input** - Any instruction format accepted
4. **Session tracking** - Automatic logging of interactions
5. **Error resilient** - Handles interruptions gracefully