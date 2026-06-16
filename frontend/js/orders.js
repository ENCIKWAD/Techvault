/*
🎯 ORDERS.JS - STATE & OBSERVER PATTERNS (FRONTEND)
====================================================
This file displays orders with state management and notifications.

Patterns Demonstrated:

1. STATE Pattern:
   - Orders transition through states: pending → paid → shipped → received
   - Each state displays different UI (buttons, messages)
   - Customer can mark as received when in "shipped" state

2. OBSERVER Pattern:
   - Status changes trigger notifications
   - When admin approves payment, customer sees update
   - When order ships, customer sees status change

Key Functions:
- loadCustomerOrders(): Load and display customer's orders
- loadAdminOrders(): Load and display all orders for admin
- approveOrderPayment(): Admin approves payment (triggers STATE transition)
- markItemReceived(): Customer confirms receipt

State Display Logic:
- Pending: Shows awaiting payment message
- Paid: Shows order confirmed
- Shipped: Shows shipping info + "Item Received" button
- Received: Shows completion message

Related Backend Files:
- backend/app/routes/order.py: Handles status updates (STATE pattern)
- backend/app/services/order_state.py: STATE pattern implementation
- backend/app/services/notification.py: OBSERVER pattern (notifies when status changes)
- backend/app/data_access/order_repository.py: Persists order state in database

Related Files:
- frontend/pages/orders.html: Orders UI with customer and admin views
- frontend/js/admin.js: Also displays orders for admin dashboard
*/

document.addEventListener('DOMContentLoaded', async () => {
    const userId = localStorage.getItem('userId');
    const userRole = localStorage.getItem('userRole');

    const customerView = document.getElementById('customer-view');
    const adminView = document.getElementById('admin-view');
    const notLoggedIn = document.getElementById('not-logged-in');

    if (!userId) {
        notLoggedIn.style.display = 'block';
        return;
    }

    if (userRole === 'admin') {
        adminView.style.display = 'block';
        await loadAdminOrders();
    } else {
        customerView.style.display = 'block';
        await loadCustomerOrders();
    }
});

