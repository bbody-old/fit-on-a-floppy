'use strict';

var endpointURL = 'https://7udyio7rpg.execute-api.us-west-2.amazonaws.com/default/pageSize';
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

function toggleAlert(show) {
    var alert = document.getElementById('alert');
    alert.style.display = show ? 'block' : 'none';
}

function showError() {
    var errorMessage = 'Unfortunately we couldn\'t load that website, can you recheck your URL or try again?';
    toggleAlert(true);
    document.getElementById('alert').innerHTML = errorMessage;
    removeClass('loading');
}

function showResults(data) {
    data.moreThanOneFloppy = data.floppies === 1;
    var html = window.foaf.output(data);

    outputMessage(html);
}

function checkIfItWillFit(url, protocol) {
    toggleAlert(false);
    document.getElementById('output').innerHTML = '';
    document.getElementById('alert').innerHTML = '';
    removeClass('loaded');
    addClass('loading');

    var xhr = new XMLHttpRequest();
    xhr.open('POST', endpointURL);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status !== 200) {
            showError();
        } else {
            var json = JSON.parse(xhr.responseText);
            showResults(json);
            var https = protocol === "https";
            var newUrl = "?website=" + url + "&https=" + https;
            var title = "Fit on a Floppy - " + json.title;
            History.pushState({ website: url, https}, title, newUrl);
            document.title = title;
        }
    };
    xhr.onerror = showError;
    xhr.send(JSON.stringify({
        url,
        https: protocol === "https"
    }));
}

window.onSubmit = function (event) {
    event.preventDefault();

    checkIfItWillFit(event.currentTarget[1].value, event.currentTarget[0].value);
};


// Can't seem to set type="text" without it being stripped out by Nunjucks
document.getElementById('website').setAttribute('type', 'text');

var urlParams = new URLSearchParams(window.location.search);

if (urlParams.has('website') && urlParams.has('https')) {
    var website = urlParams.get('website');
    var protocol = urlParams.get('https') === "false" ? "http" : "https";
    document.getElementById('website').value = website;
    document.getElementById('protocol').value = protocol;
    checkIfItWillFit(website, protocol);
}