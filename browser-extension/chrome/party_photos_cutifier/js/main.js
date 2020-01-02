var screenshotPort = chrome.extension.connect({name: "screenshot"});

screenshotPort.postMessage({request: "take"});

screenshotPort.onMessage.addListener(function (msg) {
    // To hide scrollbar
    let formerStyle = document.body.style;
    document.body.style.height = '100%';
    document.body.style.overflowY = 'hidden';

    let modal = document.createElement('div');
    modal.id = 'ppc-result';
    modal.style = `
        display: block; 
        position: fixed; 
        top: 0; 
        left: 0; 
        width: 100%;
        height: 100%;
        z-index: 10000;`;
    // todo: Use result from tensorflowjs as background-image to fit the screen better
    // background-repeat: no-repeat;
    // background-size: cover;
    // background-image: url(`+ msg.img +`)`;


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
        document.body.style = formerStyle;
        screenshotPort.disconnect();
        screenshotPort = undefined;
    };

    let img = document.createElement('img');
    img.src = msg.img;
    img.style = `
        height: 100%;
        width: 100%;`;

    let clip = document.createElement('textarea');
    clip.value = msg.img;
    clip.setAttribute('readonly', '');

    modal.appendChild(clip);
    modal.appendChild(close);
    modal.appendChild(img);
    document.body.appendChild(modal);

    clip.select();
    document.execCommand('copy');
    clip.remove();

    setTimeout(() => {
        window.alert("Raw image has been copied to the clipboard")
    }, 100);
});