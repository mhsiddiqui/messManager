(function($){
  $(function(){

    $('.button-collapse').sideNav({
      menuWidth: 240 // Default is 240
    });
     $('.parallax').parallax();
     $('.modal-trigger').leanModal();
     $(".dropdown-button").dropdown( {});
     var top_man_height = $('#nav-bar-wrap').height();
     $('#nav-mobile').css('margin-top',top_man_height);

  }); // end of document ready
})(jQuery); // end of jQuery name space
$( window ).resize(function() {
          var top_man_height = $('#nav-bar-wrap').height();
          $('#nav-mobile').css('margin-top',top_man_height);
});