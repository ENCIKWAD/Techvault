# TechVault - Database Management Guide

Complete guide to understanding, viewing, and managing the SQLite database.

---

## Quick Answer: Does Data Persist?

# ✅ YES - Data PERSISTS Between Sessions

**Once you create data, it stays there permanently** (unless you delete the database file)

### Example:
```
Session 1:
- Create user "john@example.com" ✓
- Backend stops

Session 2 (same day, next week, next month):
- Start backend again
- User "john@example.com" still exists ✓
- All orders, cart items saved ✓
```

---

## Database Location

### File Path


---

## Database Structure

### 7 Tables

#### 1. `users` - User Accounts
```
id (PK)      | INTEGER | User ID
username     | TEXT    | Username
email        | TEXT    | Email address
password     | TEXT    | Password (plain text)
role         | TEXT    | 'customer' or 'admin'
created_at   | TEXT    | Account creation time
```

---

#### 2. `category` - Product Categories
```
id (PK)      | INTEGER | Category ID
name         | TEXT    | Category name (UNIQUE)
description  | TEXT    | Category description
```



---

#### 3. `product` - Products in Catalog
```
id (PK)      | INTEGER | Product ID
name         | TEXT    | Product name
description  | TEXT    | Product description
price        | REAL    | Price in dollars
category_id  | INTEGER | Foreign key → category.id
stock        | INTEGER | Quantity in stock
created_at   | TEXT    | Creation time
```


---

#### 4. `product_variant` - Product Variations
```
id (PK)      | INTEGER | Variant ID
product_id   | INTEGER | Foreign key → product.id
size         | TEXT    | Size (S, M, L, XL)
color        | TEXT    | Color (red, blue, etc)
stock        | INTEGER | Variant stock level
```

**Status:** Pre-created but not actively used in demo

---

#### 5. `cart_item` - Shopping Cart Items
```
id (PK)      | INTEGER | Item ID
user_id      | INTEGER | Foreign key → users.id
product_id   | INTEGER | Foreign key → product.id
quantity     | INTEGER | Quantity in cart
added_at     | TEXT    | When added to cart
```


---

#### 6. `orders` - Customer Orders
```
id (PK)      | INTEGER | Order ID
user_id      | INTEGER | Foreign key → users.id
total_amount | REAL    | Total price
status       | TEXT    | pending/paid/shipped/received
payment_method | TEXT  | 'card' or 'cod'
created_at   | TEXT    | Order creation time
updated_at   | TEXT    | Last status update time
```


---

#### 7. `order_item` - Items in Each Order
```
id (PK)      | INTEGER | Item ID
order_id     | INTEGER | Foreign key → orders.id
product_id   | INTEGER | Foreign key → product.id
quantity     | INTEGER | Quantity ordered
unit_price   | REAL    | Price at time of order
```
---

## How to View Database

### Method 1: SQLite Browser (Easiest) ⭐ RECOMMENDED

**Step 1: Download SQLite Browser**
- Website: https://sqlitebrowser.org/
- Available for Windows, macOS, Linux
- Free and open-source

**Step 2: Open Database File**
1. Launch SQLite Browser
2. File → Open Database
3. Navigate to: `backend/app/data_access/techvault.db`
4. Click "Open"

**Step 3: Browse Tables**
1. Click "Browse Data" tab
2. Select table from dropdown
3. See all rows and columns
4. Can edit values directly
5. Changes save automatically

**Tables to explore:**
- `users` - See registered accounts
- `product` - See product catalog
- `orders` - See placed orders
- `cart_item` - See shopping cart contents
- `order_item` - See items in each order

---

### Method 2: Command Line (Windows, macOS, Linux)

**Windows - Command Prompt:**

```cmd
# Navigate to backend folder
cd Documents\Software_Design\Project_Assignment\backend

# View all users
sqlite3 app\data_access\techvault.db "SELECT * FROM users;"

# View all products
sqlite3 app\data_access\techvault.db "SELECT * FROM product;"

# View all orders
sqlite3 app\data_access\techvault.db "SELECT * FROM orders;"

# Count records
sqlite3 app\data_access\techvault.db "SELECT COUNT(*) FROM users;"
```

**macOS/Linux - Terminal:**

```bash
# Navigate to backend folder
cd Documents/Software_Design/Project_Assignment/backend

# View all users
sqlite3 app/data_access/techvault.db "SELECT * FROM users;"

# View all products
sqlite3 app/data_access/techvault.db "SELECT * FROM product;"

# View all orders
sqlite3 app/data_access/techvault.db "SELECT * FROM orders;"

# Count records
sqlite3 app/data_access/techvault.db "SELECT COUNT(*) FROM users;"
```

