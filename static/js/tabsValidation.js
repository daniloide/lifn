$(document).ready(function(){
    var str = "";
    var formVals = $("form:visible td.w2p_fw");
    formVals.each(function(index) {
        if ($(this).find("select").is('select')){
            str += $(this).find("select").val();
        } else if ($(this).find("input").is('input')){
            if($(this).find("input").attr('type') == "checkbox"){
                var isChecked = $(this).find("input").attr("checked");
                if (isChecked){
                    str += "Checked";            
                } else {
                    str += "UnChecked";
                }
            } else {
                str += $(this).find("input").val();
            }
        } else if ($(this).find("textarea").is("textarea")){
            str += $(this).find("textarea").val();
        }
    });
    $(".modified").html(str);
})