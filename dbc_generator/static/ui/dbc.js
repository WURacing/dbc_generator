let form;

window.onload = function() {
    form = this.document.getElementById("submission-form");
}

function addPacket() {
    let packet = document.createElement("div");
    let packetName = textInput("MID");

    packet.appendChild(packetName);
    form.appendChild(packet);
}

function addSignal(parent) {
    let signal = document.createElement("div");
}

function textInput(name) {
    let input = document.createElement("input");
    input.type = "text";
    input.name = name;
    input.id = name;
    input.placeholder = name;
    return input;
}

function post() {
    vals = {
        hello: "world",
        goodbye: "moon"
    }
    fetch("upload", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(vals)
    }).then(response => response.text()).then(console.log);
}