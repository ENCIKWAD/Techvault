# TechVault - User & Admin Data Guide

How to create and manage user accounts, including admin accounts.

---

## User Database Schema

### `users` Table Structure

```
Column    | Type    | Default  | Description
----------|---------|----------|------------------
id        | INTEGER | AUTO     | Primary key
username  | TEXT    | UNIQUE   | User's username
email     | TEXT    | UNIQUE   | User's email
password  | TEXT    | REQUIRED | Password (stored plain text - NOT SECURE)
role      | TEXT    | customer | User role (customer or admin)
created_at| TIMESTAMP| NOW     | Account creation time
```

---

## Pre-Seeded Data

### ⚠️ IMPORTANT
**NO default user accounts are pre-created.** You must register users manually.

**Sample product data IS created:**
```
Categories: Electronics, Clothing, Books
Products:  Laptop Pro, Wireless Mouse, T-Shirt, Python Book
```

---

## How to Create Users

### Method 1: Register via Frontend (Easiest)

1. **Start the backend:**
   ```bash
   python3 run.py
   ```

2. **Open frontend:**
   - Navigate to: `http://localhost:8000/pages/register.html`

3. **Fill registration form:**
   - Username: `testuser` (any name)
   - Email: `test@example.com` (any email)
   - Password: `password123` (any password)

4. **Click Register**
   - Account created automatically
   - Role set to `customer` by default
   - Redirects to login page

---

### Method 2: Register via curl (Windows, macOS, Linux)

**Windows:**
```cmd
curl -X POST http://localhost:5000/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"john\",\"email\":\"john@example.com\",\"password\":\"password123\"}"
```

**macOS/Linux:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"password123"}'
```

**Response:**
```json
{
  "success": true
}
```

---

### Method 3: Register via Postman

1. **Open Postman**
2. **Create new request:**
   - Method: `POST`
   - URL: `http://localhost:5000/api/auth/register`
3. **Body (JSON):**
   ```json
   {
     "username": "john",
     "email": "john@example.com",
     "password": "password123"
   }
   ```
4. **Click Send**

---

## Creating Admin Users

### ⚠️ LIMITATION
The API doesn't have an endpoint to create admin users. You have two options:

### Option 1: Direct Database Modification (RECOMMENDED FOR DEMO)

**All Platforms:**

1. **Install SQLite browser (optional but recommended)**
   - Download: https://sqlitebrowser.org/

2. **Locate database:**
   ```
   Windows:  Documents\Software_Design\Project_Assignment\backend\app\data_access\techvault.db
   macOS:    Documents/Software_Design/Project_Assignment/backend/app/data_access/techvault.db
   Linux:    ~/Documents/Software_Design/Project_Assignment/backend/app/data_access/techvault.db
   ```

3. **Open with SQLite Browser:**
   - Open the .db file
   - Go to "Execute SQL" tab
   - Run this query:

   ```sql
   UPDATE users SET role = 'admin' WHERE id = 1;
   ```

   Or create new admin directly:

   ```sql
   INSERT INTO users (username, email, password, role) 
   VALUES ('admin', 'admin@example.com', 'admin123', 'admin');
   ```

4. **Save and close**
5. **Restart backend** - it will use updated data

---

### Option 2: Modify Code (PERMANENT SOLUTION)

**Edit `backend/app/data_access/seed.py`:**

Find this section:
```python
def seed_data():
    conn = get_db()
    cursor = conn.cursor()

    try:
        # Add sample categories
        categories = [...]
        cursor.executemany('INSERT INTO category ...', categories)
        
        # Add sample products
        products = [...]
        cursor.executemany('INSERT INTO product ...', products)
```

Add this after products:
```python
        # Add admin user
        admin_user = [
            ('admin', 'admin@example.com', 'admin123', 'admin'),
        ]
        cursor.executemany(
            'INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
            admin_user
        )
```

Then:
1. **Delete the database** to force recreation:
   ```
   backend/app/data_access/techvault.db
   ```
2. **Run backend** - it will recreate with admin user

---

## Default Test Accounts

### Create These Test Accounts

#### Customer Account
```
Username: customer
Email:    customer@example.com
Password: password123
Role:     customer (default)
```

#### Admin Account
```
Username: admin
Email:    admin@example.com
Password: admin123
Role:     admin (must set via database)
```

#### Test Account
```
Username: testuser
Email:    test@example.com
Password: password123
Role:     customer (default)
```

---

## How to Login

### Via Frontend

1. **Navigate to login page:**
   ```
   http://localhost:8000/pages/register.html
   ```

2. **Fill login form:**
   - Email: (your registered email)
   - Password: (your password)

3. **Click Login**
   - Stores `userId` in browser localStorage
   - Redirects to product catalog

---

### Via curl (Testing)

**Windows:**
```cmd
curl -X POST http://localhost:5000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@example.com\",\"password\":\"admin123\"}"
```

