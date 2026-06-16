document.addEventListener('DOMContentLoaded', async () => {
    const products = await APIClient.get('/catalog/products');
    displayProducts(products);
});

function displayProducts(products) {
    const grid = document.getElementById('products-grid');
    const userRole = localStorage.getItem('userRole');
    grid.innerHTML = '';

    if (!products) return;

    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';

        const buttonHtml = userRole === 'admin'
            ? `<p style="color: #7f8c8d; font-size: 12px; text-align: center; margin-top: 10px;"></p>`
            : `<button onclick="addToCart(${product.id})">Add to Cart</button>`;

        card.innerHTML = `
            <h4>${product.name}</h4>
            <p>${product.description}</p>
            <p class="price">RM${product.price}</p>
            <p class="stock">Stock: ${product.stock}</p>
            ${buttonHtml}
        `;
        grid.appendChild(card);
    });
}

async function addToCart(productId) {
    const userId = localStorage.getItem('userId');
    if (!userId) {
        alert('Please login first');
        window.location.href = 'login.html';
        return;
    }

    const result = await APIClient.post('/cart/add', {
        user_id: userId,
        product_id: productId,
        quantity: 1
    });

    if (result && result.success) {
        alert('Added to cart!');
    }
}
