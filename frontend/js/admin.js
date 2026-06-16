/*
🎯 ADMIN.JS - FACADE & FACTORY PATTERNS (FRONTEND)
===================================================
This file handles admin dashboard and operations.

Patterns Demonstrated:

1. FACADE Pattern:
   - AdminService backend provides simplified API
   - Complex operations (get stats, update inventory) are hidden
   - Frontend calls simple methods without knowing implementation

2. FACTORY Pattern:
   - Admin dashboard is role-specific (created for 'admin' role users)
   - Dashboard shows: Product Management + Order Management tabs
   - Different UI from customer dashboard

Key Functions:
- loadProducts(): Load all products for management
- loadOrders(): Load all orders for approval
- startEditProduct(): Begin editing a product
- saveProduct(): Save product changes
- deleteProduct(): Remove product from inventory
- approvePayment(): Admin approves COD payment (triggers STATE transition)

Tab Interface:
- Products tab: View, edit, delete products
- Orders tab: View pending orders, approve payments

Role-Based Access:
- Only accessible to users with role='admin'
- Factory pattern determines this is admin dashboard (not customer)
- Different UI and functionality from customer pages

Related Backend Files:
- backend/app/services/admin_service.py: FACADE pattern (simplified API)
- backend/app/services/dashboard_factory.py: FACTORY pattern (creates admin dashboard)
- backend/app/routes/catalog.py: Product API endpoints
- backend/app/routes/order.py: Order API endpoints
- backend/app/data_access/product_repository.py: Product operations
- backend/app/data_access/order_repository.py: Order operations

Related Files:
- frontend/pages/admin.html: Admin dashboard HTML
- frontend/js/nav.js: Determines role and directs to admin page
*/

let editingProductId = null;
let editingProductData = {};

document.addEventListener('DOMContentLoaded', async () => {
    const userId = localStorage.getItem('userId');
    const userRole = localStorage.getItem('userRole');

    if (!userId || userRole !== 'admin') {
        document.body.innerHTML = '<div style="padding: 40px; text-align: center;"><p style="color: #e74c3c;">⛔ Admin access required</p><p><a href="index.html">Return to home</a></p></div>';
        return;
    }

    await loadProducts();
    await loadOrders();
});

function switchTab(tab) {
    document.querySelectorAll('.admin-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.admin-tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(tab).classList.add('active');
    event.target.classList.add('active');
}

// ===== PRODUCT MANAGEMENT =====
async function loadProducts() {
    const products = await APIClient.get('/catalog/products');
    const tbody = document.getElementById('products-table-body');

    if (!products || products.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6">No products found</td></tr>';
        return;
    }

    tbody.innerHTML = products.map(product => `
        <tr id="product-row-${product.id}">
            <td>${product.id}</td>
            <td><span id="name-${product.id}">${product.name}</span></td>
            <td><span id="desc-${product.id}">${product.description}</span></td>
            <td>RM<span id="price-${product.id}">${product.price.toFixed(2)}</span></td>
            <td><span id="stock-${product.id}">${product.stock}</span></td>
            <td>
                <button class="edit-btn" onclick="startEditProduct(${product.id}, '${product.name}', '${product.description}', ${product.price}, ${product.stock})">Edit</button>
                <button class="delete-btn" onclick="deleteProduct(${product.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function startEditProduct(id, name, desc, price, stock) {
    editingProductId = id;
    editingProductData = { name, description: desc, price, stock };

    const row = document.getElementById(`product-row-${id}`);
    row.innerHTML = `
        <td>${id}</td>
        <td class="input-cell"><input type="text" id="edit-name" value="${name}"></td>
        <td class="input-cell"><input type="text" id="edit-desc" value="${desc}"></td>
        <td class="input-cell">RM<input type="number" id="edit-price" value="${price}" step="0.01" style="width: 80px;"></td>
        <td class="input-cell"><input type="number" id="edit-stock" value="${stock}" style="width: 60px;"></td>
        <td>
            <button class="save-btn" onclick="saveProduct(${id})">Save</button>
            <button class="cancel-btn" onclick="cancelEditProduct()">Cancel</button>
        </td>
    `;
}

async function saveProduct(id) {
    const data = {
        name: document.getElementById('edit-name').value,
        description: document.getElementById('edit-desc').value,
        price: parseFloat(document.getElementById('edit-price').value),
        stock: parseInt(document.getElementById('edit-stock').value)
    };

    const result = await APIClient.put(`/catalog/products/${id}`, data);

    if (result && result.success) {
        alert('✅ Product updated!');
        editingProductId = null;
        await loadProducts();
    } else {
        alert('❌ Failed to update product');
    }
}

function cancelEditProduct() {
    editingProductId = null;
    loadProducts();
}

async function deleteProduct(id) {
    if (!confirm('Are you sure you want to delete this product?')) return;

    const result = await APIClient.put(`/catalog/products/${id}`, null);

    // Try DELETE instead
    const response = await fetch(`http://localhost:5000/api/catalog/products/${id}`, {
        method: 'DELETE'
    });
    const deleteResult = await response.json();

    if (deleteResult && deleteResult.success) {
        alert('✅ Product deleted!');
        await loadProducts();
    } else {
        alert('❌ Failed to delete product');
    }
}

// ===== ORDER MANAGEMENT =====
async function loadOrders() {
    const orders = await APIClient.get('/order/user/1');
    const pendingTbody = document.getElementById('orders-table-body');
    const completedTbody = document.getElementById('completed-orders-body');

    if (!orders || orders.length === 0) {
        pendingTbody.innerHTML = '<tr><td colspan="6">No pending orders</td></tr>';
        completedTbody.innerHTML = '<tr><td colspan="5">No completed orders</td></tr>';
        return;
    }

    const pending = orders.filter(o => o.status === 'pending');
    const completed = orders.filter(o => o.status !== 'pending');

    // Pending Orders
    pendingTbody.innerHTML = pending.map(order => `
        <tr>
            <td>#${order.id}</td>
            <td>${order.user_id}</td>
            <td>RM${order.total_amount.toFixed(2)}</td>
            <td>${order.payment_method === 'card' ? '💳 Card' : '💵 COD'}</td>
            <td><span class="order-status-badge status-${order.status}">${order.status.toUpperCase()}</span></td>
            <td>
                <input type="checkbox" style="width: 18px; height: 18px; cursor: pointer;" onchange="approvePayment(${order.id}, this.checked)" />
            </td>
        </tr>
    `).join('');

    // Completed Orders
    completedTbody.innerHTML = completed.map(order => `
        <tr>
            <td>#${order.id}</td>
            <td>${order.user_id}</td>
            <td>RM${order.total_amount.toFixed(2)}</td>
            <td>${order.payment_method === 'card' ? '💳 Card' : '💵 COD'}</td>
            <td><span class="order-status-badge status-${order.status}">${order.status.toUpperCase()}</span></td>
        </tr>
    `).join('');

    if (pending.length === 0) {
        pendingTbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 20px;">No pending orders</td></tr>';
    }

    if (completed.length === 0) {
        completedTbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 20px;">No completed orders</td></tr>';
    }
}

async function approvePayment(orderId, isChecked) {
    if (!isChecked) return;

    const result = await APIClient.put(`/order/${orderId}/status/paid`, {});

    if (result && result.success) {
        alert(`✅ Payment approved! Order #${orderId} marked as paid.`);
        await loadOrders();
    } else {
        alert('❌ Failed to approve payment');
    }
}
