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

  }); // end of document ready
})(jQuery); // end of jQuery name space
$( window ).resize(function() {
          var window_width = $(window).width();
          if (window_width<=434){
                  $('.brand-logo').css('font-size','15pt');
                }
          else{
              $('.brand-logo').css('font-size','31.5px');
          }
});