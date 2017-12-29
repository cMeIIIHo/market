$( document ).ready(function() {

    // ---------------------------------------------------------------------------------------------
    // from: https://docs.djangoproject.com/en/dev/ref/csrf/
    // Acquiring the token is straightforward:
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }                                                                               // AJAX SETUP
    var csrftoken = getCookie('csrftoken');

    // from: https://docs.djangoproject.com/en/dev/ref/csrf/
    // Finally, you’ll have to actually set the header on your AJAX request
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    // ---------------------------------------------------------------------------------------

    // checks if chosen delivery method is 'pickup point', and if it is - disables address textinput
    var radio = $('input[name = "pickup_point"]:checked');
    if (radio.prop('checked')) {
        var address_input = $('#id_address');
        address_input.val('').prop('disabled', true);
    }

    // removes item from the cart
    function remove_item_from_the_cart(order_id, item_id, del_url) {
        $.ajax({
            type: 'POST',
            url: del_url,
            dataType: 'json',
            data: {'order_id': order_id, 'item_id': item_id}
        });
    };

    // sets a 'onclick' event on every DELETE_ITEM_FROM_THE_CART button
    $('.order_item_line').each(function(index, item) {
        var ItemDelButton = $(item).find('.order_item_line-del_button');
        var ItemDelCheckbox = $(item).find('input[type = checkbox][id $= DELETE]');
        ItemDelButton.on('click', function() {
            $(item).css('display', 'none');
            ItemDelCheckbox.prop('checked', true);
            var order_id = $(item).attr('data-order_id');
            var item_id = $(item).attr('data-item_id');
            var del_url = ItemDelButton.attr('data-item_del_url');
            remove_item_from_the_cart(order_id, item_id, del_url);
        });
    });




//    (function() {
//        'use strict';
//        $('.order_item_line').each(function(index, item) {
//            var deleteOrderItemButton = $(item).find('.order_item_line-del_button');
//            deleteOrderItemButton.on('click', function() {
//                'use strict';
//                $(item).css('display', 'none');
//            });
//        });
//    }());






//    (function() {
//        'use strict';
//        $('[id ^= order_item_]').each(function(index, element) {
//            console.log(element);
//            var snackbarContainer = $(element).parent().find('.mdl-js-snackbar');
//            var showSnackbarButton = $(element).find('.mdl-js-button');
//            var deletion_mark = $(element).find('input[data-input_for_removing = yes]');    // this input gonna get NAME if item is removed
//            var handler = function(event) {
//            $(element).css('display', 'initial');
//            deletion_mark.removeAttr('name');                                               // input loses NAME cuz item is back
//            };
//            console.log(element);
//            showSnackbarButton.on('click', function() {
//                'use strict';
//                $(element).css('display', 'none');
//                deletion_mark.attr('name', 'remove');                                       // input gets name cuz item is removed
//                var data = {
//                  message: 'Товар удален из корзины',
//                  timeout: 5000,
//                  actionHandler: handler,
//                  actionText: 'Вернуть'
//                };
//                snackbarContainer[0].MaterialSnackbar.showSnackbar(data);
//            });
//            console.log(element);
//        });
//    }());
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