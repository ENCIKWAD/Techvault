# TechVault - File Documentation

Complete guide to every file in the project, what it does, and its responsibilities.

---

## Project Overview

```
TechVault/
├── README.md                    # Project setup and running instructions
├── COMPLETION_STATUS.md         # Project completion checklist
├── FILE_DOCUMENTATION.md        # This file - explains all files
│
├── backend/                     # Flask REST API Backend
│   ├── run.py                   # Entry point - starts Flask server
│   ├── requirements.txt         # Python dependencies list
│   ├── test_endpoints.py        # Comprehensive test suite
│   ├── test_api.sh              # Shell script for curl testing
│   ├── TEST_RESULTS.md          # Test execution report
│   ├── backend.log              # Server logs (auto-generated)
│   ├── backend.pid              # Process ID file (auto-generated)
│   │
│   └── app/                     # Main application package
│       ├── __init__.py          # Flask app factory
│       │
│       ├── data_access/         # DATABASE LAYER (Repositories)
│       │   ├── __init__.py      # Package marker
│       │   ├── db.py            # Database connection manager
│       │   ├── schema.sql       # SQL table definitions
│       │   ├── seed.py          # Sample data seeder
│       │   ├── user_repository.py       # User data access
│       │   ├── product_repository.py    # Product data access
│       │   ├── order_repository.py      # Order & cart data access
│       │   └── techvault.db     # SQLite database (auto-created)
│       │
│       ├── services/            # BUSINESS LOGIC LAYER (Services)
│       │   ├── __init__.py      # Package marker
│       │   ├── auth_service.py           # User authentication logic
│       │   ├── catalog_service.py        # Product browsing logic
│       │   ├── cart_service.py           # Shopping cart logic
│       │   ├── payment_strategy.py       # STRATEGY pattern - Payment methods
│       │   ├── order_state.py            # STATE pattern - Order lifecycle
│       │   ├── notification.py           # OBSERVER pattern - Notifications
│       │   ├── admin_service.py          # FACADE pattern - Admin interface
│       │   └── dashboard_factory.py      # FACTORY METHOD pattern - Dashboard creation
│       │
│       └── routes/              # API LAYER (REST Endpoints)
│           ├── __init__.py      # Package marker
│           ├── auth.py          # Authentication endpoints
│           ├── catalog.py       # Product catalog endpoints
│           ├── cart.py          # Shopping cart endpoints
│           └── order.py         # Order processing endpoints
│
└── frontend/                    # WEB UI Frontend
    ├── style.css                # Global CSS styling
    │
    ├── pages/                   # HTML Pages
    │   ├── index.html           # Product catalog/browse page
    │   ├── login.html           # User login page
    │   ├── register.html        # User registration page
    │   ├── cart.html            # Shopping cart & checkout page
    │   ├── orders.html          # Order tracking page
    │   └── admin.html           # Admin dashboard page
    │
    └── js/                      # JavaScript Files
        ├── api.js               # HTTP client for API calls
        ├── auth.js              # Authentication logic
        ├── catalog.js           # Product catalog logic
        ├── cart.js              # Cart operations logic
        ├── orders.js            # Order tracking logic
        └── admin.js             # Admin dashboard logic
```

---

## Backend - Data Access Layer

### `backend/app/data_access/db.py`
**Purpose:** Database connection and initialization manager

**Responsibilities:**
- Create and manage SQLite database connection
- Initialize database schema on first run
- Provide `get_db()` function for other modules
- Load schema.sql and create all tables

**Key Functions:**
- `get_db()` - Returns database connection with Row factory
- `init_db()` - Creates tables and seeds sample data

**Used by:** All repositories and services

---

### `backend/app/data_access/schema.sql`
**Purpose:** SQL schema definition for all database tables

**Contains 7 Tables:**
1. `users` - User accounts with authentication
2. `category` - Product categories
3. `product` - Product catalog
4. `product_variant` - Size/color variants for products
5. `cart_item` - Shopping cart items per user
6. `orders` - Customer orders with totals
7. `order_item` - Individual items in each order

