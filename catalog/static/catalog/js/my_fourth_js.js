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

    // product_page price uploading ajax function



    // page loaded - ajax been sent
    var foo = {};
    var form = $('.js-choosable').closest("form");
    foo['product_id'] = form.attr('product_id');
    $('.js-choosable').each(function(i, l){
        foo[$(l).attr('name')]=$(l).val();
        console.log(foo[i]);
    });
    // ajax request (post)
    $.ajax({
        url: form.attr("product_page_price-url"),
        type: 'post',
        data: foo,
        dataType: 'json',
        success: function(data){
                if (data.price) {
                    $("#price").text(data.price);
                    $("#price").addClass('with_currency');
                    }
                if (data.error_message) {
                    $("#price").text(data.error_message);
                    $("#price").removeClass('with_currency');
                    }
            }
    })

    // event for choosable options
    $('.js-choosable').change(function(){
        var foo = {};
        var form = $(this).closest("form");
        foo['product_id'] = form.attr('product_id');
        $('.js-choosable').each(function(i, l){
            foo[$(l).attr('name')]=$(l).val();
            console.log(foo[i]);
        });
        // ajax request (post)
        $.ajax({
            url: form.attr("product_page_price-url"),
            type: 'post',
            data: foo,
            dataType: 'json',
            success: function(data){
                if (data.price) {
                    $("#price").text(data.price);
                    $("#price").addClass('with_currency');
                    }
                if (data.error_message) {
                    $("#price").text(data.error_message);
                    $("#price").removeClass('with_currency');
                    }
            }
        })
    });
});