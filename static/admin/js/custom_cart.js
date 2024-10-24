// static/admin/js/sales_cart.js
let cart = [];

function addToCart(productId) {
    // Aquí puedes agregar lógica para agregar productos al carrito
    cart.push(productId);
    updateCartDisplay();
}

function updateCartDisplay() {
    const cartItemsDiv = document.getElementById('cart-items');
    cartItemsDiv.innerHTML = '';

    cart.forEach(function(productId) {
        const product = document.createElement('div');
        product.textContent = 'Producto ID: ' + productId;
        cartItemsDiv.appendChild(product);
    });
}
