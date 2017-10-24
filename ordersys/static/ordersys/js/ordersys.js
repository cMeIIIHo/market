$( document ).ready(function() {

});

function turn_off_express_delivery_checkbox() {
    var checkbox = $('#id_express_delivery');
    if (checkbox.is(':checked')) {
        checkbox.prop('checked', false);
    }
}

function turn_off_pickup_point_radio() {
    var radio = $('input[name = "pickup_point"]:checked');
    var radio_id = radio.prop('id');
    var label = $('label[for = ' + radio_id + ']');
    radio.prop('checked', false);
    label.removeClass('is-checked');
}