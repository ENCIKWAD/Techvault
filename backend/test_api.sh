#!/bin/bash

# TechVault API Test Script
# Tests all 15 endpoints with real scenarios

API_BASE="http://localhost:5000/api"
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   TechVault API Test Suite${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Helper function to print test results
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4

    echo -e "${YELLOW}Testing: $description${NC}"
    echo -e "  ${BLUE}$method $endpoint${NC}"

    if [ -z "$data" ]; then
        response=$(curl -s -X "$method" "$API_BASE$endpoint" \
            -H "Content-Type: application/json")
    else
        echo -e "  ${BLUE}Data: $data${NC}"
        response=$(curl -s -X "$method" "$API_BASE$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi

    echo -e "  ${GREEN}Response:${NC}"
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "  $response"
    echo ""
}

# ============== AUTHENTICATION ==============
echo -e "${BLUE}========== AUTH ENDPOINTS ==========${NC}\n"

# Register a new user
test_endpoint "POST" "/auth/register" \
    '{"username":"testuser","email":"test@example.com","password":"password123"}' \
    "1. Register User"

# Login user
test_endpoint "POST" "/auth/login" \
    '{"email":"test@example.com","password":"password123"}' \
    "2. Login User"

# Get user profile
test_endpoint "GET" "/auth/profile/1" \
    "" \
    "3. Get User Profile (ID: 1)"

# ============== CATALOG ==============
echo -e "${BLUE}========== CATALOG ENDPOINTS ==========${NC}\n"

# Get all categories
test_endpoint "GET" "/catalog/categories" \
    "" \
    "4. Get All Categories"

# Get all products
test_endpoint "GET" "/catalog/products" \
    "" \
    "5. Get All Products"

# Get specific product
test_endpoint "GET" "/catalog/products/1" \
    "" \
    "6. Get Product Details (Product ID: 1)"

# Get products by category
test_endpoint "GET" "/catalog/categories/1/products" \
    "" \
    "7. Get Products by Category (Category ID: 1 - Electronics)"

# ============== SHOPPING CART ==============
echo -e "${BLUE}========== CART ENDPOINTS ==========${NC}\n"

# Add item to cart
test_endpoint "POST" "/cart/add" \
    '{"user_id":1,"product_id":1,"quantity":2}' \
    "8. Add Product to Cart (Product ID: 1, Qty: 2)"

# Add another item
test_endpoint "POST" "/cart/add" \
    '{"user_id":1,"product_id":2,"quantity":1}' \
    "9. Add Product to Cart (Product ID: 2, Qty: 1)"

# View cart
test_endpoint "GET" "/cart/1" \
    "" \
    "10. View Cart (User ID: 1)"

# ============== ORDERS (CHECKOUT) ==============
echo -e "${BLUE}========== ORDER ENDPOINTS ==========${NC}\n"

# Checkout with STRATEGY pattern - Credit Card
test_endpoint "POST" "/order/checkout" \
    '{"user_id":1,"payment_method":"card"}' \
    "11. Checkout with Credit Card (STRATEGY Pattern)"

# Get user orders
test_endpoint "GET" "/order/user/1" \
    "" \
    "12. Get User Orders (User ID: 1)"

# Get specific order
test_endpoint "GET" "/order/1" \
    "" \
    "13. Get Order Details (Order ID: 1)"

# ============== ORDER STATUS UPDATE ==============
echo -e "${BLUE}========== ORDER STATUS UPDATE (OBSERVER & STATE PATTERNS) ==========${NC}\n"

# Update order status - will trigger OBSERVER notifications
test_endpoint "PUT" "/order/1/status/paid" \
    "" \
    "14. Update Order Status to PAID (Triggers OBSERVER notifications)"

# Update order status again
test_endpoint "PUT" "/order/1/status/shipped" \
    "" \
    "15. Update Order Status to SHIPPED (Triggers OBSERVER notifications)"

# ============== CART CLEANUP ==============
echo -e "${BLUE}========== CLEANUP ==========${NC}\n"

# Remove item from cart
test_endpoint "POST" "/cart/remove" \
    '{"user_id":1,"product_id":1}' \
    "16. Remove Product from Cart"

# Clear cart
test_endpoint "POST" "/cart/clear/1" \
    "" \
    "17. Clear Cart"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   All Tests Completed!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${YELLOW}Design Patterns Demonstrated:${NC}"
echo -e "  ⭐ ${BLUE}STRATEGY Pattern${NC}    - Payment methods (Credit Card, COD)"
echo -e "  ⭐ ${BLUE}STATE Pattern${NC}       - Order lifecycle (Pending → Paid → Shipped → Received)"
echo -e "  ⭐ ${BLUE}OBSERVER Pattern${NC}    - Status change notifications"
echo -e "  ⭐ ${BLUE}FACADE Pattern${NC}      - Admin service simplification"
echo -e "  ⭐ ${BLUE}FACTORY Pattern${NC}     - Dashboard creation\n"
