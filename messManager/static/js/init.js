(function($){
  $(function(){

    $('.button-collapse').sideNav({
      menuWidth: 228 // Default is 240
    });
     $('.parallax').parallax();
     $('.modal-trigger').leanModal();
     $(".dropdown-button").dropdown( {});
      var window_width = $(window).width();
          if (window_width<434){
                  $('.brand-logo').css('font-size','15pt');
                }
          else{
              $('.brand-logo').css('font-size','31.5px');
          }
      $("#login_info_div").hide();

  }); // end of document ready
})(jQuery); // end of jQuery name space
$( window ).resize(function() {
          var window_width = $(window).width();
          if (window_width<=500){
                  $('.brand-logo').css('font-size','14pt');
                }
          else{
              $('.brand-logo').css('font-size','31.5px');
          }

});
function show_login_div(element, type)
{
	var offset = $( element ).offset();
	var height = $(element).height();
	var top_position = offset.top+height;
    var adj = 2;
    if($(window).width()<600){
        top_position = 48;
        adj = 0;
    }
    if(type==1){
        right = 237;
    }
    else{
        right = offset.top-adj
    }
	if ($('#login_info_div').css('display') == 'none') {
	 $("#login_info_div" ).css({ top:top_position+3, right: right });
	 $("#login_info_div").show();
	 }
	 else
	 {
	   $("#login_info_div").hide();
	 }
}
$(window).click(function(){
    console.log('das');
});