# TechVault Debugging Guide

## 🎯 Overview
This guide demonstrates debugging techniques for the TechVault e-commerce system with Gang of Four design patterns.

---

## 1️⃣ FRONTEND DEBUGGING (Browser DevTools)

### A. Console Debugging

**Enable Debug Logging:**

Add these functions to `frontend/js/catalog.js` for tracing:

```javascript
const DEBUG = true;

function log(section, message, data = null) {
    if (DEBUG) {
        console.log(`[${section}] ${message}`, data || '');
    }
}

// Example usage:
log('CATALOG', 'Loading products', products);
log('CART', 'Item added', {productId: 1, qty: 2});
log('ORDER', 'Checkout initiated', {paymentMethod: 'card'});
```

**Usage:**
1. Open browser DevTools (F12 or Cmd+Option+I)
2. Go to **Console** tab
3. See all debug logs with section labels
4. Filter logs: type in console `[CATALOG]` to see only catalog logs

### B. Network Inspector (Trace API Calls)

1. Open DevTools → **Network** tab
2. Perform any action (add to cart, checkout, etc.)
3. Click on the API request to see:
   - **Request headers** (auth, content-type)
   - **Request body** (what data was sent)
   - **Response** (what backend returned)
   - **Status** (200, 404, 500, etc.)

**Common endpoints to monitor:**
```
POST /api/auth/login        → User authentication
POST /cart/add              → Add product to cart
POST /order/checkout        → Create order (STRATEGY pattern)
PUT /order/{id}/status/{s}  → Update order status (STATE pattern)
```

### C. Breakpoints & Step Debugging

1. **Set breakpoints:**
   - Go to **Sources** tab
   - Click line number to set breakpoint
   - Example: Set breakpoint in `cart.js` line 72 (checkout function)

2. **Step through code:**
   - **F10** - Step over (next line)
   - **F11** - Step into (enter function)
   - **Shift+F11** - Step out (exit function)

3. **Watch expressions:**
   - Add variables to watch: `userId`, `cart.total`, `order.status`
   - See values change as you step through

### D. LocalStorage Inspector

**View user session data:**
```javascript
// In console, type:
localStorage.getItem('userId')      // See logged-in user ID
localStorage.getItem('userRole')    // See user role (admin/customer)
localStorage.getItem('username')    // See username
```

**Clear session (logout):**
```javascript
localStorage.clear();
```

---

## 2️⃣ BACKEND DEBUGGING (Python)

### A. Print Debugging

**Add temporary debug prints:**

In `backend/app/routes/order.py`:

```python
@order_bp.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    user_id = data['user_id']
    payment_method = data['payment_method']
    
    print(f"🔍 DEBUG: User {user_id} checking out with {payment_method}")
    
    # Create order
    order_id = OrderRepository.create_order(user_id, total, payment_method)
    print(f"🔍 DEBUG: Order created with ID {order_id}")
    
    # Process payment (STRATEGY pattern)
    if payment_method == 'card':
        strategy = CreditCardPayment()
        print(f"🔍 DEBUG: Using CreditCardPayment strategy")
    else:
        strategy = CashOnDeliveryPayment()
        print(f"🔍 DEBUG: Using CashOnDeliveryPayment strategy")
    
    processor = PaymentProcessor(strategy)
    payment_result = processor.pay(total, user_id)
    print(f"🔍 DEBUG: Payment result: {payment_result}")
```

### B. Inspect Database

**SQLite Database Inspector:**

1. **Install DB Browser for SQLite** (already installed on your system)

2. **Open database:**
   ```bash
   cd /Users/encikwad/Documents/Software_Design/Project_Assignment/backend
   sqlite3 data.db
   ```

3. **Common queries to debug:**

   ```sql
   -- See all users
   SELECT id, username, email, role FROM user;
   
   -- See all products and prices
   SELECT id, name, price, stock FROM product;
   
   -- See all orders
   SELECT id, user_id, total_amount, payment_method, status FROM orders;
   
   -- See specific user's orders
   SELECT * FROM orders WHERE user_id = 2;
   
   -- See order items
   SELECT * FROM order_item;
   
   -- Check cart contents
   SELECT * FROM cart_item WHERE user_id = 2;
   ```

4. **Exit SQLite:**
   ```
   .exit
   ```

---

## 3️⃣ DESIGN PATTERN DEBUGGING

### A. STRATEGY Pattern (Payment)

**How to debug payment flow:**

1. **Add logging in payment_strategy.py:**
```python
class PaymentProcessor:
    def __init__(self, strategy):
        print(f"🏗️ STRATEGY: PaymentProcessor initialized with {strategy.__class__.__name__}")
        self.strategy = strategy

    def pay(self, amount, user_id):
        print(f"💳 STRATEGY: Processing payment of RM{amount} using {self.strategy.__class__.__name__}")
        return self.strategy.process_payment(amount, user_id)
```

2. **Watch the console** when checking out:
   - With Card → see "CreditCardPayment"
   - With COD → see "CashOnDeliveryPayment"

### B. STATE Pattern (Order Lifecycle)

**Debug order state transitions:**

In `backend/app/routes/order.py`:

```python
@order_bp.route('/<int:order_id>/status/<status>', methods=['PUT'])
def update_order_status(order_id, status):
    print(f"📊 STATE: Updating order {order_id} to status: {status}")
    
    old_order = OrderRepository.get_order_by_id(order_id)
    print(f"📊 STATE: Old status was: {old_order['status']}")
    
    OrderRepository.update_order_status(order_id, status)
    
    new_order = OrderRepository.get_order_by_id(order_id)
    print(f"📊 STATE: New status is: {new_order['status']}")
```

**Expected flow:**
- Card: pending → paid → shipped → received
- COD: pending → paid → shipped → received

