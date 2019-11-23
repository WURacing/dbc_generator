let schema;
let inputs = [];

window.onload = function() {
    fetch("/static/ui/schema.json")
    .then(response => response.json())
    .then(response => {
        schema = response;
        this.createFields(schema.file, "file", inputs, document.getElementById("fields"));
    });

    fetch("/dbcs")
    .then(response => response.json())
    .then(response => {
        let select = this.document.getElementById("select-dbc");
        for(let file of response) {
            let option = document.createElement("option");
            option.text = file.name;
            option.value = file.download;
            select.appendChild(option);
        }
    });
}

/**
 * Creates the fields for the schema object
 * @param {Object} fieldList 
 * @param {HTMLInputElement[]} inputList 
 * @param {HTMLDivElement} parentContainer 
 */
function createFields(fieldList, key, inputList, parentContainer) {
    let container = document.createElement("div");
    container.classList.add("container");
    container.id = key;
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
                createFields(schema[field.ref], field.ref, subInputs, container);
                inputFields.push(subInputs[0]);
            }
            container.appendChild(button);
        }
    }
    let deleteButton = document.createElement("button");
    deleteButton.classList.add("delete");
    deleteButton.innerHTML = "Delete";
    deleteButton.onclick = () => {
        container.remove();
    }
    container.appendChild(deleteButton);
    inputList.push(inputFields);
    parentContainer.appendChild(container);
}
/**
 * Creates a text input field
 * @param {string} id
 * @param {string} placeholder 
 * @param {string?} value 
 * @returns The text field DOM element
 */
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

/**
 * Sends data to the backend
 */
function post() {
    let data = extractData();
    fetch("upload", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    }).then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
        // the filename you want
        a.download = "file.dbc";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    });
}

/**
 * Imports data into fields from a JSON response
 * @param {Object} data 
 * @param {string} key 
 * @param {HTMLDivElement} parentContainer 
 */
function importFields(data, key, parentContainer) {
    let schemaData = schema[key];

    for(let entry of data) {
        let container = document.createElement("div");
        container.classList.add("container");
        container.id = key;

        for(let field of schemaData) {
            if(field.ref == undefined) {
                // create text input field
                let defaultText = entry[field.name];
                let textField = textInput(field.name, field.display, defaultText);
                // inputFields.push(textField);
                container.appendChild(textField);
            } else {
                let button = document.createElement("button");
                button.innerHTML = field.display;
                button.onclick = () => {
                    let subInputs = [];
                    createFields(schema[field.ref], field.ref, subInputs, container);
                    subInputs.push(subInputs[0]);
                }
                container.appendChild(button);
                importFields(entry[field.ref], field.ref, container);
            }
        }
        let deleteButton = document.createElement("button");
        deleteButton.classList.add("delete");
        deleteButton.innerHTML = "Delete";
        deleteButton.onclick = () => {
            container.remove();
        }
        container.appendChild(deleteButton);
        parentContainer.appendChild(container);
    }
}

function extractData() {
    let fields = document.getElementById("fields");
    return getDataFromContainer(fields);
}

function getDataFromContainer(container) {
    let data = {};
    for(let element of container.children) {
        if(element instanceof HTMLDivElement) {
            if(!data[element.id]) {
                data[element.id] = [];
            }
            data[element.id].push(getDataFromContainer(element));
        } else if(element instanceof HTMLInputElement) {
            // console.log(element.name)
            data[element.name] = element.value;
        }
    }
    return data;
}

/**
 * Loads the selected DBC file from github
 */
async function loadSelectedFile() {
    let selector = document.getElementById("select-dbc");
    let url = selector.options[selector.selectedIndex].value;
    if(url == "null") {
        return;
    }
    console.log(url);
    let response = await fetch("/parse", {
        method: "POST",
        body: url
    });
    let data = await response.json();
    let parentContainer = document.getElementById("fields");
    parentContainer.innerHTML = "";
    importFields(data.file, "file", parentContainer);
}