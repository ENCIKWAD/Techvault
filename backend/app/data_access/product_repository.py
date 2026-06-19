from .db import get_db

class ProductRepository:
    @staticmethod
    def get_all_products():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT p.*, c.name as category_name FROM product p LEFT JOIN category c ON p.category_id = c.id'
        )
        products = cursor.fetchall()
        conn.close()
        return products

    @staticmethod
    def get_product_by_id(product_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT p.*, c.name as category_name FROM product p LEFT JOIN category c ON p.category_id = c.id WHERE p.id = ?',
            (product_id,)
        )
        product = cursor.fetchone()
        conn.close()
        return product

    @staticmethod
    def get_products_by_category(category_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM product WHERE category_id = ?',
            (category_id,)
        )
        products = cursor.fetchall()
        conn.close()
        return products

    @staticmethod
    def get_all_categories():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM category')
        categories = cursor.fetchall()
        conn.close()
        return categories

    @staticmethod
    def update_product(product_id, data):
        conn = get_db()
        cursor = conn.cursor()
        try:
            if 'name' in data:
                cursor.execute('UPDATE product SET name = ? WHERE id = ?', (data['name'], product_id))
            if 'description' in data:
                cursor.execute('UPDATE product SET description = ? WHERE id = ?', (data['description'], product_id))
            if 'price' in data:
                cursor.execute('UPDATE product SET price = ? WHERE id = ?', (data['price'], product_id))
            if 'stock' in data:
                cursor.execute('UPDATE product SET stock = ? WHERE id = ?', (data['stock'], product_id))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    @staticmethod
    def create_product(name, description, price, category_id, stock):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO product (name, description, price, category_id, stock) VALUES (?, ?, ?, ?, ?)',
                (name, description, price, category_id, stock)
            )
            conn.commit()
            product_id = cursor.lastrowid
            conn.close()
            return product_id
        except:
            conn.close()
            return None

    @staticmethod
    def delete_product(product_id):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM product WHERE id = ?', (product_id,))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()
