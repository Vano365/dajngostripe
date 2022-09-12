fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  document.querySelector("#submitBtnUsd").addEventListener("click", () => {
    // Get Checkout Session ID
    price = document.querySelector("#total_usd").innerHTML;
    quanity = 1
    cur = 'usd'
    if (Number(price) > 0){

    fetch("/create-checkout-session/" + price + "/" + quanity + "/" + cur + "/")
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  }});
});