const { ipcRenderer } = require("electron");

process.once("loaded", () => {
    window.addEventListener("message", event => {
        const message = event.data;
        ipcRenderer.send("custom-message", message)
    });
});