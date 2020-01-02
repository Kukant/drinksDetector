chrome.browserAction.onClicked.addListener(browserActionHandler);

chrome.extension.onConnect.addListener(messageRequestHandler);

function browserActionHandler(info, tab) {
    chrome.tabs.executeScript({ file: 'js/main.js' });
}

function messageRequestHandler(port) {
    if (port.name === "screenshot") {
        port.onMessage.addListener(function (msg) {
            if (msg.request === "take") {
                chrome.tabs.captureVisibleTab(null, {
                    format: "jpeg",
                    quality: 100
                }, function (img) {
                    // Defining Upsamplelike class does not work as when implemented according to github
                    // the extension throws the class loaded does not have static className property, but it does.
                    // tf.serialization.registerClass("UpsampleLike");
                    // let model = tf.loadLayersModel('https://raw.githubusercontent.com/Kukant/drinksDetector/chrome-extension/browser-extension/chrome/party_photos_cutifier/js-model/model.json').then(
                    //     () => {
                    //         // todo: process the photo via model...
                    //
                    //         port.postMessage({ img: img });
                    //     }
                    // );
                    // todo: delete after processing works
                    port.postMessage({ img: img });
                });
            }
        });
    }
}