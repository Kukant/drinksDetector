chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
    console.log("TEST");
    if (msg.request === "update") {
        var img = document.createElement('img');
        img.src = "1234";
        document.getElementById('img-wrapper').appendChild(img);
    }
});