let form;
let schema;
let inputs = [];

window.onload = function() {
    form = this.document.getElementById("submission-form");
    fetch("/static/ui/schema.json")
    .then(response => response.json())
    .then(response => {
        schema = response;
        this.createFields(schema.file, inputs, document.getElementById("fields"));
        
    });
}

function createFields(fieldList, inputList, parentContainer) {
    let container = document.createElement("div");
    container.classList.add("container");
    let inputFields = [];
    for(let field of fieldList) {
        if(field.ref == undefined) {
            // create text input field
            let defaultText = field.default != undefined ? field.default : "";
            let textField = textInput(field.name, field.display, defaultText);
            inputFields.push(textField);
            container.appendChild(textField);
        } else {
            let button = document.createElement("button");
            button.innerHTML = field.display;
            button.onclick = () => {
                let subInputs = [];
                createFields(schema[field.ref], subInputs, container);
                // if(inputList[field.ref] == undefined) {
                //     inputList[field.ref] = [];
                // }
                inputFields.push(subInputs[0]);
                // inputList[field.ref].push(subInputs);
            }
            container.appendChild(button);
        }
    }
    inputList.push(inputFields);
    
    parentContainer.appendChild(container);

}

function textInput(id, placeholder, value = "") {
    let input = document.createElement("input");
    input.type = "text";
    input.name = id;
    input.id = id;
    input.placeholder = placeholder;
    input.value = value;
    input.classList.add("text-input");
    return input;
}

function post() {
    let data = {file: []};
    for(let packet of inputs[0]) {
        let packetData = {signals: []};
        for(let value of packet) {
            if(value instanceof Array) {
                let signalData = {};
                for(let j = 0; j < schema.signal.length; j++) {
                    signalData[schema.signal[j].name] = value[j].value;
                }
                packetData.signals.push(signalData);
            } else {
                packetData[value.name] = value.value;
            }
        }
        data.file.push(packetData);
    }

    console.log(data);

    fetch("upload", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    }).then(response => response.text()).then(console.log);
}