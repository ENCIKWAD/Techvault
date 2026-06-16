# VS Code Debugging Guide for TechVault

## 🎯 Setup Overview
- Debug **Python Backend** (Flask)
- Debug **JavaScript Frontend** (Browser)
- Debug **Database** (SQLite)
- View **Console Output** side-by-side

---

## 1️⃣ PYTHON BACKEND DEBUGGING

### A. Install Python Extension

1. Open VS Code
2. Go to **Extensions** (Ctrl+Shift+X)
3. Search: `Python`
4. Install **Python** by Microsoft
5. Install **Pylance** (optional, for better autocomplete)

### B. Create Launch Configuration

1. In VS Code, press **Ctrl+Shift+D** (Debug view)
2. Click **"Create a launch.json file"**
3. Select **"Python"**
4. Replace with this configuration:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "TechVault Backend",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/backend/run.py",
            "console": "integratedTerminal",
            "justMyCode": true,
            "cwd": "${workspaceFolder}/backend"
        }
    ]
}
```

### C. Set Breakpoints in Backend

1. Open `backend/app/routes/order.py`
2. **Click on line number** to set breakpoint (red dot appears)
3. Example: Set breakpoint at line 15 (checkout function start)
4. Press **F5** to start debugging
5. Perform an action (checkout) → **Execution pauses at breakpoint**

### D. Debug Controls

| Key | Action |
|-----|--------|
| **F5** | Start/Continue debugging |
| **F10** | Step over (next line) |
| **F11** | Step into (enter function) |
| **Shift+F11** | Step out (exit function) |
| **Ctrl+Shift+D** | Toggle debug panel |

### E. Watch Variables

1. In debug view, **WATCH** panel (left side)
2. Click **+** to add variable
3. Examples:
   - `user_id`
   - `order_id`
   - `payment_method`
   - `payment_result`

4. Variables update as you step through code

---

## 2️⃣ JAVASCRIPT FRONTEND DEBUGGING

### A. Install Debugger Extension

1. Extensions → Search: `Debugger for Chrome`
2. Install **Debugger for Chrome** by Microsoft
3. (Or use **Debugger for Firefox** if you prefer Firefox)

### B. Create Launch Configuration for Frontend

1. Ctrl+Shift+D → Open `.vscode/launch.json`
2. Add this configuration:

```json
{
    "name": "TechVault Frontend",
    "type": "chrome",
    "request": "attach",
    "port": 9222,
    "pathMapping": {
        "/": "${workspaceFolder}/frontend/"
    },
    "webRoot": "${workspaceFolder}/frontend"
}
```

### C. Start Frontend with Debug Mode

**Option 1: Using VS Code Terminal**

1. Open Terminal in VS Code (Ctrl+`)
2. Run:
   ```bash
   cd frontend
   python3 -m http.server 8000
   ```

**Option 2: Chrome with Remote Debugging**

