from flask import Blueprint, request, jsonify
from ..services.cart_service import CartService
from ..data_access.order_repository import OrderRepository
from ..services.payment_strategy import PaymentProcessor, CreditCardPayment, CashOnDeliveryPayment
from ..services.notification import OrderNotificationManager, EmailNotifier, SMSNotifier

order_bp = Blueprint('order', __name__, url_prefix='/api/order')

# Initialize notification system
notification_manager = OrderNotificationManager()
notification_manager.attach(EmailNotifier())
notification_manager.attach(SMSNotifier())

@order_bp.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    user_id = data['user_id']
    payment_method = data['payment_method']

    print(f"\n🛒 [CHECKOUT] User {user_id} initiating checkout with method: {payment_method}")

    cart = CartService.get_cart(user_id)
    total = cart['total']
    print(f"🛒 [CHECKOUT] Cart total: RM{total}")

    order_id = OrderRepository.create_order(user_id, total, payment_method)
    print(f"🛒 [CHECKOUT] Order created with ID: {order_id}")

    for item in cart['items']:
        OrderRepository.add_order_item(order_id, item['product_id'], item['quantity'], item['price'])
    print(f"🛒 [CHECKOUT] Order items added: {len(cart['items'])} items")

    # STRATEGY Pattern
    print(f"\n📋 [STRATEGY PATTERN] Initializing payment strategy...")
    if payment_method == 'card':
        strategy = CreditCardPayment()
        print(f"📋 [STRATEGY] Using: CreditCardPayment strategy")
    else:
        strategy = CashOnDeliveryPayment()
        print(f"📋 [STRATEGY] Using: CashOnDeliveryPayment strategy")

    processor = PaymentProcessor(strategy)
    payment_result = processor.pay(total, user_id)
    print(f"📋 [STRATEGY] Payment result: {payment_result}\n")

    final_status = 'paid' if payment_result['success'] else 'pending'
    OrderRepository.update_order_status(order_id, final_status)
    print(f"📊 [STATE] Order #{order_id} status set to: {final_status}")

    CartService.clear_cart(user_id)

    # OBSERVER Pattern
    print(f"📢 [OBSERVER] Notifying observers of status change...")
    notification_manager.notify_status_change(order_id, final_status)
    print(f"📢 [OBSERVER] Notification complete\n")

    return jsonify({'order_id': order_id, 'status': 'success'}), 201

@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = OrderRepository.get_order_by_id(order_id)
    if order:
        return jsonify(dict(order))
    return jsonify({'error': 'Order not found'}), 404

@order_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    orders = OrderRepository.get_user_orders(user_id)
    return jsonify([dict(o) for o in orders])

@order_bp.route('/<int:order_id>/status/<status>', methods=['PUT'])
def update_order_status(order_id, status):
    old_order = OrderRepository.get_order_by_id(order_id)
    old_status = old_order['status'] if old_order else 'unknown'

    print(f"\n📊 [STATE PATTERN] Order transition detected")
    print(f"📊 [STATE] Order ID: {order_id}")
    print(f"📊 [STATE] Old status: {old_status} → New status: {status}")

    OrderRepository.update_order_status(order_id, status)

    print(f"📊 [STATE] Database updated successfully")
    print(f"📢 [OBSERVER] Triggering notifications...")

    notification_manager.notify_status_change(order_id, status)

    print(f"📢 [OBSERVER] Notifications sent")
    print(f"✅ [STATE] Order #{order_id} transition complete: {old_status} → {status}\n")

    return jsonify({'success': True})
