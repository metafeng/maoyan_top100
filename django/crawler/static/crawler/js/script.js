$(document).ready(function () {
    var navHeight = $("nav").height();
    $("nav li").show();
    $(".dropdown").hide();
    $(window).scroll(function () {
        // if scrolled a greater amount then the initial height of the nav..
        if ($(document).scrollTop() > navHeight) {
            //shrink icon
            $(".logo").addClass("logoShrink");
            //shrink nav
            $("nav").addClass("navShrink");
            // keep the links centered in the nav
            $("nav li").addClass("keepCenter");
            // move the dropdown up so it is still on the lower edge of the nav
            $(".dropdown").css("top", "69px"); //equal to nav height-1

        } else {
            // otherwise if no scroll or scroll back up take off the settings
            $(".logo").removeClass("logoShrink");
            $("nav").removeClass("navShrink");
            $("nav li").removeClass("keepCenter");
            $(".dropdown").css("top", "99px");//equal to nav height
        }
    });
});
//end document ready