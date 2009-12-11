var timeout = 41;

$(document).ready(function() {
 $("#text").keyup(function() {
     var input = $("#text")[0].value;
     var max = $("#hc")[0].innerHTML;
     updateStatusTextCharCounter(input, max);
 });

 $("#post_button").click(function(){
    text = $("#text").get(0).value;
    $("#text").attr('disabled', 'disabled');
    $("#post_button").attr('disabled', 'disabled');
    loading(true);
    $.post("/sweetter/status/new", { text: text },
      function(data){
        refresh();
        $("#post_button").removeAttr('disabled');
        $("#text").removeAttr('disabled');
        $("#text")[0].value = "";
      }); 

    return false;
 });

 shover();
});

function loading(bool){
    if (bool)
        $("#refresh_img").css("display", "block");
    else
        $("#refresh_img").css("display", "none");
}

function refresh(){
    id = $(".sweet:first").attr("id");
    if (!id){
        id = 0;
    }
    page = $("#pagenumber").html();
    refresh_uri = $("#refresh_uri").html().trim();
    loading(true);
    $.get(refresh_uri+"/"+id+"/"+page, function(data){
        $("#sweets").prepend(data);
        sweet = $(".sweet:first");
        while(sweet.attr('id') > id){
            sweet.hide();
            sweet.fadeIn("slow");
            sweet.addClass("new");
            sweet = sweet.next();
        }

        loading(false);
        shover();
    });
}

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

function shover(){
 $(".sweet").hover(function(){
        $(this).css("background-color", "#ffffff");
        $(this).find(".tools").show();
    },
    function(){
        $(this).css("background-color", "transparent");
        $(this).find(".tools").hide();
 });
 mytime = setTimeout("refresh()", timeout*1000); 
 }