**Responsibilities:**
- Define table structure
- Define relationships and foreign keys
- Create indexes for performance
- Ensure data integrity

---

### `backend/app/data_access/seed.py`
**Purpose:** Populate database with sample data on first run

**Responsibilities:**
- Create 3 sample product categories
- Add 4 sample products
- Handle duplicate insertion gracefully

**Sample Data Created:**
```
Categories: Electronics, Clothing, Books
Products: Laptop Pro, Wireless Mouse, T-Shirt, Python Book
```

**Used by:** `db.py` during initialization

---

### `backend/app/data_access/user_repository.py`
**Purpose:** User data access layer - handles all user database operations

**Responsibilities:**
- `create_user()` - Register new user
- `get_user_by_email()` - Find user by email
- `get_user_by_id()` - Find user by ID

**Database Operations:** INSERT, SELECT
**Used by:** `auth_service.py`

---

### `backend/app/data_access/product_repository.py`
**Purpose:** Product data access layer - handles product queries

**Responsibilities:**
- `get_all_products()` - Fetch all products with categories
- `get_product_by_id()` - Get single product details
- `get_products_by_category()` - Filter products by category
- `get_all_categories()` - Fetch all categories

**Database Operations:** SELECT with JOINs
**Used by:** `catalog_service.py`

---

### `backend/app/data_access/order_repository.py`
**Purpose:** Order and cart data access layer

**Responsibilities:**

**Order Operations:**
- `create_order()` - Create new order
- `add_order_item()` - Add items to order
- `get_order_by_id()` - Retrieve order details
- `get_user_orders()` - Get user's order history
- `update_order_status()` - Change order status

**Cart Operations:**
- `get_cart_items()` - View shopping cart
- `add_to_cart()` - Add/update cart items
- `remove_from_cart()` - Delete cart item
- `clear_cart()` - Empty entire cart

**Database Operations:** INSERT, SELECT, UPDATE, DELETE
**Used by:** `cart_service.py`, `order.py` route

---

## Backend - Business Logic Layer

### `backend/app/services/auth_service.py`
**Purpose:** User authentication business logic

**Responsibilities:**
- `register()` - New user registration
- `login()` - User authentication
- `get_user_profile()` - Retrieve user info

**Calls:** `UserRepository` for database access
**Used by:** `auth.py` routes

**Note:** Password hashing should be improved for production (currently plain text)

---

### `backend/app/services/catalog_service.py`
**Purpose:** Product browsing business logic

**Responsibilities:**
- `get_all_products()` - Return all products
- `get_product()` - Get single product details
- `get_products_by_category()` - Filter by category
- `get_categories()` - Fetch all categories

**Calls:** `ProductRepository`
**Used by:** `catalog.py` routes

---

### `backend/app/services/cart_service.py`
**Purpose:** Shopping cart business logic

**Responsibilities:**
- `add_to_cart()` - Add item with quantity check
- `remove_from_cart()` - Delete item from cart
- `get_cart()` - Calculate cart total
- `clear_cart()` - Empty cart

**Validation:**
- Check product exists
- Verify stock availability
- Calculate totals

**Calls:** `OrderRepository`, `ProductRepository`
**Used by:** `cart.py` routes

---

### `backend/app/services/payment_strategy.py`
**Purpose:** STRATEGY DESIGN PATTERN - Flexible payment processing

**Pattern Implementation:**
```
PaymentStrategy (Abstract)
├── CreditCardPayment (Concrete)
└── CashOnDeliveryPayment (Concrete)

PaymentProcessor (Context) - Uses strategy at runtime
```

**Responsibilities:**
- `PaymentStrategy` - Define payment interface
- `CreditCardPayment` - Process card payments
- `CashOnDeliveryPayment` - Handle COD orders
- `PaymentProcessor` - Context that uses strategy

**Key Benefit:** Payment methods can be swapped at runtime without changing checkout logic

**Used by:** `order.py` during checkout

---

### `backend/app/services/order_state.py`
**Purpose:** STATE DESIGN PATTERN - Order lifecycle management