1. Close all Chrome windows
2. Open Terminal and run:
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
   --remote-debugging-port=9222 http://localhost:8000/pages/index.html
   ```
   (Windows: Use `chrome.exe` path)

3. In VS Code, press **F5** to attach debugger

### D. Set Breakpoints in JavaScript

1. Open `frontend/js/cart.js`
2. **Click on line number** (e.g., line 72 - checkout function)
3. Red dot appears = breakpoint set
4. Perform action (checkout) → Debugger pauses
5. Inspect variables in left panel

### E. Debug Console Features

1. **VARIABLES** panel (left):
   - Local variables
   - Click to expand objects
   - Watch values change in real-time

2. **WATCH** panel:
   - Add: `localStorage.getItem('userId')`
   - Add: `cart.total`
   - Add: `order.status`

3. **DEBUG CONSOLE** (bottom):
   - Type commands: `localStorage`
   - Type: `document.getElementById('cart-list')`
   - Execute JS expressions

---

## 3️⃣ DEBUGGING WORKFLOW IN VS CODE

### Scenario: Debug a Checkout

**Step 1: Set Backend Breakpoint**
```
Open: backend/app/routes/order.py
Line 15: @order_bp.route('/checkout', methods=['POST'])
Click line number → Red dot appears
```

**Step 2: Set Frontend Breakpoint**
```
Open: frontend/js/cart.js
Line 72: async function checkout() {
Click line number → Red dot appears
```

**Step 3: Start Backend Debug**
```
Press F5 or Debug → Start Debugging → Select "TechVault Backend"
Terminal shows: "Running on http://127.0.0.1:5000"
Backend pauses at breakpoint when hit
```

**Step 4: Start Frontend Server**
```
In new terminal tab:
cd frontend
python3 -m http.server 8000
```

**Step 5: Debug Frontend**
```
Open Chrome: http://localhost:8000/pages/index.html
Login → Add to cart → Click Checkout
Frontend pauses at line 72
Press F10 (Step over) to move through code
```

**Step 6: Watch Breakpoint Hit**
```
When checkout() calls API:
Backend breakpoint is hit automatically
Look at Variables panel on left
user_id, payment_method are visible
Press F10 to step through
```

---

## 4️⃣ USEFUL BREAKPOINT LOCATIONS

### Backend Breakpoints:

| File | Line | Function | Purpose |
|------|------|----------|---------|
| `routes/order.py` | 15 | `checkout()` | Trace order creation |
| `routes/order.py` | 63 | `update_order_status()` | Debug status update |
| `services/payment_strategy.py` | 13 | `CreditCardPayment.process_payment()` | STRATEGY pattern |
| `services/notification.py` | 23 | `notify_status_change()` | OBSERVER pattern |

### Frontend Breakpoints:

| File | Line | Function | Purpose |
|------|------|----------|---------|
| `js/cart.js` | 72 | `checkout()` | Trace checkout start |
| `js/orders.js` | 98 | `approveOrderPayment()` | Debug admin approval |
| `js/catalog.js` | 55 | `addToCart()` | Debug item addition |
| `js/auth.js` | 20 | `loginForm.submit` | Debug login |

---

## 5️⃣ QUICK DEBUG SESSION (5 min demo)

### Setup (1 minute)
```bash
# Terminal 1: Start backend with debugger
cd backend
python3 run.py

# Terminal 2: Start frontend
cd frontend
python3 -m http.server 8000
```

### Debug Frontend (2 minutes)
1. Open `frontend/js/cart.js`
2. Set breakpoint at line 72 (checkout)
3. Open browser: http://localhost:8000/pages/index.html
4. Login → Add to cart → Click Checkout
5. VS Code pauses at breakpoint
6. Show Variables panel (userId, paymentMethod)
7. Press F10 to step through

### Debug Backend (2 minutes)
1. Open `backend/app/routes/order.py`
2. Set breakpoint at line 15 (checkout route)
3. In paused frontend, press F5 (Continue)
4. API call hits backend breakpoint
5. Show Variables panel
6. Show console.log output in terminal
7. See STRATEGY pattern logs

---

## 6️⃣ TIPS & TRICKS

### Conditional Breakpoints

1. Right-click on breakpoint (red dot)
2. Click "Edit Breakpoint"
3. Add condition: `order_id == 5`
4. Breakpoint only pauses when condition is true

### Logpoints (Print without pause)

1. Right-click on line number
2. Click "Add Logpoint"
3. Type message: `"Checkout for user {user_id}"`
4. Executes silently, prints to console
5. No pause, perfect for production

### Debug Terminal Output

**Show all debug output:**
- Backend: Terminal shows print() statements
- Frontend: Debug Console shows console.log()
- Right-click → "Attach to running process" for existing apps

### Multi-Session Debugging

Keep both terminal tabs open:
- **Tab 1:** Backend Python (debug output)
- **Tab 2:** Frontend HTTP server
- **View → Debug Console:** Shows JS console.log()

---

## 7️⃣ COMMON DEBUG SCENARIOS

### Scenario 1: Order Not Creating

```
1. Set breakpoint in order.py line 25 (OrderRepository.create_order)
2. F5 → Start debugging
3. Checkout → Pauses at breakpoint
4. Hover over variables: user_id, total, payment_method
5. Step F10 → See order_id returned
6. If order_id is None/0 → Database issue
7. Check Database in SQLite
```

### Scenario 2: Payment Not Processing (STRATEGY Pattern)

```
1. Set breakpoint in payment_strategy.py line 13
2. Checkout in frontend
3. Pauses at PaymentProcessor init
4. Check: strategy.__class__.__name__
5. Should show "CreditCardPayment" or "CashOnDeliveryPayment"
6. F10 → Enter process_payment()
7. Watch return value
8. If success=True → Payment OK
9. If success=False → Payment failed
```

### Scenario 3: Status Not Updating (STATE Pattern)

```
1. Set breakpoint in order.py line 63
2. Admin clicks "Approve Payment"
3. Frontend pauses first at cart.js:98
4. F5 → Continue to backend breakpoint
5. Check: order_id, old_status, new_status
6. F10 → Step through update
7. Check database after update
```

### Scenario 4: localStorage Issue

```
1. In Debug Console, type:
   localStorage
2. See all stored values
3. Check: userId, userRole, username
4. Type: localStorage.getItem('userId')
5. If empty → Login not working
6. Set breakpoint in auth.js to debug login
```

---

## 8️⃣ DEBUG CONSOLE COMMANDS

### Check User Session (in Debug Console)
```javascript
localStorage.getItem('userId')      // User ID
localStorage.getItem('userRole')    // admin or customer
localStorage.getItem('username')    // Username
```

### Test API Calls (in Debug Console)
```javascript
// Get all products
APIClient.get('/catalog/products').then(p => console.log(p))

// Get user's orders
APIClient.get('/order/user/2').then(o => console.log(o))

// Add to cart
APIClient.post('/cart/add', {user_id: 2, product_id: 1, quantity: 1})
```

### Check DOM Elements (in Debug Console)
```javascript
document.getElementById('cart-total')        // Get cart total element
document.getElementById('products-grid')     // Get products container
document.querySelectorAll('.product-card')   // Get all product cards
```

---

## 9️⃣ TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| **Breakpoint not working** | Reload page (Cmd+R), ensure code matches |
| **Debug won't start** | Check `.vscode/launch.json` syntax |
| **Variables show "undefined"** | Breakpoint may be before variable declaration |
| **Frontend debug not attaching** | Kill Chrome, restart with `--remote-debugging-port=9222` |
| **Can't see console.log** | Open **Debug Console** (not terminal) |
| **Backend pauses unexpectedly** | Check for other breakpoints, use F5 to continue |

---

## 🔟 DEMONSTRATION SCRIPT (15 min)

```
[00:00] Show project structure in VS Code
[01:00] Open launch.json, explain configurations
[02:00] Set breakpoint in cart.js line 72
[03:00] Set breakpoint in order.py line 15
[04:00] F5 → Start backend debugging
[05:00] Open browser, login
[06:00] Add to cart, click Checkout
[07:00] Frontend pauses at breakpoint
[08:00] Show Variables panel, expand objects
[09:00] F10 to step through code
[10:00] API call triggers backend breakpoint
[11:00] Show backend Variables panel
[12:00] Demonstrate STRATEGY pattern in console output
[13:00] F10 to complete checkout
[14:00] Query database to verify order created
[15:00] Show console.log output visible in Debug Console
```

---

**You're ready to debug in VS Code! 🚀**
