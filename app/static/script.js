$(document).on("click", ".go_to_top", function(e) {
    e.preventDefault();
    $('body, html').animate({scrollTop: 0}, 800);
});