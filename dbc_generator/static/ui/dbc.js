let schema;
let ecus = [];

window.onload = function() {
    fetch("/static/ui/schema.json")
    .then(response => response.json())
    .then(response => {
        schema = response.dbc;
        ecus = response.ecu;
        this.createFields(schema.file, "file", document.getElementById("fields"));
        let ecuSelect = this.document.getElementById("select-ecu");
        for(let ecu of ecus) {
            let option = this.document.createElement("option");
            option.text = ecu;
            option.value = ecu;
            ecuSelect.appendChild(option);
        }
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
 * @param {string} key
 * @param {HTMLDivElement} parentContainer 
 */
function createFields(fieldList, key, parentContainer) {
    let container = document.createElement("div");
    container.classList.add("container");
    container.name = key;
    let hasDeleteButton = key == "file";
    for(let field of fieldList) {
        if(field.ref == undefined) {
            // create text input field
            let defaultText = field.default != undefined ? field.default : "";
            let textField = textInput(field.name, field.display, defaultText);
            container.appendChild(textField);
        } else {
            let button = document.createElement("button");
            button.innerHTML = field.display;
            button.onclick = () => {
                createFields(schema[field.ref], field.ref, container);
            }
            container.appendChild(button);
            if(!hasDeleteButton) {
                addDeleteButton(container);
                hasDeleteButton = true;
            }
        }
    }
    if(!hasDeleteButton) {
        addDeleteButton(container);
        hasDeleteButton = true;
    }
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
    input.name = id;
    input.placeholder = placeholder;
    input.value = value;
    input.classList.add("text-input");
    return input;
}

/**
 * Sends data to the backend and downloads the file
 */
function post() {
    let selector = document.getElementById("select-ecu");
    let ecu = selector.options[selector.selectedIndex].value;
    if(ecu == "null") {
        alert("Please select a valid ECU.");
        return;
    }
    let data = {
        dbc: extractData(),
        ecu: ecu
    }
    fetch("upload", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    }).then(response => {
        if(!response.ok) {
            alert("Failed to compile DBC file");
            throw "Failed to compile DBC file";
        }
        return response.blob()
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
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
        container.name = key;
        let hasDeleteButton = key == "file";
        for(let field of schemaData) {
            if(field.ref == undefined) {
                // create text input field
                let defaultText = entry[field.name];
                let textField = textInput(field.name, field.display, defaultText);
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
                if(!hasDeleteButton) {
                    addDeleteButton(container);
                    hasDeleteButton = true;
                }
                importFields(entry[field.ref], field.ref, container);
            }
        }
        if(!hasDeleteButton) {
            addDeleteButton(container);
            hasDeleteButton = true;
        }
        parentContainer.appendChild(container);
    }
}

/**
 * Adds a delete button to the specified container
 * @param {HTMLDivElement} container 
 */
function addDeleteButton(container) {
    let deleteButton = document.createElement("button");
    deleteButton.classList.add("delete");
    deleteButton.innerHTML = "Delete";
    deleteButton.onclick = () => {
        container.remove();
    }
    container.appendChild(deleteButton);
}

/**
 * Extracts all of the user inputs from text fields
 */
function extractData() {
    let fields = document.getElementById("fields");
    return getDataFromContainer(fields);
}

/**
 * Extracts text field values recursively from a container div.
 * @param {HTMLDivElement} container 
 */
function getDataFromContainer(container) {
    let data = {};
    for(let element of container.children) {
        if(element instanceof HTMLDivElement) {
            if(!data[element.name]) {
                data[element.name] = [];
            }
            data[element.name].push(getDataFromContainer(element));
        } else if(element instanceof HTMLInputElement) {
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
        alert("Please select a valid DBC file to load.");
        return;
    }
    let response = await fetch("/parse", {
        method: "POST",
        body: url
    });
    let data = await response.json();
    let parentContainer = document.getElementById("fields");
    parentContainer.innerHTML = "";
    importFields(data.dbc.file, "file", parentContainer);
    document.getElementById("select-ecu").selectedIndex = ecus.indexOf(data.ecu) + 1;
}