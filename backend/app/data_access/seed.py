from .db import get_db

def seed_data():
    conn = get_db()
    cursor = conn.cursor()

    try:
        # Add sample categories
        categories = [
            ('Electronics', 'Electronic devices and gadgets'),
            ('Clothing', 'Apparel and accessories'),
            ('Books', 'Educational and recreational books'),
        ]
        cursor.executemany('INSERT INTO category (name, description) VALUES (?, ?)', categories)

        # Add sample products (prices in RM)
        products = [
            ('Laptop Pro', 'High-performance laptop', 4499.99, 1, 10),
            ('Wireless Mouse', 'Ergonomic mouse', 129.99, 1, 50),
            ('T-Shirt', 'Cotton t-shirt', 89.99, 2, 100),
            ('Python Book', 'Learn Python Programming', 169.99, 3, 25),
        ]
        cursor.executemany(
            'INSERT INTO product (name, description, price, category_id, stock) VALUES (?, ?, ?, ?, ?)',
            products
        )

        conn.commit()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Seeding error (may already be seeded): {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    seed_data()
