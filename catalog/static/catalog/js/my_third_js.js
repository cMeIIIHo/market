$( document ).ready(function() {
    $('.choosable').change(function(){
        console.log( $(this).val() );
        var foo = [];
        $('.choosable').each(function(i, l){
            foo[i]=$(l).val()
        });
        console.log(foo);



    });
});