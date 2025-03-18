const http = require("http");
const express = require("express");
const { Server } = require("socket.io");
const pty = require("node-pty");
const path = require("path")

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

// Serve frontend files
app.use(express.static("public"));
const baseDir = path.resolve(__dirname, "..")

io.on("connection", (socket) => {
  console.log("Client connected");
  

  // Create a new terminal session
  const shell = pty.spawn("sudo", [path.join(baseDir, "output", "main")], {
    name: "xterm-color",
    cols: 80,
    rows: 30,
    cwd: process.env.HOME,
    env: process.env,
  });

  // Send terminal output to client
  shell.on("data", (data) => {
    socket.emit("output", data);
  });

  // Receive user input and write to shell
  socket.on("input", (data) => {
    shell.write(data);
  });

  // Resize terminal
  socket.on("resize", (cols, rows) => {
    shell.resize(cols, rows);
  });

  socket.on("disconnect", () => {
    console.log("Client disconnected");
    shell.kill();
  });
});

const PORT = 8080;
server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});