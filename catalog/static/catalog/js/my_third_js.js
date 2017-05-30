$( document ).ready(function() {
    $('.js-choosable').change(function(){
        console.log( $(this).val() );
        var foo = [];
        $('.js-choosable').each(function(i, l){
            foo[i]=$(l).val()
        });
        console.log(foo);



    });
});