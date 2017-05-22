var price = parseInt($(".price").text());
var quantity = parseInt($(".quantity").val());
$(".quantity").keyup(function(){
   var quantity = parseInt($(this).val());
   var newPrice = price*quantity;
   $(".price").text(newPrice);
});