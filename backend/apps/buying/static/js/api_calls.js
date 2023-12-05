const stripe_key = 'pk_test_51OJh2RK32lDd86yxP9kJlFxVViTRS64G54BlreNbIAgahunSZG4kMvSlaWfIYlGaT6x2cUqMlrtPuxll714UtKOM00dn90XbHJ'

function buy_item(){
    var stripe = Stripe(stripe_key)
    item_id = document.getElementById('item_id').innerText
    currency = document.getElementById('currency').innerText
    axios.get(`/buy/${item_id}/currency/${currency}`)
        .then(function(response){
            return stripe.redirectToCheckout({ sessionId: response.data.session_id })
        })
        .catch(function(error){
            console.error(error)
        })
    
}

function make_order(){
    var stripe = Stripe(stripe_key)
    order_id = document.getElementById('order_id').innerText
    currency = document.getElementById('currency').innerText
    console.log(`/makeorder/${order_id}/currency/${currency}`)
    axios.get(`/makeorder/${order_id}/currency/${currency}`)
        .then(function(response){
            return stripe.redirectToCheckout({ sessionId: response.data.session_id })
        })
        .catch(function(error){
            console.error(error)
        })
}