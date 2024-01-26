const { app, ipcMain, BrowserWindow } = require("electron");

const createWindow = () => {
    const window = new BrowserWindow({
        width: 854,
        height: process.platform !== "darwin" ? 480 : 508,
        backgroundColor: "#000000",
        icon: "resources/icons/icon.png",
        show: false,
        webPreferences: {
            preload: "src/preload.js",
            nodeIntegration: false,
            enableRemoteModule: false,
            contextIsolation: true,
            sandbox: true
        }
    })

    window.loadFile("src/html/index.html");

    window.once("ready-to-show", () => {
        window.show();
    });
}

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit();
    }
})

app.on("ready", () => {
    createWindow();
    
    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    })

    ipcMain.on("custom-message", (event, message) => {
        console.log("IPC message: ", event, message);
    })
})