**Pattern Implementation:**
```
OrderState (Abstract)
├── PendingState
├── PaidState
├── ShippedState
└── ReceivedState

Order (Context) - Manages state transitions
```

**State Flow:**
```
Pending → Paid → Shipped → Received
```

**Responsibilities:**
- `OrderState` - Define state interface
- Concrete states - Implement state behavior
- `Order` - Manage transitions

**Key Benefit:** Clear, type-safe order lifecycle management

**Used by:** Order processing and status updates

---

### `backend/app/services/notification.py`
**Purpose:** OBSERVER DESIGN PATTERN - Event-based notifications

**Pattern Implementation:**
```
Observer (Abstract)
├── EmailNotifier (Concrete)
└── SMSNotifier (Concrete)

OrderNotificationManager (Subject)
```

**Responsibilities:**
- `Observer` - Define observer interface
- `EmailNotifier` - Send email notifications
- `SMSNotifier` - Send SMS notifications
- `OrderNotificationManager` - Manage observers and notify all

**Notification Triggers:**
- Order status changes
- Payment processed
- Shipment updates

**Key Benefit:** Add/remove notification methods without changing order logic

**Used by:** `order.py` route when status updates

---

### `backend/app/services/admin_service.py`
**Purpose:** FACADE DESIGN PATTERN - Simplified admin interface

**Pattern Implementation:**
```
AdminService (Facade)
├── Wraps OrderRepository
├── Wraps ProductRepository
└── Performs calculations
```

**Simplified Methods:**
- `get_dashboard_stats()` - Overall statistics
- `get_pending_orders()` - Order management
- `update_order_status()` - Status updates
- `get_inventory_report()` - Stock analysis

**Key Benefit:** Complex multi-repository operations simplified into single calls

**Hides Complexity:** Multiple repositories, joins, calculations

**Used by:** Admin dashboard and admin routes

---

### `backend/app/services/dashboard_factory.py`
**Purpose:** FACTORY METHOD DESIGN PATTERN - Create role-based dashboards

**Pattern Implementation:**
```
Dashboard (Abstract)
├── CustomerDashboard (Concrete)
└── AdminDashboard (Concrete)

DashboardFactory (Factory)
```

**Responsibilities:**
- `Dashboard` - Define dashboard interface
- `CustomerDashboard` - Customer-specific data/actions
- `AdminDashboard` - Admin-specific data/actions
- `DashboardFactory` - Create appropriate dashboard by role

**Key Benefit:** New dashboard types can be added without modifying existing code

**Used by:** Frontend to get role-specific data

---

## Backend - API Routes Layer

### `backend/app/routes/auth.py`
**Purpose:** Authentication API endpoints

**Endpoints:**
```
POST   /api/auth/register           - Register new user
POST   /api/auth/login              - Authenticate user
GET    /api/auth/profile/<user_id>  - Get user info
```

**Responsibilities:**
- Parse JSON requests
- Validate input
- Call `AuthService`
- Return JSON responses with proper HTTP status codes

**Status Codes:**
- 201 (Created) - Successful registration
- 200 (OK) - Successful login/profile
- 401 (Unauthorized) - Invalid credentials
- 400 (Bad Request) - Invalid input

**Uses:** `AuthService`

---

### `backend/app/routes/catalog.py`
**Purpose:** Product browsing API endpoints

**Endpoints:**
```
GET    /api/catalog/products                  - All products
GET    /api/catalog/products/<id>             - Product details
GET    /api/catalog/categories                - All categories
GET    /api/catalog/categories/<id>/products  - Products by category
```

**Responsibilities:**
- Return product/category data
- Handle filtering by category
- Return proper JSON structure

**Status Codes:**
- 200 (OK) - Successful retrieval
- 404 (Not Found) - Product/category not found

**Uses:** `CatalogService`

---

### `backend/app/routes/cart.py`
**Purpose:** Shopping cart API endpoints

**Endpoints:**
```
POST   /api/cart/add           - Add item to cart
POST   /api/cart/remove        - Remove item
GET    /api/cart/<user_id>     - View cart
POST   /api/cart/clear/<user_id> - Clear cart
```

