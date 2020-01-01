var loaded = (loaded === true);
var screenshotPort = chrome.extension.connect({name: "screenshot"});

if (!loaded) {
    loadModel().then(() => {
        console.log("loaded");
    });
    loaded = true;
}

screenshotPort.postMessage({request: "take"});

screenshotPort.onMessage.addListener(function (msg) {
    let cuteImg = cutify(msg);

    let modal = document.createElement('div');
    modal.id = 'ppc-result';
    modal.style = `
        display: block; 
        position: fixed; 
        top: 0; 
        left: 0; 
        width: 100%;
        height: 100%;
        z-index: 10000;
        background-repeat: no-repeat;
        background-size: cover;
        background-image: url(`+ cuteImg +`)`;

    let close = document.createElement('div');
    close.style = `
        position: fixed;
        top: 10px; 
        left: calc(100% - 55px); 
        width: 45px; 
        height: 45px; 
        font-size: 35px; 
        cursor: pointer; 
        color: dimgray;
        text-align: center;
        user-select: none;`;
    close.innerText = 'X';
    close.onclick = (e) => {
        e.target.parentElement.remove();
        screenshotPort.disconnect();
        screenshotPort = undefined;
    };

    modal.appendChild(close);
    document.body.appendChild(modal);
});

async function loadModel() {
    //model = await tf.loadLayersModel('');
}

function cutify(img) {
    // Do some magic stuff with the image there


    return img;
}