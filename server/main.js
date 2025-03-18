const fs = require("fs")
const http = require("http")
const path = require("path")
const os = require("os")
const util = require("util")
const process = require("process")
const { buffer } = require("stream/consumers")
const pty = require("node-pty")
const { spawn } = require('node:child_process');
const { join } = require("node:path")
const { exit } = require("node:process")

const is_cyber_authenticated = function() {
    return false;
}

const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});


function shellx(command) {
    const result = [];
    let current = '';
    let inQuotes = false;
    let escapeNext = false;
    
    for (let i = 0; i < command.length; i++) {
        const char = command[i];
        
        if (escapeNext) {
            current += char;
            escapeNext = false;
        } else if (char === '\\') {
            escapeNext = true;
        } else if (char === '"' || char === "'") {
            inQuotes = !inQuotes;
        } else if (char === ' ' && !inQuotes) {
            if (current) {
                result.push(current);
                current = '';
            }
        } else {
            current += char;
        }
    }
    
    if (current) {
        result.push(current);
    }
    
    return result;
}

const main_prompt = function() {
    let buffer = []
    const promptUser = () => {
        const where = process.cwd();
        const prompt = `[[${where}] | cyber=[${is_cyber_authenticated()}]= `;

        readline.question(prompt, (command) => {
            
            // Process the command here
            buffer = shellx(command)
            process_command(buffer)
        });
    };

    // Start the prompt loop
    promptUser();
};

function process_command(buffer) {
    let command = buffer[0]
    switch (command) {
        case "-s":

            const cmd = buffer[1]
            const args = buffer.slice(2);
            
            
            // Use node-pty for interactive commands
            const ptyProcess = pty.spawn(cmd, args, {
                name: 'xterm-color',
                cols: 80,
                rows: 30,
                cwd: process.cwd(),
                env: process.env
            });

            ptyProcess.on('data', (data) => {
                process.stdout.write(data);
            });

            ptyProcess.on('exit', (code) => {
                console.log(`child exited with code ${code}`);
                main_prompt();
            });

            process.stdin.on('data', (data) => {
                ptyProcess.write(data);
            });

            break;
        
        case 'exit':
            exit(0)
            
        default:
            console.log(`Command not recognized: ${command}`);
            main_prompt();
            break;
    }
}

main_prompt()