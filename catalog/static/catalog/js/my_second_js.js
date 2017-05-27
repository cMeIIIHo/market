$( document ).ready(function() {
    var price = parseInt($("#price").text());
    $("#amount").change(function(){
       console.log( $(this).val() );
       var quantity = parseInt($(this).val());
       var newPrice = price*quantity;
       $("#price").text(newPrice);
    });
});



