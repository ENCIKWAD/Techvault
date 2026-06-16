/*
🎯 CART.JS - STRATEGY PATTERN (FRONTEND)
==========================================
This file handles shopping cart and checkout functionality.

Pattern Demonstrated: STRATEGY Pattern
Purpose: User selects payment method at checkout
         Frontend triggers backend to use appropriate payment strategy

Key Functions:
- loadCart(): Display cart items and total
- removeItem(): Remove product from cart
- checkout(): Execute payment with selected strategy

Design Pattern Flow:
1. User selects payment method (radio button):
   - Card: triggers CreditCardPayment strategy
   - COD: triggers CashOnDeliveryPayment strategy

2. Frontend sends payment method to backend

3. Backend uses STRATEGY pattern to execute:
   - CreditCardPayment.process_payment()
   - CashOnDeliveryPayment.process_payment()

Related Backend Files:
- backend/app/routes/order.py: Receives payment method, uses strategy
- backend/app/services/payment_strategy.py: Strategy implementations

Related Files:
- frontend/pages/cart.html: Cart UI with payment method radio buttons
- frontend/js/catalog.js: Adds products to this cart
*/

document.addEventListener('DOMContentLoaded', async () => {
    const userId = localStorage.getItem('userId');
    const userRole = localStorage.getItem('userRole');

    if (!userId) {
        window.location.href = 'login.html';
        return;
    }

    // Admins cannot access cart
    if (userRole === 'admin') {
        window.location.href = 'admin.html';
        return;
    }

    await loadCart();

    // Checkout button
    document.getElementById('checkout-btn').addEventListener('click', checkout);
});

async function loadCart() {
    const userId = localStorage.getItem('userId');
    const cart = await APIClient.get(`/cart/${userId}`);

    if (!cart || !cart.items || cart.items.length === 0) {
        document.getElementById('cart-list').innerHTML = '<p>Your cart is empty</p>';
        document.getElementById('cart-total').textContent = 'Total: RM0.00';
        return;
    }

    // Display cart items
    const cartHtml = cart.items.map(item => `
        <div class="cart-item" style="padding: 15px; border-bottom: 1px solid #ddd;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4>${item.name}</h4>
                    <p>Price: RM${item.price}</p>
                    <p>Quantity: ${item.quantity}</p>
                    <p style="color: #27ae60; font-weight: bold;">Subtotal: RM${(item.price * item.quantity).toFixed(2)}</p>
                </div>
                <button onclick="removeItem(${item.product_id})" style="
                    padding: 8px 15px;
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                ">Remove</button>
            </div>
        </div>
    `).join('');

    document.getElementById('cart-list').innerHTML = cartHtml;

    // Update total
    document.getElementById('cart-total').textContent = `Total: RM${cart.total.toFixed(2)}`;
}

async function removeItem(productId) {
    const userId = localStorage.getItem('userId');
    const result = await APIClient.post('/cart/remove', {
        user_id: userId,
        product_id: productId
    });

    if (result && result.success) {
        await loadCart();
    }
}

async function checkout() {
    const userId = localStorage.getItem('userId');
    const paymentMethod = document.querySelector('input[name="payment"]:checked').value;

    console.log(`[CHECKOUT] 🛒 User ${userId} initiating checkout with ${paymentMethod}`);

    const result = await APIClient.post('/order/checkout', {
        user_id: userId,
        payment_method: paymentMethod
    });

    console.log(`[CHECKOUT] 📊 Response:`, result);

    if (result && result.status === 'success') {
        console.log(`[CHECKOUT] ✅ Order #${result.order_id} created successfully`);
        alert(`✅ Order placed successfully!\nOrder ID: ${result.order_id}`);
        window.location.href = 'orders.html';
    } else {
        console.error(`[CHECKOUT] ❌ Checkout failed`, result);
        alert('❌ Checkout failed!');
    }
}
