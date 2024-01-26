$("#singleplayer").on("click", () => {
    window.postMessage({
        type: "click",
        payload: "singleplayer"
    })
})

$("#multiplayer").on("click", () => {
    window.close();
})

$("#realms").on("click", () => {
    window.close();
})

$("#options").on("click", () => {
    window.close();
})

$("#quit").on("click", () => {
    window.close();
})