**Responsibilities:**
- Handle cart operations
- Calculate totals
- Return cart state
- Convert SQLite Row objects to JSON

**Status Codes:**
- 200 (OK) - Successful operation
- 201 (Created) - Item added
- 400 (Bad Request) - Invalid input

**Uses:** `CartService`

---

### `backend/app/routes/order.py`
**Purpose:** Order processing API endpoints (demonstrates multiple patterns)

**Endpoints:**
```
POST   /api/order/checkout                    - Create order (STRATEGY pattern)
GET    /api/order/<order_id>                  - Order details
GET    /api/order/user/<user_id>              - User's orders
PUT    /api/order/<order_id>/status/<status>  - Update status (OBSERVER pattern)
```

**Responsibilities:**

**Checkout (uses STRATEGY pattern):**
- Get user's cart
- Select payment strategy (Card/COD)
- Create order
- Add order items
- Process payment
- Update order status
- Clear cart
- Notify observers

**Status Updates (uses OBSERVER pattern):**
- Update order status
- Trigger notifications
- Update database

**Uses:** `CartService`, `OrderRepository`, `PaymentProcessor`, `OrderNotificationManager`

---

### `backend/app/__init__.py`
**Purpose:** Flask application factory

**Responsibilities:**
- Create Flask app instance
- Enable CORS (Cross-Origin Resource Sharing)
- Register all blueprints (routes)
- Define error handlers

**Blueprints Registered:**
- `auth_bp` from `auth.py`
- `catalog_bp` from `catalog.py`
- `cart_bp` from `cart.py`
- `order_bp` from `order.py`

**Error Handlers:**
- 404 Not Found
- 500 Internal Server Error

**Used by:** `run.py`

---

## Backend - Configuration & Testing

### `backend/run.py`
**Purpose:** Application entry point

**Responsibilities:**
- Import `create_app` from app package
- Initialize database if it doesn't exist
- Create Flask application
- Start development server on port 5000

**Key Steps:**
1. Check if database exists
2. If not, run `init_db()` to create and seed
3. Create app with `create_app()`
4. Print startup message
5. Run server with debug mode enabled

**Command to run:** `python3 run.py`

---

### `backend/requirements.txt`
**Purpose:** Python dependencies specification

**Contains:**
- `Flask==2.3.0` - Web framework
- `Flask-CORS==4.0.0` - Cross-origin support
- `Werkzeug==2.3.0` - WSGI utilities
- `python-dotenv==1.0.0` - Environment variables

**Usage:** `pip3 install -r requirements.txt`

---

### `backend/test_endpoints.py`
**Purpose:** Comprehensive Python test suite

**Responsibilities:**
- Test all 15 API endpoints
- Verify correct HTTP status codes
- Validate response data
- Demonstrate design patterns in use
- Provide colored output for readability

**Tests Included:**
1. Authentication (register, login, profile)
2. Catalog (products, categories, filtering)
3. Shopping Cart (add, view, remove, clear)
4. Orders (checkout, list, details, status)

**Design Pattern Tests:**
- STRATEGY pattern in checkout
- STATE pattern in order status
- OBSERVER pattern notifications
- FACADE pattern admin service
- FACTORY METHOD pattern dashboard

**Command:** `python3 test_endpoints.py`

---

### `backend/test_api.sh`
**Purpose:** Bash script for testing with curl commands

**Responsibilities:**
- Provide shell-based testing alternative
- Show curl command examples
- Test endpoints without Python

**Usage:** `bash test_api.sh`

**Platforms:** macOS and Linux (Windows requires Git Bash)

---

### `backend/TEST_RESULTS.md`
**Purpose:** Test execution report and documentation

**Contains:**
- Summary of all tests
- Endpoint breakdown
- Sample responses
- Design pattern demonstrations
- Test metrics and timing
- Instructions to run tests

---

## Frontend - Pages

### `frontend/pages/index.html`
**Purpose:** Main product catalog/browse page

