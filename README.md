# TechVault - E-Commerce System with Design Patterns

A Software Design assignment demonstrating 5 Gang of Four design patterns in a fully functional e-commerce system with backend API and frontend UI.

## Quick Summary

- **Backend:** Flask REST API with 15 endpoints
- **Frontend:** 6 HTML pages + 6 JavaScript files
- **Database:** SQLite with 7 tables
- **Design Patterns:** 5 Gang of Four patterns (STRATEGY, STATE, OBSERVER, FACADE, FACTORY METHOD)
- **Architecture:** 3-layer (Routes → Services → Repositories)
- **Testing:** All 17 endpoints tested and passing ✅

---


## Installation & Setup

### Prerequisites by Platform

#### **Windows**
1. **Python 3.9+**
   - Download from: https://www.python.org/downloads/
   - **IMPORTANT:** Check "Add Python to PATH" during installation
   - Verify: Open Command Prompt and run `python --version`

2. **Git (Optional, for cloning)**
   - Download from: https://git-scm.com/download/win

3. **Text Editor/IDE (Optional)**
   - VS Code: https://code.visualstudio.com/
   - PyCharm Community: https://www.jetbrains.com/pycharm/

#### **macOS**
1. **Python 3.9+** (usually pre-installed)
   - Check: `python3 --version`
   - If not installed: `brew install python3`
   - Install Homebrew first: https://brew.sh/

2. **Homebrew (Recommended)**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Git (Recommended)**
   ```bash
   brew install git
   ```


## Running the Application

### Backend Setup & Run

#### **Windows**

1. **Open Command Prompt** (Win+R, type `cmd`)

2. **Navigate to project**
   ```cmd
   cd Documents\Software_Design\Project_Assignment\backend
   ```

3. **Create Python virtual environment** (Optional but recommended)
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

5. **Run the backend**
   ```cmd
   python run.py
   ```

   Expected output:
   ```
   Starting TechVault backend on http://localhost:5000
   ```

6. **Keep this window open** - the server will run here

---

#### **macOS**

1. **Open Terminal** (Cmd+Space, type `terminal`)

2. **Navigate to project**
   ```bash
   cd Documents/Software_Design/Project_Assignment/backend
   ```

