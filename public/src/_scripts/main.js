'use strict';

var addHelpers = require('../_templates/helpers.js');

addHelpers(Handlebars);

var ids = ['outputRow','inputRow'];

function addClass(className) {
    for (var i = 0; i < ids.length; i++) {
        document.getElementById(ids[i]).classList.add(className);
    }
}

function removeClass(className) {
    for (var i = 0; i < ids.length; i++) {
        document.getElementById(ids[i]).classList.remove(className);
    }
}

function outputMessage(html) {
    document.getElementById('output').innerHTML = html;
    
    removeClass('loading');
    addClass('loaded');
}

function showError() {
    var html = window.foaf.error();
    
    outputMessage(html);
}

function showResults(data) {
    data.moreThanOneFloppy = data.floppies === 1;
    var html = window.foaf.output(data);

    outputMessage(html);
}


window.onSubmit = function (event) {
    event.preventDefault();
    document.getElementById('output').innerHTML = '';
    removeClass('loaded');
    addClass('loading');
    
    var endpointURL = 'https://7udyio7rpg.execute-api.us-west-2.amazonaws.com/default/pageSize';
    var url = event.currentTarget[0].value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', endpointURL);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status !== 200) {
            showError();
        } else {
            var json = JSON.parse(xhr.responseText);
            showResults(json);
        }
    };
    xhr.onerror = showError;
    xhr.send(JSON.stringify({
        url
    }));
}