**Responsibilities:**
- Display navigation bar
- Show product grid
- Display category filters
- Handle product browsing

**Components:**
- Hero section with tagline
- Category filter buttons
- Product grid with "Add to Cart" buttons

**JavaScript:** Uses `catalog.js`
**API Calls:** GET `/api/catalog/products`, GET `/api/catalog/categories`

---

### `frontend/pages/login.html`
**Purpose:** User login page

**Responsibilities:**
- Display login form
- Validate email/password
- Send credentials to API
- Store user session (localStorage)

**Form Fields:**
- Email address
- Password

**JavaScript:** Uses `auth.js`
**API Calls:** POST `/api/auth/login`
**On Success:** Redirect to index.html

---

### `frontend/pages/register.html`
**Purpose:** User registration page

**Responsibilities:**
- Display registration form
- Create new user account
- Send to login page after registration

**Form Fields:**
- Username
- Email address
- Password

**JavaScript:** Uses `auth.js`
**API Calls:** POST `/api/auth/register`
**On Success:** Redirect to login.html

---

### `frontend/pages/cart.html`
**Purpose:** Shopping cart and checkout page (demonstrates STRATEGY pattern)

**Responsibilities:**
- Display items in cart
- Show individual prices and subtotals
- Calculate total amount
- Allow quantity removal
- Handle checkout process
- Implement payment method selection

**Features:**
- Item list with remove buttons
- Running total calculation
- Payment method selection (STRATEGY pattern):
  - Credit Card
  - Cash on Delivery
- Checkout button

**JavaScript:** Uses `cart.js`
**API Calls:** 
- GET `/api/cart/<user_id>`
- POST `/api/cart/remove`
- POST `/api/order/checkout`

**Pattern Demonstration:** Shows payment strategy selection

---

### `frontend/pages/orders.html`
**Purpose:** Order tracking page (demonstrates STATE & OBSERVER patterns)

**Responsibilities:**
- Display user's orders
- Show order status with visual state progression
- Allow status updates
- Display notifications

**Features:**
- Order list with details
- Visual state progression (Pending → Paid → Shipped → Received)
- Status dropdown to update
- Shows created/updated timestamps

**JavaScript:** Uses `orders.js`
**API Calls:**
- GET `/api/order/user/<user_id>`
- PUT `/api/order/<order_id>/status/<status>`

**Pattern Demonstration:** 
- STATE pattern: Visual progression through states
- OBSERVER pattern: Status changes trigger notifications

---

### `frontend/pages/admin.html`
**Purpose:** Admin dashboard (demonstrates FACADE & FACTORY patterns)

**Responsibilities:**
- Display overall statistics
- Show pending orders
- Display inventory report
- Allow order status management

**Sections:**
- Dashboard stats (total orders, pending, products, inventory value)
- Pending orders list
- Inventory report with low-stock warnings
- Product table with stock levels

**JavaScript:** Uses `admin.js`
**API Calls:**
- GET `/api/order/user/1`
- GET `/api/catalog/products`
- PUT `/api/order/<order_id>/status/<status>`

**Pattern Demonstration:**
- FACADE pattern: Simplified dashboard interface hiding complexity
- FACTORY METHOD pattern: Dashboard created based on user role

---

## Frontend - JavaScript Files

### `frontend/js/api.js`
**Purpose:** HTTP client for API communication

**Responsibilities:**
- Provide reusable API methods
- Handle base URL configuration
- Manage headers
- Parse JSON responses

**Methods:**
- `APIClient.get(endpoint)` - GET request
- `APIClient.post(endpoint, data)` - POST request
- `APIClient.put(endpoint, data)` - PUT request

**Used by:** All other JavaScript files for API calls
**Base URL:** `http://localhost:5000/api`

---

### `frontend/js/auth.js`
**Purpose:** Authentication logic and form handling

**Responsibilities:**
- Handle login form submission
- Handle registration form submission
- Store user ID in localStorage
- Validate credentials
- Redirect on success/failure

**Functions:**
- Login form listener → POST to `/api/auth/login`
- Register form listener → POST to `/api/auth/register`

