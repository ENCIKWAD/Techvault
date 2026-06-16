"""
🎯 FACADE PATTERN IMPLEMENTATION
=================================
This file demonstrates the FACADE design pattern for admin operations.

Pattern: Structural Design Pattern
Purpose: Provide a simplified, unified interface to complex subsystem components.
         Admin operations are simplified by hiding repository complexity.

Key Classes:
- AdminService: Facade that provides simplified admin interface

Complex Subsystem (Hidden behind facade):
- OrderRepository: Complex order database operations
- ProductRepository: Complex product database operations
- Multiple queries, calculations, data processing

Facade Methods:
- get_dashboard_stats(): Returns stats (hides multiple DB queries)
- update_order_status(): Updates order status (hides database update)
- get_inventory_report(): Returns inventory data (hides complex filtering)

Related Files:
- backend/app/data_access/order_repository.py: Provides order data
- backend/app/data_access/product_repository.py: Provides product data
- frontend/js/admin.js: Uses simplified admin interface

Usage Flow:
1. Admin frontend calls AdminService methods
2. AdminService internally uses repositories
3. Complex operations are hidden from frontend
4. Frontend receives simple, clean data
5. If repositories change, facade updates but frontend unchanged

Benefits:
- Simplified interface for complex operations
- Decoupling between frontend and repositories
- Easy to modify subsystem without affecting clients
- Reduced client complexity
"""

from ..data_access.order_repository import OrderRepository
from ..data_access.product_repository import ProductRepository

class AdminService:
    @staticmethod
    def get_dashboard_stats():
        all_orders = OrderRepository.get_user_orders(1)
        all_products = ProductRepository.get_all_products()

        return {
            'total_orders': len(all_orders) if all_orders else 0,
            'total_products': len(all_products) if all_products else 0,
            'pending_orders': sum(1 for o in (all_orders or []) if o['status'] == 'pending'),
            'inventory_value': sum(p['price'] * p['stock'] for p in (all_products or []))
        }

    @staticmethod
    def get_pending_orders():
        return []

    @staticmethod
    def update_order_status(order_id, status):
        OrderRepository.update_order_status(order_id, status)

    @staticmethod
    def get_inventory_report():
        products = ProductRepository.get_all_products()
        low_stock = [p for p in products if p['stock'] < 5]
        return {
            'total_products': len(products),
            'low_stock_items': len(low_stock),
            'low_stock_list': low_stock
        }
