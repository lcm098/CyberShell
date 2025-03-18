import { TerminalUI } from "./TerminalUI.js";
import io from "https://cdn.socket.io/4.7.2/socket.io.esm.min.js"; // CDN

// Server connection
const serverAddress = "http://localhost:8080";
const socket = io(serverAddress);

// Update connection status
socket.on("connect", () => {
    document.getElementById("server-status").textContent = "Connected";
});
socket.on("disconnect", () => {
    document.getElementById("server-status").textContent = "Disconnected";
});

// Start the terminal UI
document.addEventListener("DOMContentLoaded", () => {
    const terminalContainer = document.getElementById("terminal-container");
    const terminal = new TerminalUI(socket);
    terminal.attachTo(terminalContainer);
    terminal.startListening();

    // Clear button
    document.getElementById("clear-btn").addEventListener("click", () => {
        terminal.clear();
    });

    // Maximize button
    document.getElementById("maximize-btn").addEventListener("click", () => {
        document.querySelector(".terminal-container").classList.toggle("maximized");
    });
});
