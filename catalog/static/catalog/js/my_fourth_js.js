$( document ).ready(function() {
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
}
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

// product_page price uploading ajax function + it enables/disables cart_button element + adds spec_prod_id form's attr

function get_price() {
    var foo = {};
    var form = $('.js-choosable').closest("form");
    foo['product_id'] = form.attr('data-product_id');
    $('.js-choosable').each(function(i, l){
        foo[$(l).attr('name')]=$(l).val();
    });
    // ajax request (post)
    $.ajax({
        url: form.attr("data-product_page_price-url"),
        type: 'post',
        data: foo,
        dataType: 'json',
        success: function(data){
                if (data.price) {
                    $("#price").text(data.price);
                    $("#price").addClass('with_currency');
                    $('#cart_button').removeAttr('disabled');
                    form.attr('data-spec_prod_id', data.spec_prod_id);
                    }
                if (data.error_message) {
                    $("#price").text(data.error_message);
                    $("#price").removeClass('with_currency');
                    $('#cart_button').attr('disabled', 'disabled');
                    form.removeAttr('data-spec_prod_id')
                    }
            }
    })
}

// page loaded - get price

get_price();

// event for changing choosable options
$('.js-choosable').change(get_price);

// product_page modal winow's appearance

function show_modal_window() {
    $('.blocker').css('display', 'block');
    $('.modal_window').css('display', 'flex');
}

// product page hiding modal window function

function hide_modal_window() {
    $('.blocker').css('display', 'none');
    $('.modal_window').css('display', 'none')
}

// product page add to the cart ajax function
function add_sp_to_cart() {
    $.ajax ({
        url: $('#cart_button').attr('data-url-add_sp_to_cart'),
        type: 'post',
        data: {'sp_id': $('#sp_selection_form').attr('data-spec_prod_id'),
               'sp_quantity': $('#amount').val()},
        dataType: 'json',
    })
}


// changes text and adds animation of CART_LINK if u add goods to the cart
function change_cart_link_appearance() {
    $('#empty_cart_link').addClass('my-cart_link-animated').text('В корзину')
}

// show modal window if u click cart button on product page + add spec_prod_id to user's session

$('#cart_button').click(function() {
    add_sp_to_cart();
    show_modal_window();
    change_cart_link_appearance();
});

$('#keep_shopping').click(hide_modal_window);



});