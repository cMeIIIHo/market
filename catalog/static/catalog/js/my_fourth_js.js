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

    // event for choosable options
    $('.js-choosable').change(function(){
        var foo = {};
        var form = $(this).closest("form");
        $('.js-choosable').each(function(i, l){
            foo[i]=$(l).val();
            console.log(foo[i]);
        });
        // ajax request (post)
        $.ajax({
            url: form.attr("product_page_price-url"),
            type: 'post',
            data: foo,
            dataType: 'json',
            success: function(data){
                $("#price").text(data.price);
            }
        })
    });
});