### C. OBSERVER Pattern (Notifications)

**Debug notification flow:**

In `backend/app/services/notification.py`:

```python
class OrderNotificationManager:
    def notify_status_change(self, order_id, status):
        print(f"📢 OBSERVER: Status changed, notifying {len(self.observers)} observers")
        for observer in self.observers:
            print(f"📢 OBSERVER: Notifying {observer.__class__.__name__}")
            observer.update(order_id, status)
```

---

## 4️⃣ TESTING SCENARIOS FOR DEMONSTRATION

### Scenario 1: Customer Journey (with debugging)

1. **Open DevTools Console** (F12)
2. **Register as customer:**
   - Username: `test_customer`
   - Email: `customer@test.com`
   - Password: `test123`
   - Watch: `POST /api/auth/register` in Network tab

3. **Login:**
   - Watch localStorage update: `console.log(localStorage)`
   - Check: userId, userRole, username set

4. **Browse products:**
   - Network tab shows: `GET /api/catalog/products`
   - Console shows all products loaded

5. **Add to cart:**
   - Network shows: `POST /api/cart/add`
   - Check request body has correct productId

6. **Checkout with Card:**
   - Network shows: `POST /api/order/checkout` 
   - Backend console shows STRATEGY pattern: "CreditCardPayment"
   - Check database: new order created with status="paid"

### Scenario 2: Admin Approval (COD Order)

1. **Login as admin:**
   - Email: `admin@techvault.com`
   - Password: `admin123`

2. **Go to Orders tab:**
   - Should see pending orders
   - Network shows: `GET /api/order/user/1`

3. **Approve payment (check checkbox):**
   - Network shows: `PUT /api/order/{id}/status/paid`
   - Database: order status changes to "paid"
   - Order moves to "Completed" section

4. **Watch STATE pattern:**
   - Backend console shows state transitions
   - OBSERVER pattern triggers notifications

### Scenario 3: Product Edit (Admin)

1. **Go to Products tab:**
   - Edit a product (change price, stock)
   - Network shows: `PUT /api/catalog/products/{id}`

2. **Check database:**
   ```sql
   SELECT id, name, price, stock FROM product WHERE id = 1;
   ```

---

## 5️⃣ USEFUL BREAKPOINT LOCATIONS

| File | Function | Line | Purpose |
|------|----------|------|---------|
| `cart.js` | `checkout()` | 72 | Trace payment initiation |
| `orders.js` | `approveOrderPayment()` | 98 | Debug status update |
| `admin.js` | `loadOrders()` | 113 | See order fetching |
| `catalog.js` | `addToCart()` | 55 | Track item addition |
| `order.py` | `checkout()` | 15 | Backend order creation |
| `order.py` | `update_order_status()` | 63 | Backend state change |

---

## 6️⃣ COMMON DEBUGGING COMMANDS

**Frontend Console:**
```javascript
// Check current user
console.log('User:', {
    id: localStorage.getItem('userId'),
    role: localStorage.getItem('userRole'),
    name: localStorage.getItem('username')
});

// Test API call
APIClient.get('/catalog/products').then(p => console.log('Products:', p));

// Check cart state
APIClient.get(`/cart/${localStorage.getItem('userId')}`).then(c => console.log('Cart:', c));
```

**Backend Terminal:**
```bash
# Start backend with debug output
cd backend
python3 run.py

# The print() statements will show up in the terminal
```

**SQLite:**
```sql
-- Check recent orders
SELECT * FROM orders ORDER BY created_at DESC LIMIT 5;

-- Check cart contents
SELECT c.*, p.name FROM cart_item c JOIN product p ON c.product_id = p.id;

-- Verify payment flows
SELECT id, status, payment_method FROM orders WHERE user_id = 2;
```

---

## 7️⃣ DEMONSTRATION SCRIPT FOR LECTURER

### Part 1: Frontend Debugging (5 minutes)
1. Open browser DevTools
2. Show Console with debug logs
3. Add to cart - show Network request/response
4. Show LocalStorage for session tracking
5. Set breakpoint in checkout function

### Part 2: Backend Debugging (5 minutes)
1. Show Python print statements in terminal
2. Demonstrate STRATEGY pattern switching (card vs COD)
3. Show STATE pattern transitions in console output
4. Show OBSERVER pattern notifications

### Part 3: Database Verification (3 minutes)
1. Open SQLite Database Browser
2. Query orders table to show status changes
3. Query cart_item to show items added
4. Show design patterns reflected in data

### Part 4: Full Flow Test (5 minutes)
1. Create account → Show DB insert
2. Add to cart → Show API call + DB update
3. Checkout with COD → Show STRATEGY pattern
4. Admin approves → Show STATE + OBSERVER patterns
5. Verify final order status in DB

---

## 📋 DEBUGGING CHECKLIST

- [ ] DevTools Console shows no errors
- [ ] Network tab shows successful API calls (200, 201 status)
- [ ] LocalStorage has userId, userRole, username
- [ ] Database has correct order records
- [ ] Order status follows correct workflow
- [ ] Design patterns visible in console output
- [ ] No SQL errors in database queries
- [ ] Price displays in RM currency
- [ ] Role-based UI works (admin vs customer)

---

## 🐛 Common Issues & Solutions

| Issue | Debug Method | Solution |
|-------|--------------|----------|
| "Cannot add to cart" | Check Console for errors | Verify userId in localStorage |
| Order not showing in orders.html | Network tab check | Ensure API returns orders |
| Product price wrong | SQLite query | Check if update was successful |
| Admin can't approve order | Console log status | Check order status enum values |
| Payment not processing | Backend print statements | Check STRATEGY pattern initialization |

---

End of Debugging Guide
