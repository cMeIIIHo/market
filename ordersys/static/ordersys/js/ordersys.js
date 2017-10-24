$( document ).ready(function() {

});

function turn_off_express_delivery_checkbox() {
    var checkbox = $('#id_express_delivery');
    if (checkbox.is(':checked')) {
        checkbox.prop('checked', false);
    }
}