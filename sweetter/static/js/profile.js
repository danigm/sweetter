$(document).ready(function() {
 $("#pw").keyup(function() {
     check_password($("#pw"), $("#pw2"));
 });
 $("#pw2").keyup(function() {
     check_password($("#pw"), $("#pw2"));
 });
});

function check_password(pw1, pw2){
    str1 = pw1.get(0).value;
    str2 = pw2.get(0).value;
    if (str1 != str2){
        $("#pw_info").html("passwords doesn't match");
        pw1.css("background", "#ff5555");
        pw2.css("background", "#ff5555");
    }
    else{
        $("#pw_info").html("");
        pw1.css("background", "#55ff55");
        pw2.css("background", "#55ff55");
    }
}
