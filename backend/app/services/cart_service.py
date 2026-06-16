from ..data_access.order_repository import OrderRepository
from ..data_access.product_repository import ProductRepository

class CartService:
    @staticmethod
    def add_to_cart(user_id, product_id, quantity=1):
        product = ProductRepository.get_product_by_id(product_id)
        if not product or product['stock'] < quantity:
            return False
        OrderRepository.add_to_cart(user_id, product_id, quantity)
        return True

    @staticmethod
    def remove_from_cart(user_id, product_id):
        OrderRepository.remove_from_cart(user_id, product_id)

    @staticmethod
    def get_cart(user_id):
        items = OrderRepository.get_cart_items(user_id)
        total = sum(item['price'] * item['quantity'] for item in items)
        return {'items': items, 'total': total}

    @staticmethod
    def clear_cart(user_id):
        OrderRepository.clear_cart(user_id)
