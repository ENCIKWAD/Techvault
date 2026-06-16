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
