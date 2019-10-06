let form;
let schema;
let inputs = {};

window.onload = function() {
    form = this.document.getElementById("submission-form");
    fetch("/static/ui/schema.json")
    .then(response => response.json())
    .then(response => {
        schema = response;
        addFields(schema.packet, document.getElementById("fields"), "packet");
    });
}

function addFields(fields, parent, name) {
    let container = document.createElement("div");
    container.classList.add("container");
    let inputFields = [];
    for(let field of fields) {
        if(field.ref == undefined) {
            let defaultText = field.default != undefined ? field.default : "";
            let textField = textInput(field.name, field.display, defaultText);
            inputFields.push(textField);
            container.appendChild(textField);
        } else {
            let button = document.createElement("button");
            button.innerHTML = field.display;
            let subcontainer = document.createElement("div");
            button.onclick = () => {
                addFields(schema[field.ref], subcontainer, field.ref);
            }
            container.appendChild(button);
            container.appendChild(subcontainer);
        }
    }
    if(!inputs[name]) {
        inputs[name] = [];
    }
    inputs[name].push(inputFields);
    parent.appendChild(container);
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

    for(key of Object.keys(inputs)) {
        for(input of inputs[key]) {
            // TODO: collect inputs into JSON object
        }
    }

    fetch("upload", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(vals)
    }).then(response => response.text()).then(console.log);
}