#!/usr/bin/env node

/**
 * GitHub Copilot Mid-Chat Review Flow (Node.js version)
 * =====================================================
 * 
 * Alternative implementation in JavaScript/Node.js
 * Same functionality as the Python version
 */

const readline = require('readline');
const fs = require('fs').promises;
const path = require('path');

class GitHubCopilotFlow {
    constructor() {
        this.rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
    }

    printBanner() {
        const now = new Date().toLocaleTimeString();
        console.log('\n' + '='.repeat(50));
        console.log('🔄 GITHUB COPILOT REVIEW CHECKPOINT');
        console.log('='.repeat(50));
        console.log(`⏰ Time: ${now}`);
        console.log('📍 Current task completed');
        console.log('-'.repeat(50));
    }

    async getUserInput() {
        console.log('\n💬 What would you like to do next?');
        console.log('\n📋 Options:');
        console.log('   🔄 Continue: Describe changes, improvements, or new features');
        console.log('   ✅ Finish: Type "done", "finish", or "end" to complete session');
        console.log('   ❓ Help: Type "help" for more options');
        console.log('\n' + '-'.repeat(50));

        return new Promise((resolve) => {
            const askInput = () => {
                this.rl.question('\n👤 Your instruction: ', (answer) => {
                    if (!answer.trim()) {
                        console.log('⚠️  Please enter an instruction...');
                        askInput();
                    } else {
                        resolve(answer.trim());
                    }
                });
            };
            askInput();
        });
    }

    processInput(userInput) {
        const inputLower = userInput.toLowerCase().trim();
        const finishKeywords = ['done', 'finish', 'end', 'complete', 'stop', 'exit', 'quit'];
        
        if (finishKeywords.some(keyword => inputLower.includes(keyword))) {
            return { action: 'finish', input: userInput };
        }
        
        if (inputLower.includes('help')) {
            return { action: 'help', input: userInput };
        }
        
        return { action: 'continue', input: userInput };
    }

    showHelp() {
        console.log('\n' + '='.repeat(50));
        console.log('📚 HELP - How to use this review checkpoint:');
        console.log('='.repeat(50));
        console.log('\n🔄 TO CONTINUE:');
        console.log('   - Describe what you want to change or add');
        console.log('   - Example: "Add a dark mode toggle"');
        console.log('   - Example: "Fix the responsive design issues"');
        console.log('   - Example: "Add more animations"');
        
        console.log('\n✅ TO FINISH:');
        console.log('   - Type: "done", "finish", "end", or "complete"');
        console.log('   - The session will end with a summary');
        
        console.log('\n💡 TIPS:');
        console.log('   - Be specific about what you want');
        console.log('   - You can ask for multiple changes at once');
        console.log('   - GitHub Copilot will continue from where it left off');
        console.log('\n' + '-'.repeat(50));
    }

    generateResponse(action, userInput) {
        if (action === 'finish') {
            return `
🎯 SESSION ENDING

User has chosen to finish the session.
Final instruction: "${userInput}"

===== SUMMARY REQUEST =====
Please provide a comprehensive summary of:
1. What was accomplished in this session
2. Files created or modified
3. Key features implemented
4. Any remaining tasks or suggestions

Thank you for the productive session! 🎉
`;
        } else if (action === 'continue') {
            return `
🚀 CONTINUING SESSION

User wants to continue with: "${userInput}"

===== NEXT STEPS =====
Please implement the following request:
${userInput}

Continue working on this task and run the flow again when ready for the next review checkpoint.
`;
        } else {
            return `
📚 Help information displayed to user.
Please wait for user to provide their actual instruction...
`;
        }
    }

    async saveSessionLog(action, userInput) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            action: action,
            user_input: userInput
        };

        const logFile = path.join(__dirname, 'session_log.json');

        try {
            let logs = [];
            try {
                const data = await fs.readFile(logFile, 'utf8');
                logs = JSON.parse(data);
            } catch (err) {
                // File doesn't exist or is empty, start with empty array
            }

            logs.push(logEntry);
            await fs.writeFile(logFile, JSON.stringify(logs, null, 2));
        } catch (error) {
            console.log(`⚠️  Could not save log: ${error.message}`);
        }
    }

    async run() {
        try {
            this.printBanner();

            while (true) {
                const userInput = await this.getUserInput();
                const { action, input } = this.processInput(userInput);

                if (action === 'help') {
                    this.showHelp();
                    continue;
                }

                await this.saveSessionLog(action, input);

                const response = this.generateResponse(action, input);
                console.log('\n' + '='.repeat(50));
                console.log('📤 RESPONSE FOR GITHUB COPILOT:');
                console.log('='.repeat(50));
                console.log(response);
                console.log('='.repeat(50));

                break;
            }
        } catch (error) {
            console.log(`\n❌ Error in flow script: ${error.message}`);
            console.log('\n🔄 Defaulting to continue session...');
            console.log('Please try again or contact support.');
            process.exit(1);
        } finally {
            this.rl.close();
        }
    }
}

// Run the flow
const flow = new GitHubCopilotFlow();
flow.run().catch(console.error);
