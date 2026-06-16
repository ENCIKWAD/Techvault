import sqlite3
from .db import get_db

class OrderRepository:
    @staticmethod
    def create_order(user_id, total_amount, payment_method):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO orders (user_id, total_amount, payment_method, status) VALUES (?, ?, ?, ?)',
            (user_id, total_amount, payment_method, 'pending')
        )
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return order_id

    @staticmethod
    def add_order_item(order_id, product_id, quantity, unit_price):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO order_item (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
            (order_id, product_id, quantity, unit_price)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_order_by_id(order_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = cursor.fetchone()
        conn.close()
        return order

    @staticmethod
    def get_user_orders(user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        orders = cursor.fetchall()
        conn.close()
        return orders

    @staticmethod
    def update_order_status(order_id, status):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (status, order_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_cart_items(user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT c.*, p.name, p.price FROM cart_item c JOIN product p ON c.product_id = p.id WHERE c.user_id = ?',
            (user_id,)
        )
        items = cursor.fetchall()
        conn.close()
        return items

    @staticmethod
    def add_to_cart(user_id, product_id, quantity=1):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT OR REPLACE INTO cart_item (user_id, product_id, quantity) VALUES (?, ?, COALESCE((SELECT quantity FROM cart_item WHERE user_id = ? AND product_id = ?), 0) + ?)',
            (user_id, product_id, user_id, product_id, quantity)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def remove_from_cart(user_id, product_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM cart_item WHERE user_id = ? AND product_id = ?',
            (user_id, product_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def clear_cart(user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cart_item WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
