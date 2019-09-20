// Main javascript entry point
// Should handle bootstrapping/starting application

'use strict';

import $ from 'jquery';
var addHelpers = require('../_templates/helpers.js'); 

window.onSubmit = function(event) {
  event.preventDefault();
  
  var protocol = event.currentTarget[0].value;
  var url = event.currentTarget[1].value;
  url = url.replace('https://', '');
  url = url.replace('http://', '');

  $.ajax({                     
      type: "POST",                     
      url: 'https://7udyio7rpg.execute-api.us-west-2.amazonaws.com/default/pageSize',
      contentType: 'application/json',      
      data: JSON.stringify({
          url,
          protocol                
      }),                     
      success: function(res){
          var html = window.foaf.output(res);
          $('#output').html(html);
          $('#outputRow').show();
      },
      error: function(error){
        var html = window.foaf.error();
        $('#output').html(html);
        $('#outputRow').show();
      }
  }); 
}

addHelpers(Handlebars);