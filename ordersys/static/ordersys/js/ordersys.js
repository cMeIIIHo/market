$( document ).ready(function() {

    var radio = $('input[name = "pickup_point"]:checked');
    if (radio.prop('checked')) {
        var address_input = $('#id_address');
        address_input.val('').prop('disabled', true);
    }

    (function() {
        'use strict';
        $('[id ^= order_item_]').each(function(index, element) {
            console.log(element);
            var snackbarContainer = $(element).parent().find('.mdl-js-snackbar');
            var showSnackbarButton = $(element).find('.mdl-js-button');
            var handler = function(event) {
            $(element).css('display', 'initial');
            };
            console.log(element);
            showSnackbarButton.on('click', function() {
                'use strict';
                $(element).css('display', 'none');
                var data = {
                  message: 'Товар удален из корзины',
                  timeout: 5000,
                  actionHandler: handler,
                  actionText: 'Вернуть'
                };
                snackbarContainer[0].MaterialSnackbar.showSnackbar(data);
            });
            console.log(element);
        });
    }());
});



function turn_off_express_delivery_checkbox() {
    var checkbox = $('#id_express_delivery:checked');
    var label = $('label[for = id_express_delivery]');
    checkbox.prop('checked', false);
    label.removeClass('is-checked');
    var address_input = $('#id_address');
    address_input.val('').prop('disabled', true);
}

function turn_off_pickup_point_radio() {
    var radio = $('input[name = "pickup_point"]:checked');
    var radio_id = radio.prop('id');
    var label = $('label[for = ' + radio_id + ']');
    radio.prop('checked', false);
    label.removeClass('is-checked');
    var address_input = $('#id_address');
    address_input.val('').prop('disabled', false);
}