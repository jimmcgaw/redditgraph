var Predilection = Predilection || {};

// the magical code for this comes from: http://dygraphs.com/

Predilection.activateButtonSwap = function(){
  var form = jQuery("form");
  form.submit(function(e){
    var submit_input = jQuery("#submit");
    var loading_div = jQuery("#loading");
    submit_input.toggleClass("hidden");
    loading_div.toggleClass("hidden");
  });
  
};

jQuery(document).ready(function(){
  Predilection.activateButtonSwap();
});