**Storage:** localStorage for `userId` and `userRole`

**Used in:** login.html, register.html

---

### `frontend/js/catalog.js`
**Purpose:** Product catalog browsing logic

**Responsibilities:**
- Load products on page load
- Load categories
- Display product grid
- Handle category filtering
- Add to cart functionality

**Functions:**
- `loadAllProducts()` - Fetch and display all
- `loadProductsByCategory()` - Filter by category
- `displayProducts()` - Render product grid
- `addToCart()` - Add item with quantity

**API Calls:**
- GET `/api/catalog/categories`
- GET `/api/catalog/products`
- POST `/api/cart/add`

**Used in:** index.html

---

### `frontend/js/cart.js`
**Purpose:** Shopping cart operations (demonstrates STRATEGY pattern)

**Responsibilities:**
- Load and display cart items
- Calculate totals
- Handle item removal
- Process checkout with payment strategy selection

**Functions:**
- `loadCart()` - Fetch cart data
- `removeItem()` - Delete item from cart
- `checkout()` - Create order with payment method

**Payment Strategies Demonstrated:**
- Credit Card Payment
- Cash on Delivery

**API Calls:**
- GET `/api/cart/<user_id>`
- POST `/api/cart/remove`
- POST `/api/order/checkout`

**Used in:** cart.html

**Pattern Display:** Console logs show STRATEGY pattern usage

---

### `frontend/js/orders.js`
**Purpose:** Order tracking and status management (demonstrates STATE & OBSERVER patterns)

**Responsibilities:**
- Load user's orders
- Display order status progression
- Handle status updates
- Show notifications triggered by OBSERVER pattern

**Functions:**
- `loadOrders()` - Fetch user's orders
- `getStateDisplay()` - Visualize state progression
- `updateStatus()` - Change order status

**State Visualization:**
```
⏳ Pending → ✓ Paid → 🚚 Shipped → 📦 Received
```

**API Calls:**
- GET `/api/order/user/<user_id>`
- PUT `/api/order/<order_id>/status/<status>`

**Pattern Display:**
- STATE pattern: Visual state progression
- OBSERVER pattern: Notifications on status change

**Used in:** orders.html

---

### `frontend/js/admin.js`
**Purpose:** Admin dashboard (demonstrates FACADE & FACTORY patterns)

**Responsibilities:**
- Load dashboard statistics
- Display pending orders
- Show inventory report
- Handle order status updates
- Check user role (FACTORY pattern)

**Functions:**
- `loadDashboard()` - Fetch all data
- `displayPendingOrders()` - Show orders needing attention
- `displayInventoryReport()` - Show stock status
- `updateOrderStatus()` - Change order status

**Dashboard Stats:**
- Total orders
- Pending orders
- Total products
- Inventory value

**Inventory Features:**
- Low stock warnings (< 5 units)
- Product table with prices and stock
- Stock value calculations

**API Calls:**
- GET `/api/order/user/<user_id>`
- GET `/api/catalog/products`
- PUT `/api/order/<order_id>/status/<status>`

**Pattern Display:**
- FACADE pattern: Simplified complex operations
- FACTORY METHOD pattern: Dashboard based on role

**Used in:** admin.html

---

## Frontend - Styling

### `frontend/style.css`
**Purpose:** Global CSS styling for entire application

**Responsibilities:**
- Define color scheme and theme
- Style all HTML elements
- Create responsive layout
- Style forms, buttons, cards, grids
- Handle hover and active states

**Key Styles:**
- Navigation bar
- Hero section
- Product cards with hover effects
- Forms and inputs
- Buttons with colors
- Grid layout for products
- Cart items layout
- Order status visualization
- Admin dashboard layout

**Color Scheme:**
- Primary: #3498db (blue)
- Success: #27ae60 (green)
- Warning: #f39c12 (orange)
- Danger: #e74c3c (red)
- Background: #f5f5f5 (light gray)

**Features:**
- Responsive design
- Flexbox and Grid layouts
- Smooth transitions
- Professional appearance

---

## Configuration & Documentation Files

