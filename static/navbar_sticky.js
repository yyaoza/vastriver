document.addEventListener('DOMContentLoaded', function() {
    // When the user scrolls the page, execute myFunction
    window.addEventListener('scroll', myFunction);
    //window.onscroll = function() {myFunction()};

    // Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
    function myFunction() {
        // Get the navbar
        var top_bar = document.getElementById("top_bar");
        var middle_bar = document.getElementById("middle_bar");
        var main_section = document.getElementById("main_section");

        // Get the offset position of the navbar
        var middle_sticky = $("#myCarousel").height()
      if (window.pageYOffset >= middle_sticky) {
        middle_bar.classList.add("stickyMiddle")
        middle_bar.style.top = "42px"
        middle_bar.style.position = "fixed"
//        main_section.style.position = "fixed"
        main_section.style.marginTop = "70px"
      } else {
        middle_bar.classList.remove("stickyMiddle");
        middle_bar.style.top = "42px"
        middle_bar.style.position = "unset"
        main_section.style.marginTop = "0px"
//        main_section.style.paddingTop = "0px"
//        main_section.style.position = "unset"
      }
    }
});