---

### Method 3: Interactive SQLite Shell (Advanced)

**Windows:**

```cmd
cd Documents\Software_Design\Project_Assignment\backend
sqlite3 app\data_access\techvault.db
```

Then at the `sqlite>` prompt:

```sql
.tables                  -- List all tables
SELECT * FROM users;     -- View all users
SELECT * FROM orders;    -- View all orders
.quit                    -- Exit
```

**macOS/Linux:**

```bash
cd Documents/Software_Design/Project_Assignment/backend
sqlite3 app/data_access/techvault.db
```

Then at the `sqlite>` prompt:

```sql
.tables                  -- List all tables
SELECT * FROM users;     -- View all users
SELECT * FROM orders;    -- View all orders
.quit                    -- Exit
```

---

## Useful SQL Queries

### Users

```sql
-- View all users
SELECT id, username, email, role FROM users;

-- View customers only
SELECT * FROM users WHERE role = 'customer';

-- View admin only
SELECT * FROM users WHERE role = 'admin';

-- Count users
SELECT COUNT(*) as total_users FROM users;

-- Find specific user
SELECT * FROM users WHERE email = 'john@example.com';
```

### Products

```sql
-- View all products
SELECT id, name, price, stock FROM product;

-- View products by category
SELECT p.id, p.name, c.name as category, p.price, p.stock 
FROM product p 
JOIN category c ON p.category_id = c.id;

-- View low stock items
SELECT id, name, stock FROM product WHERE stock < 5;

-- Total inventory value
SELECT SUM(price * stock) as total_value FROM product;
```

### Orders

```sql
-- View all orders
SELECT id, user_id, total_amount, status FROM orders;

-- View orders by user
SELECT * FROM orders WHERE user_id = 1;

-- View pending orders
SELECT * FROM orders WHERE status = 'pending';

-- View shipped orders
SELECT * FROM orders WHERE status = 'shipped';

-- Order count by status
SELECT status, COUNT(*) as count FROM orders GROUP BY status;

-- Total revenue
SELECT SUM(total_amount) as revenue FROM orders WHERE status = 'paid';
```

### Cart

```sql
-- View cart items
SELECT c.id, c.user_id, p.name, c.quantity, p.price 
FROM cart_item c 
JOIN product p ON c.product_id = p.id;

-- View specific user's cart
SELECT p.name, c.quantity, p.price, (c.quantity * p.price) as subtotal
FROM cart_item c
JOIN product p ON c.product_id = p.id
WHERE c.user_id = 1;

-- Cart total for user
SELECT SUM(c.quantity * p.price) as cart_total
FROM cart_item c
JOIN product p ON c.product_id = p.id
WHERE c.user_id = 1;
```

### Order Details

```sql
-- View items in specific order
SELECT o.id as order_id, o.status, p.name, oi.quantity, oi.unit_price, 
       (oi.quantity * oi.unit_price) as item_total
FROM orders o
JOIN order_item oi ON o.id = oi.order_id
JOIN product p ON oi.product_id = p.id
WHERE o.id = 1;

-- Order history with items for user
SELECT o.id as order_id, o.status, o.created_at, o.total_amount,
       p.name, oi.quantity
FROM orders o
JOIN order_item oi ON o.id = oi.order_id
JOIN product p ON oi.product_id = p.id
WHERE o.user_id = 1
ORDER BY o.created_at DESC;
```

---

## Modify Database

### Update User Role to Admin

```sql
UPDATE users SET role = 'admin' WHERE id = 1;
```

### Change User Password

```sql
UPDATE users SET password = 'newpassword123' WHERE id = 1;
```

### Update Product Stock

```sql
UPDATE product SET stock = 100 WHERE id = 1;
```

### Update Order Status

```sql
UPDATE orders SET status = 'shipped' WHERE id = 1;
```

### Delete User

```sql
DELETE FROM users WHERE id = 1;
```

### Delete Order

```sql
DELETE FROM orders WHERE id = 1;
```

---

## Reset Database

### Option 1: Full Reset (Recommended for Testing)

**Delete everything and start fresh:**

1. **Close SQLite Browser** (if open)
2. **Delete database file:**
   - Navigate to: `backend/app/data_access/techvault.db`
   - Right-click → Delete (or move to trash)
3. **Restart backend:**
   ```bash
   python3 run.py
   ```
4. **Backend will:**
   - Auto-detect missing database ✓
   - Create new database ✓
   - Re-seed sample data ✓
   - Start fresh ✓

**Time to complete:** < 5 seconds

---

### Option 2: Clear Tables Only (Keep Structure)

**Keep database structure, delete all data:**