// ===== CUSTOMER VIEW =====
async function loadCustomerOrders() {
    const userId = localStorage.getItem('userId');
    console.log(`[ORDERS] 👤 Loading orders for customer ${userId}`);

    const orders = await APIClient.get(`/order/user/${userId}`);
    console.log(`[ORDERS] 📦 Found ${orders ? orders.length : 0} orders`, orders);

    const ordersContainer = document.getElementById('customer-orders');

    if (!orders || orders.length === 0) {
        console.log(`[ORDERS] ℹ️ No orders found for user ${userId}`);
        ordersContainer.innerHTML = '<p style="text-align: center; padding: 40px; color: #7f8c8d;">No orders yet. <a href="index.html">Start shopping</a></p>';
        return;
    }

    let html = '';

    for (const order of orders) {
        // Get order items (for now, we'll show basic order info since items aren't returned by the API)
        const paymentStatusClass = order.status === 'paid' ? 'status-paid' : 'status-pending';
        const paymentStatusText = order.status === 'paid' ? '✓ Paid' : '⏳ Pending Payment';
        const paymentMethodText = order.payment_method === 'card' ? '💳 Credit Card' : '💵 Cash on Delivery';

        html += `
            <div class="customer-order-card">
                <div class="order-header">
                    <div>
                        <h4 style="margin: 0;">Order #${order.id}</h4>
                        <p style="margin: 5px 0 0 0; color: #7f8c8d; font-size: 13px;">${order.created_at}</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; font-size: 13px; color: #7f8c8d;">${paymentMethodText}</p>
                        <div class="payment-status ${paymentStatusClass}">${paymentStatusText}</div>
                    </div>
                </div>

                <div class="order-items">
                    <p style="color: #7f8c8d; font-size: 13px; margin-bottom: 10px;">Items ordered:</p>
                    <div class="order-item">
                        <span class="item-name"><strong>Order Total</strong></span>
                        <span class="item-price"><strong>RM${order.total_amount.toFixed(2)}</strong></span>
                    </div>
                </div>

                <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #ecf0f1;">
                    <p style="margin: 0; font-size: 13px; color: #7f8c8d;">
                        <strong>Status:</strong>
                        <span style="text-transform: capitalize; color: #2c3e50;">
                            ${getCustomerOrderStatus(order.status)}
                        </span>
                    </p>
                    ${order.status === 'shipped' ? `
                        <button onclick="markItemReceived(${order.id})"
                                style="width: 100%; padding: 10px; margin-top: 10px; background-color: #27ae60; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
                            ✓ Item Received
                        </button>
                    ` : order.status === 'received' ? `
                        <div style="width: 100%; padding: 10px; margin-top: 10px; background-color: #d5f4e6; color: #27ae60; border-radius: 4px; text-align: center; font-weight: bold;">
                            ✓ Order Completed
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    ordersContainer.innerHTML = html;
}

function getCustomerOrderStatus(status) {
    const statusMap = {
        'pending': ' Pending',
        'paid': '✓ Paid',
        'shipped': ' Shipped',
        'received': 'Received'
    };
    return statusMap[status] || status;
}

async function markItemReceived(orderId) {
    const result = await APIClient.put(`/order/${orderId}/status/received`, {});
    if (result && result.success) {
        alert('✅ Order marked as received!');
        await loadCustomerOrders();
    } else {
        alert('❌ Failed to update order!');
    }
}

// ===== ADMIN VIEW =====
async function loadAdminOrders() {
    const orders = await APIClient.get(`/order/user/1`);
    const adminOrdersContainer = document.getElementById('admin-orders');

    if (!orders || orders.length === 0) {
        adminOrdersContainer.innerHTML = '<p style="text-align: center; padding: 40px;">No orders found.</p>';
        return;
    }

    let html = `
        <style>
            .admin-orders-table {
                width: 100%;
                border-collapse: collapse;
                background: white;
                border-radius: 4px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }
            .admin-orders-table th {
                background: #34495e;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: bold;
            }
            .admin-orders-table td {
                padding: 12px;
                border-bottom: 1px solid #ecf0f1;
            }
            .admin-orders-table tr:hover {
                background: #f9f9f9;
            }
            .order-status-badge {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
            }
            .status-pending { background: #f39c12; color: white; }
            .status-paid { background: #3498db; color: white; }
            .status-shipped { background: #9b59b6; color: white; }
            .status-received { background: #27ae60; color: white; }
            .approve-checkbox {
                width: 18px;
                height: 18px;
                cursor: pointer;
            }
            .section-title {
                margin-top: 30px;
                margin-bottom: 15px;
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
            }
        </style>

        <h3 class="section-title">Pending Orders</h3>
        <table class="admin-orders-table">
            <thead>
                <tr>
                    <th>Order #</th>
                    <th>Customer ID</th>
                    <th>Amount</th>
                    <th>Payment Method</th>
                    <th>Status</th>
                    <th>Approve Payment</th>
                </tr>
            </thead>
            <tbody id="pending-orders-tbody">
            </tbody>
        </table>

        <h3 class="section-title">Completed Orders</h3>
        <table class="admin-orders-table">
            <thead>
                <tr>
                    <th>Order #</th>
                    <th>Customer ID</th>
                    <th>Amount</th>
                    <th>Payment Method</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody id="completed-orders-tbody">
            </tbody>
        </table>
    `;

    adminOrdersContainer.innerHTML = html;

    const pending = orders.filter(o => o.status === 'pending');
    const completed = orders.filter(o => o.status !== 'pending');

    const pendingTbody = document.getElementById('pending-orders-tbody');
    const completedTbody = document.getElementById('completed-orders-tbody');

    pendingTbody.innerHTML = pending.map(order => `
        <tr>
            <td>#${order.id}</td>
            <td>${order.user_id}</td>
            <td>RM${order.total_amount.toFixed(2)}</td>
            <td>${order.payment_method === 'card' ? '💳 Card' : '💵 COD'}</td>
            <td><span class="order-status-badge status-${order.status}">${order.status.toUpperCase()}</span></td>
            <td>
                <input type="checkbox" class="approve-checkbox" onchange="approveOrderPayment(${order.id}, this.checked, '${order.payment_method}')" />
            </td>
        </tr>
    `).join('');

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

async function approveOrderPayment(orderId, isChecked, paymentMethod) {
    if (!isChecked) return;

    console.log(`[ADMIN APPROVAL] 👨‍💼 Admin approving payment for order #${orderId}`);
    console.log(`[ADMIN APPROVAL] 💳 Payment method: ${paymentMethod}`);

    const result = await APIClient.put(`/order/${orderId}/status/paid`, {});
    console.log(`[ADMIN APPROVAL] 📊 Approval response:`, result);

    if (result && result.success) {
        console.log(`[ADMIN APPROVAL] ✅ Order #${orderId} status updated to PAID`);
        alert(`✅ Payment approved! Order #${orderId} marked as paid.`);
        await loadAdminOrders();
    } else {
        console.error(`[ADMIN APPROVAL] ❌ Failed to approve payment`, result);
        alert('❌ Failed to approve payment');
    }
}
