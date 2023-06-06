//--------------------------------------------------------------
document.addEventListener("keyup", e=>{
    if(e.target.matches("#buscador")){
        document.querySelectorAll(".card").forEach(fruta=>{
            fruta.textContent.toLowerCase().includes(e.target.value.toLowerCase())
                ?fruta.classList.remove("inactive")
                :fruta.classList.add("inactive")
        })
    }
    console.log(e.target.value)
})

//Shopping Cart
const cartIcon = document.querySelector(".navbar-shopping-cart");
const shoppingCartContainer =document.querySelector("#shoppingCartContainer");

cartIcon.addEventListener("click", toggleShoppingCart);
function toggleShoppingCart() {
    shoppingCartContainer.classList.toggle("inactive");
}
const formCart = document.querySelector(".formCart")

formCart.addEventListener("submit", (event) => {
    event.preventDefault()
})