```sql
-- Delete all data (keep table structure)
DELETE FROM cart_item;
DELETE FROM order_item;
DELETE FROM orders;
DELETE FROM users;
DELETE FROM product;
DELETE FROM category;

-- Reset auto-increment IDs
DELETE FROM sqlite_sequence;
```

**Then re-seed sample data:**

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

### Option 3: Selective Clear (Keep Specific Data)

**Keep users and products, clear orders:**

```sql
DELETE FROM order_item;
DELETE FROM orders;
DELETE FROM cart_item;
-- Users and products stay intact
```

---

## Backup Database

### Create Backup

**Windows:**
```cmd
# Copy database to backup folder
copy "Documents\Software_Design\Project_Assignment\backend\app\data_access\techvault.db" "Documents\backup\techvault_backup.db"
```

**macOS/Linux:**
```bash
# Copy database to backup folder
cp ~/Documents/Software_Design/Project_Assignment/backend/app/data_access/techvault.db ~/Documents/backup/techvault_backup.db
```

### Restore from Backup

**Windows:**
```cmd
copy "Documents\backup\techvault_backup.db" "Documents\Software_Design\Project_Assignment\backend\app\data_access\techvault.db"
```

**macOS/Linux:**
```bash
cp ~/Documents/backup/techvault_backup.db ~/Documents/Software_Design/Project_Assignment/backend/app/data_access/techvault.db
```

---

## Database Facts Summary

| Aspect | Detail |
|--------|--------|
| **Type** | SQLite (file-based relational database) |
| **File** | `techvault.db` |
| **Location** | `backend/app/data_access/` |
| **Size** | ~100KB (for demo data) |
| **Tables** | 7 |
| **Persists?** | ✅ YES - Between sessions, across reboots |
| **Auto-creates?** | ✅ YES - First run creates everything |
| **Auto-backup?** | ❌ NO - Backup manually if important |
| **Corrupt recovery?** | Delete file and recreate |

---

## Troubleshooting

### "Database is locked" error
- **Cause:** Two programs accessing simultaneously
- **Fix:** Close SQLite Browser, stop other connections, restart backend

### "Table doesn't exist" error
- **Cause:** Wrong database file or corrupted
- **Fix:** Delete `.db` file, restart backend

### "No data showing up"
- **Cause:** Viewing wrong database or data not committed
- **Fix:** Refresh SQLite Browser, verify correct file path

### "Can I see data from API calls?"
- **Answer:** ✅ YES - All data created via API is in database
- **How:** Open database file with SQLite Browser or SQL queries

### "When does data save?"
- **Answer:** Immediately after API call completes
- **View:** Open database while backend is running (SQLite allows read during writes)

### "Can I edit data while backend is running?"
- **Answer:** ✅ YES - Safe to edit with SQLite Browser while backend is running
- **Caution:** Don't delete tables or core data while in use

---

## Quick Commands Reference

### View Database

```bash
# Simple user listing
sqlite3 app/data_access/techvault.db "SELECT username, email FROM users;"

# Orders with amounts
sqlite3 app/data_access/techvault.db "SELECT id, total_amount, status FROM orders;"

# Product inventory
sqlite3 app/data_access/techvault.db "SELECT name, stock FROM product;"
```

### Reset Database

```bash
# Delete and recreate (simplest method)
rm app/data_access/techvault.db
python3 run.py
```

### Backup Database

```bash
# Copy to backup
cp app/data_access/techvault.db app/data_access/techvault_backup.db
```

---

## Persistence Examples

### Example 1: Create User, Stop Server, Restart

```
Time 1:00 PM:
- Start backend: python3 run.py
- Register user: john@example.com
- Stop backend: Ctrl+C

Time 2:00 PM (same day):
- Start backend: python3 run.py
- User john@example.com STILL EXISTS ✓
- All orders STILL THERE ✓

Time Next Week:
- Start backend: python3 run.py
- User john@example.com STILL EXISTS ✓
- Data persists across weeks ✓
```

### Example 2: Create Order, Restart, View

```
Time 10:00 AM:
- User places order #1 ($100)
- Backend saves to database

Time 10:30 AM:
- Restart backend
- Query database: SELECT * FROM orders;
- Order #1 still there with $100 ✓

Time Tomorrow:
- Order #1 still there ✓
- Can continue from where left off ✓
```

---

## Summary

✅ **Data persists between sessions** - You don't lose anything when stopping backend  
✅ **Easy to view** - SQLite Browser makes it simple  
✅ **Easy to reset** - Delete .db file and restart  
✅ **Safe to edit** - Direct database edits possible while running  
✅ **Backupable** - Just copy the .db file  

---

Last updated: June 16, 2026
