import { Terminal } from "https://cdn.jsdelivr.net/npm/xterm@5.3.0/+esm";
import { FitAddon } from "https://cdn.jsdelivr.net/npm/xterm-addon-fit@0.7.0/+esm";

export class TerminalUI {
    constructor(socket) {
        this.terminal = new Terminal({
            cursorBlink: true,
            fontSize: 14,
            theme: { background: "#1e1e1e", foreground: "#f0f0f0" },
        });

        this.fitAddon = new FitAddon();
        this.terminal.loadAddon(this.fitAddon);
        this.socket = socket;
    }

    startListening() {
        this.terminal.onData((data) => {
            this.socket.emit("input", data);
        });

        this.socket.on("output", (data) => {
            this.terminal.write(data);
        });
    }

    attachTo(container) {
        this.terminal.open(container);
        this.fitAddon.fit();
        this.terminal.focus();
        this.terminal.write("Welcome to CyberShell\r\n$ ");
    }

    clear() {
        this.terminal.clear();
    }
}
