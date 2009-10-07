$(document).ready(function() {
 $("#text").keyup(function() {
     var input = $("#text")[0].value;
     var max = $("#hc")[0].innerHTML;
     updateStatusTextCharCounter(input, max);
 });

 $(".sweet").hover(function(){
        $(this).css("background-color", "#ffffff");
        $(this).find(".tools").show();
    },
    function(){
        $(this).css("background-color", "transparent");
        $(this).find(".tools").fadeOut();
 });
});

function updateStatusTextCharCounter(value, max) {
    len = value.length;
    res = max - len;
    jQuery('#counter').html('' + res);
    if (len > max) {
        if (jQuery("#new").attr('disabled') != 'disabled') {
            jQuery('#new').attr('disabled', 'disabled');
        }   
    } else {
        if (jQuery("#new").attr('disabled') == true) {
            jQuery('#new').removeAttr('disabled');
        }   

        if (res > 10) {
            jQuery('#counter').css('color', '#999' );
        } else if (res > 5) {
            jQuery('#counter').css('color', '#940000' );
        } else {
            jQuery('#counter').css('color', '#f00' );
        }   
    }   
}