3. **Create Python virtual environment** (Optional but recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run the backend**
   ```bash
   python3 run.py
   ```

   Expected output:
   ```
   Starting TechVault backend on http://localhost:5000
   ```

6. **Keep this terminal open** - the server will run here

- **Open Terminal** (Ctrl+Alt+T)

2. **Navigate to project**
   ```bash
   cd ~/Documents/Software_Design/Project_Assignment/backend
   ```

3. **Create Python virtual environment** (Optional but recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run the backend**
   ```bash
   python3 run.py
   ```

   Expected output:
   ```
   Starting TechVault backend on http://localhost:5000
   ```

6. **Keep this terminal open** - the server will run here


### Frontend Setup & Run

#### **Option 1: Open HTML Files Directly (Quickest)**

**Windows:**
1. Navigate to: `Documents\Software_Design\Project_Assignment\frontend\pages`
2. Right-click `index.html`
3. Select "Open with" → Choose your browser (Chrome, Firefox, Edge, Safari)

**macOS:**
1. Open Finder
2. Navigate to: `Documents/Software_Design/Project_Assignment/frontend/pages`
3. Double-click `index.html` (opens in default browser)
4. Or right-click → "Open With" → Choose browser


---

#### **Option 2: Use Python HTTP Server (Recommended for Testing)**

**Windows:**

1. **Open Command Prompt** in the frontend directory
   ```cmd
   cd Documents\Software_Design\Project_Assignment\frontend
   python -m http.server 8000
   ```

2. **Open browser** and visit: `http://localhost:8000/pages/index.html`

**macOS:**

1. **Open Terminal** in the frontend directory
   ```bash
   cd Documents/Software_Design/Project_Assignment/frontend
   python3 -m http.server 8000
   ```

2. **Open browser** and visit: `http://localhost:8000/pages/index.html`


### Complete Workflow (All Platforms)

**Terminal 1 - Backend (Keep running):**
```bash
cd backend
python3 run.py    # or just 'python' on Windows
# Output: Starting TechVault backend on http://localhost:5000
```

**Terminal 2 - Frontend (or just open in browser):**
```bash
cd frontend
python3 -m http.server 8000
# Then visit: http://localhost:8000/pages/index.html
```

**Now you can:**
1. ✅ Browse products
2. ✅ Register/login
3. ✅ Add items to cart
4. ✅ Checkout with payment method selection (STRATEGY pattern)
5. ✅ Track order status (STATE + OBSERVER patterns)
6. ✅ View admin dashboard (FACADE + FACTORY patterns)

---

## Database Management

### Database Persistence ✅

**IMPORTANT:** The database **PERSISTS across sessions**

- **Once you create data, it stays there** (until you delete the database file)
- Users, orders, cart items are all saved permanently
- Database is stored as: `backend/app/data_access/techvault.db`
- Closing and restarting the backend does NOT delete data
- The same data will be there when you restart

**Example:**
1. Create user account "john" → saved to database
2. Stop backend server
3. Start backend again
4. User "john" still exists ✅

---

### How to Check/View Database

#### **Option 1: SQLite Browser (Easiest - Recommended)**

1. **Download SQLite Browser**
   - Website: https://sqlitebrowser.org/
   - Works on Windows, macOS, Linux

2. **Open the database file**
   - Navigate to: `backend/app/data_access/techvault.db`
   - Right-click → "Open with SQLite Browser"

3. **Browse tables**
   - Click on "Browse Data" tab
   - Select table from dropdown:
     - `users` - See all registered users
     - `product` - See products
     - `orders` - See placed orders
     - `cart_item` - See items in carts
     - `order_item` - See items in orders
     - `category` - See product categories

4. **View data**
   - See all columns and values
   - Edit data directly if needed
   - Changes save automatically

---

#### **Option 2: SQL Queries (Command Line)**

**Windows:**
```cmd
# Navigate to backend
cd Documents\Software_Design\Project_Assignment\backend

# View all users
sqlite3 app\data_access\techvault.db "SELECT * FROM users;"

# View all orders
sqlite3 app\data_access\techvault.db "SELECT * FROM orders;"

# View specific user
sqlite3 app\data_access\techvault.db "SELECT * FROM users WHERE username='john';"
```

**macOS/Linux:**
```bash
# Navigate to backend
cd Documents/Software_Design/Project_Assignment/backend

# View all users
sqlite3 app/data_access/techvault.db "SELECT * FROM users;"

# View all orders
sqlite3 app/data_access/techvault.db "SELECT * FROM orders;"

# View specific user
sqlite3 app/data_access/techvault.db "SELECT * FROM users WHERE username='john';"
```

---

#### **Option 3: Python Script (Advanced)**

**Create file: `backend/check_db.py`**

```python
import sqlite3

db_path = 'app/data_access/techvault.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check users
print("=== USERS ===")
cursor.execute("SELECT id, username, email, role FROM users;")
users = cursor.fetchall()
for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")

# Check orders
print("\n=== ORDERS ===")
cursor.execute("SELECT id, user_id, total_amount, status FROM orders;")
orders = cursor.fetchall()
for order in orders:
    print(f"ID: {order[0]}, User: {order[1]}, Amount: ${order[2]}, Status: {order[3]}")

# Check products
print("\n=== PRODUCTS ===")
cursor.execute("SELECT id, name, price, stock FROM product;")
products = cursor.fetchall()
for product in products:
    print(f"ID: {product[0]}, Name: {product[1]}, Price: ${product[2]}, Stock: {product[3]}")

conn.close()
```

**Run it:**
```bash
python3 check_db.py
```

---

### Common Database Queries

#### **View All Users**
```sql
SELECT id, username, email, role, created_at FROM users;
```

#### **View All Orders**
```sql
SELECT id, user_id, total_amount, status, created_at FROM orders;
```

#### **View Cart Items**
```sql
SELECT c.id, c.user_id, p.name, c.quantity, p.price FROM cart_item c JOIN product p ON c.product_id = p.id;
```

#### **View User's Orders**
```sql
SELECT * FROM orders WHERE user_id = 1;
```

#### **View Order Details with Items**
```sql
SELECT o.id, o.status, oi.product_id, p.name, oi.quantity, oi.unit_price 
FROM orders o 
JOIN order_item oi ON o.id = oi.order_id 
JOIN product p ON oi.product_id = p.id 
WHERE o.id = 1;
```

#### **Count Total Users**
```sql
SELECT COUNT(*) as total_users FROM users;
```

#### **Count Total Orders**
```sql
SELECT COUNT(*) as total_orders FROM orders;
```

#### **View Products with Low Stock**
```sql
SELECT id, name, stock FROM product WHERE stock < 5;
```

---

### Reset Database

#### **Option 1: Delete Database File (Full Reset)**

1. **Locate database file:**
   ```
   backend/app/data_access/techvault.db
   ```

2. **Delete it:**
   - Right-click → Delete (or move to trash)

3. **Restart backend:**
   ```bash
   python3 run.py
   ```
   - Backend will auto-create fresh database
   - Sample data will be re-seeded
   - All previous data is gone ❌

---

#### **Option 2: Clear Specific Tables (Keep Database)**

**Keep database structure, clear data:**

```sql
DELETE FROM cart_item;
DELETE FROM order_item;
DELETE FROM orders;
DELETE FROM users;
DELETE FROM product;
DELETE FROM category;
```

**Then re-seed:**
```sql
INSERT INTO category (name, description) VALUES 
('Electronics', 'Electronic devices and gadgets'),
('Clothing', 'Apparel and accessories'),
('Books', 'Educational and recreational books');

INSERT INTO product (name, description, price, category_id, stock) VALUES
('Laptop Pro', 'High-performance laptop', 999.99, 1, 10),
('Wireless Mouse', 'Ergonomic mouse', 29.99, 1, 50),
('T-Shirt', 'Cotton t-shirt', 19.99, 2, 100),
('Python Book', 'Learn Python Programming', 39.99, 3, 25);
```

---

#### **Option 3: Keep Everything (Normal Operation)**

**Just keep using it:**
- Data persists automatically
- No action needed
- Everything you create stays

### Database Facts

| Aspect | Details |
|--------|---------|
| **Type** | SQLite (file-based) |
| **Location** | `backend/app/data_access/techvault.db` |
| **Persists?** | ✅ YES - Data stays between sessions |
| **Auto-creates?** | ✅ YES - On first backend run |
| **Tables** | 7 (users, products, orders, etc.) |
| **Backup** | Copy `.db` file to backup |
| **Reset** | Delete `.db` file to start fresh |
| **Size** | Small (~100KB for demo data) |

---

### Troubleshooting Database

#### **"Database locked" error**
- **Cause:** Two programs accessing database simultaneously
- **Solution:** 
  - Close SQLite Browser
  - Stop all other connections
  - Restart backend

#### **"Table already exists" error**
- **Cause:** Schema mismatch or corrupted database
- **Solution:** Delete `techvault.db` and restart backend

#### **Missing data**
- **Cause:** Viewing wrong database or file deleted
- **Check:** Verify file path: `backend/app/data_access/techvault.db`
- **Verify:** Run: `sqlite3 techvault.db ".tables"` to list tables

#### **Can't see new data I just created**
- **Cause:** Data not committed or viewing old database
- **Solution:** 
  - Refresh SQLite Browser
  - Check correct database file
  - Verify backend is running

---

## Testing the API

### Using Python Test Suite (Recommended)

**All Platforms:**

1. **Make sure backend is running** (see Backend Setup above)

2. **Open new terminal/command prompt** in backend folder
   ```bash
   python3 test_endpoints.py
   ```

3. **Expected output:**
   ```
   ✓ Connected to API on localhost:5000
   [TEST 1] Register New User
   [TEST 2] Login User
   ... (17 total tests)
   All Tests Completed! ✅
   ```

---

### Using curl (Command Line)

**Windows:**
```cmd
# Register
curl -X POST http://localhost:5000/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"john\",\"email\":\"john@example.com\",\"password\":\"123456\"}"

# Browse products
curl http://localhost:5000/api/catalog/products
```

**macOS/Linux:**
```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"123456"}'

# Browse products
curl http://localhost:5000/api/catalog/products
```

---

### Using Postman (GUI Tool)

1. **Download Postman**: https://www.postman.com/downloads/
2. **Open Postman**
3. **Create new request:**
   - Method: `POST`
   - URL: `http://localhost:5000/api/auth/register`
   - Body (JSON): `{"username":"john","email":"john@example.com","password":"123456"}`
4. **Click Send** to test

---

## API Endpoints

### Authentication (3)
```
POST   /api/auth/register              # Register new user
POST   /api/auth/login                 # Login user
GET    /api/auth/profile/<user_id>     # Get user profile
```

### Catalog (4)
```
GET    /api/catalog/products                        # All products
GET    /api/catalog/products/<id>                   # Product details
GET    /api/catalog/categories                      # All categories
GET    /api/catalog/categories/<id>/products        # Products by category
```

### Shopping Cart (4)
```
POST   /api/cart/add                   # Add item to cart
POST   /api/cart/remove                # Remove item
GET    /api/cart/<user_id>             # View cart
POST   /api/cart/clear/<user_id>       # Clear cart
```

### Orders (4)
```
POST   /api/order/checkout             # Create order (STRATEGY pattern)
GET    /api/order/<order_id>           # Get order details
GET    /api/order/user/<user_id>       # Get user's orders
PUT    /api/order/<order_id>/status/<status>  # Update status (OBSERVER)
```

---

## Design Patterns Implemented

| Pattern | File | Purpose |
|---------|------|---------|
| **STRATEGY** | `services/payment_strategy.py` | Credit Card / Cash on Delivery payment methods |
| **STATE** | `services/order_state.py` | Order lifecycle (Pending → Paid → Shipped → Received) |
| **OBSERVER** | `services/notification.py` | Notify on status changes (Email, SMS) |
| **FACADE** | `services/admin_service.py` | Simplified admin interface |
| **FACTORY METHOD** | `services/dashboard_factory.py` | Create customer/admin dashboards by role |

---

## Troubleshooting

### "Python not found" (Windows)
- **Solution:** Add Python to PATH during installation
- Or use `python3` instead of `python`
- Or reinstall Python checking "Add to PATH"

### "Port 5000 already in use"
- **Solution:** Change port in `run.py` or kill process using port 5000
  
  **Windows:**
  ```cmd
  netstat -ano | findstr :5000
  taskkill /PID <PID> /F
  ```
  
  **macOS/Linux:**
  ```bash
  lsof -i :5000
  kill -9 <PID>
  ```

### "Module not found" error
- **Solution:** Make sure you installed requirements
  ```bash
  pip3 install -r requirements.txt
  ```

### Frontend can't connect to API
- **Make sure backend is running** on `http://localhost:5000`
- Check browser console (F12) for errors
- Enable CORS (already configured in Flask)

### Database not found
- **Solution:** Backend auto-creates it on first run
- Delete `backend/app/data_access/techvault.db` to reset

---

## File Locations (For Reference)

### Windows
```
Backend:   C:\Users\<YourUsername>\Documents\Software_Design\Project_Assignment\backend
Frontend:  C:\Users\<YourUsername>\Documents\Software_Design\Project_Assignment\frontend
Database:  C:\Users\<YourUsername>\Documents\Software_Design\Project_Assignment\backend\app\data_access\techvault.db
```

### macOS
```
Backend:   ~/Documents/Software_Design/Project_Assignment/backend
Frontend:  ~/Documents/Software_Design/Project_Assignment/frontend
Database:  ~/Documents/Software_Design/Project_Assignment/backend/app/data_access/techvault.db
```


## Key Features

✅ **3-Layer Architecture** - Clean separation of concerns  
✅ **15 API Endpoints** - Complete e-commerce functionality  
✅ **5 Design Patterns** - Real-world implementations  
✅ **SQLite Database** - 7 tables with relationships  
✅ **Responsive UI** - 6 pages with modern design  
✅ **Full Test Suite** - All endpoints tested  
✅ **Cross-Platform** - Works on Windows, macOS, Linux  

---

## Sample Data

**Auto-loaded on first run:**
- 3 Categories (Electronics, Clothing, Books)
- 4 Products (Laptop Pro, Mouse, T-Shirt, Python Book)
- Ready to browse and purchase

---

## Next Steps

1. ✅ Run backend: `python3 run.py`
2. ✅ Open frontend: `http://localhost:8000/pages/index.html`
3. ✅ Register new user
4. ✅ Browse products
5. ✅ Add to cart
6. ✅ Checkout (see STRATEGY pattern in action)
7. ✅ Track order (see STATE & OBSERVER patterns)

---

**Assignment Status:** ✅ Complete  
**Deadline:** June 16, 2026  
**Total Implementation:** 40+ files, 5 design patterns, 3-layer architecture
