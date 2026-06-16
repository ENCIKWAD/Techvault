from flask import Blueprint, request, jsonify
from ..services.cart_service import CartService

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.json
    success = CartService.add_to_cart(data['user_id'], data['product_id'], data.get('quantity', 1))
    return jsonify({'success': success}), 201 if success else 400

@cart_bp.route('/remove', methods=['POST'])
def remove_from_cart():
    data = request.json
    CartService.remove_from_cart(data['user_id'], data['product_id'])
    return jsonify({'success': True})

@cart_bp.route('/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart = CartService.get_cart(user_id)
    items = [dict(item) for item in cart['items']]
    return jsonify({'items': items, 'total': cart['total']})

@cart_bp.route('/clear/<int:user_id>', methods=['POST'])
def clear_cart(user_id):
    CartService.clear_cart(user_id)
    return jsonify({'success': True})
