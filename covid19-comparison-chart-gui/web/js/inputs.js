// Add new input if needed
//   On change last input add another one
//       If there is one empty, don't add
//       Remove empty inputs if more than 1 is empty

////////////
//// Variables declaration

let mainDiv = document.getElementById('countries');
let alignButton = document.getElementById('align');
let acDivs;
let inputs;
let lastInput;


////////////
//// Function Definitions

function _refresh() {
    acDivs = document.getElementsByClassName('autocomplete');
    inputs = document.getElementsByClassName('input');
}

function _getNumberOfEmpty() {
    let count = 0;
    for(let i = 0; i < inputs.length; ++i)
        if (inputs[i].value == '' || inputs[i].value == null)
            count += 1;
    return count;
}

function onInputFunction(e) {
    let count = _getNumberOfEmpty();

    if(count < 1) {
        node = acDivs[0].cloneNode(true);
        node.lastElementChild.value = '';

        mainDiv.appendChild(node);
        _refresh();

        lastInput = inputs[inputs.length-1];
        lastInput.oninput = onInputFunction;
        addAutocomplete();
    }
    removeUnnecessary();
}

function removeUnnecessary() {
    let count = _getNumberOfEmpty();
    
    if(count > 1) {
        for(let i = 0; i < inputs.length; ++i)
            if(inputs[i].value == '' || inputs[i].value == null)
                if (!(inputs[i] === document.activeElement))
                    inputs[i].parentNode.remove();

        _refresh();
        addAutocomplete();
    }
}

function getCountries() {
    _refresh();
    let values = [];

    for(let i = 0; i < inputs.length; ++i)
        if (inputs[i].value != '' && inputs[i].value != null)
            values.push(inputs[i].value);

    values = values.filter( (item, index) => values.indexOf(item) === index);
    return values;
}

function toggleAlign() {
    s = document.getElementById('start-from');
    d = document.getElementById('days-limit');
    if(alignButton.checked){
        s.removeAttribute('disabled', 'false');
        d.removeAttribute('disabled', 'false');
        s.parentNode.style = 'filter: opacity(1);'
        d.parentNode.style = 'filter: opacity(1);'
    } else {
        s.setAttribute('disabled', 'true');
        d.setAttribute('disabled', 'true');
        s.parentNode.style = 'filter: opacity(0.5);'
        d.parentNode.style = 'filter: opacity(0.5);'
    }
}

////////////
//// Script

// _refresh assigns acDivs and inputs
_refresh();
lastInput = inputs[inputs.length-1];
lastInput.oninput = onInputFunction;
alignButton.oninput = toggleAlign;
toggleAlign();

