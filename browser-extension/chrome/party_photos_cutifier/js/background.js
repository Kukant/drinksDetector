chrome.browserAction.onClicked.addListener(browserActionHandler);

chrome.extension.onConnect.addListener(messageRequestHandler);

function browserActionHandler(info, tab){
    chrome.tabs.executeScript({
        file: 'js/main.js'
    });
}

function messageRequestHandler(port) {
    if (port.name === "screenshot") {
        port.onMessage.addListener(function (msg) {
            if (msg.request === "take") {
                chrome.tabs.captureVisibleTab(null, {
                    format: "jpeg",
                    quality: 100
                }, function (img) {
                    port.postMessage(img);
                });
            }
        });
    }
}