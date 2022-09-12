function add_to_cart(id) {
    
    addtocartBtn = document.querySelector("#addtocartBtn");
    addtocartBtn.classList.add('disabled');
    addtocartBtn.innerHTML = "Товар уже в корзине";
    
    qty = document.querySelector("#qty_input").value;
    count_cart = document.querySelector("#cart_count").innerHTML;
    $.ajax({
           type: "GET",
           data: {'id': id, 'qty': qty},
           url: "/add-to-cart/",
           cache:true,
           success: function (response) {
             console.log(response);
             document.querySelector("#cart_count").innerHTML = Number(qty) + Number(count_cart);

           },
           error: function (response) {
            addtocartBtn.classList.remove('disabled');
            addtocartBtn.innerHTML = "В Корзину";
           }
   });
}
function add_to_cart_one(id) {
    qty = 1;
    count_cart = document.querySelector("#cart_count").innerHTML;
    $.ajax({
           type: "GET",
           data: {'id': id, 'qty': qty},
           url: "/add-to-cart/",
           cache:true,
           success: function (response) {
             console.log(response);
             document.querySelector("#cart_count").innerHTML = Number(qty) + Number(count_cart);

           },
           error: function (response) {
           }
   });
}

function delete_product_to_cart(id, cur, total) {
    count_cart = document.querySelector("#cart_count").innerHTML;

    total_usd = document.querySelector("#total_usd").innerHTML;
    total_eur = document.querySelector("#total_eur").innerHTML;
    total_rub = document.querySelector("#total_rub").innerHTML;
    $.ajax({
           type: "GET",
           data: {'id': id},
           url: "/delete-product-to-cart/",
           cache:true,
           success: function (response) {
             console.log(response);
             document.querySelector("#cart_count").innerHTML = Number(count_cart) - Number(response.qty);
             document.querySelector("#tr_" + id).remove()
             if (cur == 'usd'){
              document.querySelector("#total_usd").innerHTML = total_usd - total;
            }
            else if(cur == 'eur'){
              document.querySelector("#total_eur").innerHTML = total_eur - total;
            }
            else if(cur == 'rub'){
              document.querySelector("#total_rub").innerHTML = total_rub - total;
            }
           },
           error: function (response) {
           }
   });
}

function delete_to_cart() {
    $.ajax({
           type: "GET",
           data: {},
           url: "/delete-to-cart/",
           cache:true,
           success: function (response) {
             console.log(response);
             document.querySelector("#cart_count").innerHTML = 0
             document.querySelector("#table_product").remove()
             document.querySelector("#total_usd").innerHTML = 0;
            document.querySelector("#total_eur").innerHTML = 0;
            document.querySelector("#total_rub").innerHTML = 0;
           },
           error: function (response) {
           }
   });
}

function add_to_cart_one_cart(id, price, qty_one, cur) {
    qty = document.querySelector("#qty_input_" + id).value;
    count_cart = document.querySelector("#cart_count").innerHTML;
    cart_total = document.querySelector("#cart_total_" + id);

    total_usd = document.querySelector("#total_usd").innerHTML;
    total_eur = document.querySelector("#total_eur").innerHTML;
    total_rub = document.querySelector("#total_rub").innerHTML;
    if (count_cart > 0){
    $.ajax({
           type: "GET",
           data: {'id': id, 'qty': qty_one},
           url: "/add-to-cart/",
           cache:true,
           success: function (response) {
            console.log(response);
            document.querySelector("#cart_count").innerHTML = Number(qty_one) + Number(count_cart);
            cart_total.innerHTML = price * (Number(qty) + 1);
            if (cur == 'usd'){
              total_usd = Number(total_usd) + price * qty_one ;
              document.querySelector("#total_usd").innerHTML = total_usd;
            }
            else if(cur == 'eur'){
              total_eur = Number(total_eur) + price * qty_one ;
              document.querySelector("#total_eur").innerHTML = total_eur;
            }
            else if(cur == 'rub'){
              total_rub = Number(total_rub) + price * qty_one ;
              document.querySelector("#total_rub").innerHTML = total_rub;
            }
           },
           error: function (response) {
           }
   });}
   else{
    delete_product_to_cart(id);
   }
}