**macOS/Linux:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "role": "admin"
}
```

---

## User Storage

### Browser Storage (Frontend)

When you login, the frontend stores:
```javascript
localStorage.setItem('userId', result.id);        // User ID
localStorage.setItem('userRole', result.role);    // User role (customer/admin)
```

These are used to:
- Determine which pages to show
- Restrict access to admin features
- Track which user is logged in

### Check Your Login Status

**In browser console (F12):**
```javascript
localStorage.getItem('userId')    // Returns: "1"
localStorage.getItem('userRole')  // Returns: "admin" or "customer"
```

### Logout

```javascript
localStorage.removeItem('userId');
localStorage.removeItem('userRole');
// Then navigate to login page
```

---

## Different User Views

### Customer View (Role: customer)

**Can access:**
- ✅ Browse products
- ✅ View categories
- ✅ Shopping cart
- ✅ Checkout (place orders)
- ✅ Track orders
- ❌ Admin dashboard (blocked)

**Available pages:**
- index.html (products)
- cart.html (shopping)
- orders.html (tracking)

---

### Admin View (Role: admin)

**Can access:**
- ✅ All customer features
- ✅ Admin dashboard
- ✅ View statistics
- ✅ Manage pending orders
- ✅ View inventory report
- ✅ Update order status

**Available pages:**
- index.html (products)
- cart.html (shopping)
- orders.html (tracking)
- admin.html (dashboard) ⭐

---

## Database Queries

### View All Users

```sql
SELECT id, username, email, role, created_at FROM users;
```

### View Customers Only

```sql
SELECT * FROM users WHERE role = 'customer';
```

### View Admin Only

```sql
SELECT * FROM users WHERE role = 'admin';
```

### Change User to Admin

```sql
UPDATE users SET role = 'admin' WHERE id = 1;
```

### Change Admin to Customer

```sql
UPDATE users SET role = 'customer' WHERE id = 1;
```

### Delete User

```sql
DELETE FROM users WHERE id = 1;
```

### Reset All Users (Keep data, remove accounts)

```sql
DELETE FROM users;
DELETE FROM sqlite_sequence WHERE name='users';
```

---

## Security Notes

⚠️ **IMPORTANT - NOT PRODUCTION READY**

Current implementation has security issues:

1. **Passwords stored in plain text**
   - ❌ Should use bcrypt or argon2
   - ❌ Currently: `password` stored as-is
   - ✅ Fix: Use hashing library

2. **No password validation**
   - ❌ Can be empty, too short, weak
   - ✅ Fix: Add validation rules

3. **No JWT authentication**
   - ❌ Using localStorage (client-side)
   - ❌ No session validation on backend
   - ✅ Fix: Implement JWT tokens

4. **No HTTPS**
   - ❌ Credentials sent over HTTP
   - ✅ Fix: Use HTTPS in production

5. **No rate limiting**
   - ❌ Can brute force passwords
   - ✅ Fix: Implement rate limiting

**For assignment:** This is acceptable as a demo  
**For production:** These must be fixed!

---

## Testing Workflow

### 1. Create Customer Account

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"customer1","email":"customer@example.com","password":"pass123"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"customer@example.com","password":"pass123"}'

# Response will show user ID, use in next requests
```

### 2. Create Admin Account (via database)

```sql
INSERT INTO users (username, email, password, role) 
VALUES ('admin1', 'admin@example.com', 'admin123', 'admin');
```

### 3. Login as Admin

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

### 4. Test Different Features

**As Customer:**
- Browse products
- Add to cart
- Checkout
- View orders

**As Admin:**
- All above features
- View admin dashboard
- Manage orders
- View inventory

---

## Sample Test Data to Create

### Accounts

| Username | Email | Password | Role |
|----------|-------|----------|------|
| customer1 | customer1@test.com | pass123 | customer |
| customer2 | customer2@test.com | pass123 | customer |
| admin1 | admin1@test.com | pass123 | admin |
| testuser | test@test.com | pass123 | customer |

### How to Create All at Once

1. **Register customers via frontend or curl**
2. **Update one to admin via SQL:**
   ```sql
   UPDATE users SET role = 'admin' WHERE username = 'admin1';
   ```

---

## Troubleshooting

### "User already exists" error
- Email must be unique
- Try different email: `newuser@example.com`

### "Invalid credentials" on login
- Double-check email spelling (case-sensitive in some systems)
- Make sure password is correct
- Try all lowercase for email

### Can't access admin page
- User must have `role = 'admin'`
- Check database: `SELECT * FROM users WHERE id = 1;`
- Update if needed: `UPDATE users SET role = 'admin' WHERE id = 1;`

### Lost login session
- Clear browser localStorage: `localStorage.clear()`
- Login again

### Need to reset everything
- Delete `techvault.db`
- Restart backend - it recreates with fresh data
- Register new accounts

---

## Summary

| Task | Method |
|------|--------|
| **Register User** | Frontend form or curl |
| **Login** | Frontend form or curl |
| **Create Admin** | SQL database update (no API endpoint) |
| **View Users** | SQL query or SQLite Browser |
| **Delete User** | SQL query or SQLite Browser |
| **Reset Database** | Delete .db file and restart |

---

**Next Steps:**
1. Start backend: `python3 run.py`
2. Create a customer account via registration
3. Create an admin account via database
4. Test both account types
5. Explore features as each role

---

Last updated: June 16, 2026
