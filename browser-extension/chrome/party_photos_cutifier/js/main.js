var screenshotPort = chrome.extension.connect({ name: "screenshot" });
var popupPort = chrome.extension.connect({ name: "popup" });
var img;

screenshotPort.postMessage({ request: "take" });


screenshotPort.onMessage.addListener(function (msg) {
    img = document.createElement('img');
    img.src = msg;
    popupPort.postMessage({ request: "open", data: msg });
});

popupPort.onMessage.addListener(function (win) {
    popupPort.postMessage({ request: "update", tabId: win.tabs[0].id });
    //chrome.tabs.sendMessage(popups, {}, appendImage);
    // win.addEventListener('load', loadEvent => {
    //     let window = loadEvent.currentTarget;
    //     window.console.log("test");
    //     window.document.getElementById('img-wrapper').appendChild(img);
    // });
});