### `README.md`
**Purpose:** Project setup and usage guide

**Contains:**
- Quick summary
- Installation instructions (Windows, macOS, Linux)
- Backend setup steps
- Frontend setup options
- API endpoint documentation
- Testing instructions
- Troubleshooting guide
- Design patterns overview
- File locations

**Audience:** Developers setting up the project

---

### `COMPLETION_STATUS.md`
**Purpose:** Project completion checklist and summary

**Contains:**
- Completion status for all components
- File count and metrics
- Architecture diagram
- Design pattern details
- Database schema explanation
- Assignment requirements met
- What's still needed (presentation, docs)

**Audience:** Project stakeholders and instructors

---

### `FILE_DOCUMENTATION.md`
**Purpose:** This file - comprehensive file documentation

**Contains:**
- Every file's purpose and responsibility
- How files interact
- Dependencies between files
- Pattern implementations

**Audience:** Developers understanding the codebase

---

## Database Files

### `backend/app/data_access/techvault.db`
**Purpose:** SQLite database file (auto-created)

**Responsibilities:**
- Store all application data
- Maintain 7 tables with relationships
- Persist user accounts, products, orders, etc.

**Created by:** `db.py` on first run
**Deleted by:** Deleting the file resets database

**Not in git:** Database file is local to each installation

---

## Log & Cache Files (Auto-Generated)

### `backend/backend.log`
**Purpose:** Server startup logs (created when running)

**Contains:**
- Server startup messages
- Request logs (if logging enabled)
- Error messages

---

### `backend/backend.pid`
**Purpose:** Process ID file (created when running)

**Contains:**
- PID of running Flask process
- Used to stop server gracefully

---

## File Interaction Map

```
run.py
  └─→ app/__init__.py (create_app)
       ├─→ routes/auth.py ──→ services/auth_service.py
       ├─→ routes/catalog.py ──→ services/catalog_service.py
       ├─→ routes/cart.py ──→ services/cart_service.py
       └─→ routes/order.py ──→ services/{payment_strategy, order_state, notification}
                                 ├─→ services/admin_service.py
                                 └─→ data_access/{repositories}
                                       └─→ data_access/db.py ──→ techvault.db

Frontend JS Files:
  ├─→ All use: js/api.js ──→ Backend API routes
  ├─→ auth.js: Used by login.html, register.html
  ├─→ catalog.js: Used by index.html
  ├─→ cart.js: Used by cart.html (STRATEGY pattern)
  ├─→ orders.js: Used by orders.html (STATE + OBSERVER patterns)
  └─→ admin.js: Used by admin.html (FACADE + FACTORY patterns)

CSS:
  └─→ style.css: Used by all HTML pages
```

---

## Summary by Purpose

### Data Layer Files
- `db.py` - Connection management
- `schema.sql` - Table definitions
- `seed.py` - Sample data
- `*_repository.py` (3 files) - Data access

### Business Logic Files
- `auth_service.py` - Authentication
- `catalog_service.py` - Product queries
- `cart_service.py` - Cart calculations
- `payment_strategy.py` - STRATEGY pattern
- `order_state.py` - STATE pattern
- `notification.py` - OBSERVER pattern
- `admin_service.py` - FACADE pattern
- `dashboard_factory.py` - FACTORY METHOD pattern

### API Route Files
- `auth.py` - Authentication endpoints
- `catalog.py` - Product endpoints
- `cart.py` - Cart endpoints
- `order.py` - Order endpoints

### Frontend UI Files
- 6 HTML pages - User interfaces
- 6 JavaScript files - Logic and API calls
- 1 CSS file - Styling

### Configuration & Documentation
- `run.py` - Entry point
- `requirements.txt` - Dependencies
- `README.md` - Setup guide
- `COMPLETION_STATUS.md` - Project status
- `FILE_DOCUMENTATION.md` - This file

---

**Total Files:** 40+  
**Total Lines of Code:** 5000+  
**Design Patterns:** 5  
**API Endpoints:** 15  
**Database Tables:** 7

---

Last updated: June 16, 2026
