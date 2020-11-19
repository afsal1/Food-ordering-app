var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
    
    var productId = this.dataset.product
    var action = this.dataset.action
    var val = document.getElementById("cart-total").textContent
    if (action == 'add'){
        val ++;
    }else{
        val --;
    }
    console.log('new cart', val)
    document.getElementById("cart-total").innerHTML = val
    console.log('productId:', productId, 'action :', action )
    console.log('USER:',user)

    if (user == 'AnonymousUser'){
        console.log('User not logged')

    }
    else{
        updateUserOrder(productId,action)
    }
})
}
function updateUserOrder(productId, action){
    console.log('User logged in, sending data...')

    var url = '/update_item'
    console.log('URL:', url)

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,

        },
        body:JSON.stringify({'productId':productId, 'action':action})

    })

    .then((response)=>{
        return response.json()
    })

    .then((data)=>{
        console.log('Data:',data)
        // location.reload()
    })

}