// Main javascript entry point
// Should handle bootstrapping/starting application

'use strict';

import $ from 'jquery';
var addHelpers = require('../_templates/helpers.js'); 
addHelpers(Handlebars);

window.onSubmit = function(event) {
  event.preventDefault();
  var query = '#outputRow,#inputRow';
  var url = event.currentTarget[0].value;
  $(query).addClass('loading');
  $.ajax({                     
      type: "POST",                     
      url: 'https://7udyio7rpg.execute-api.us-west-2.amazonaws.com/default/pageSize',
      contentType: 'application/json',      
      data: JSON.stringify({
          url
      }),                     
      success: function(res){
          var html = window.foaf.output(res);
          $('#output').html(html);
          $(query).removeClass('loading').addClass('loaded');
      },
      error: function(error){
        var html = window.foaf.error();
        $('#output').html(html);
        $(query).removeClass('loading').addClass('loaded');
      }
  }); 
}

