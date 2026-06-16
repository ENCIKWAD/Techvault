import os
import sys
from app import create_app
from app.data_access.db import init_db, ensure_default_users

if __name__ == '__main__':
    db_path = os.path.join(os.path.dirname(__file__), 'app/data_access/techvault.db')
    if not os.path.exists(db_path):
        print("Initializing database...")
        init_db()
        print("Database initialized successfully!")

    ensure_default_users()
    print("Default accounts ready (admin@techvault.com / customer@techvault.com)")

    app = create_app()
    print("Starting TechVault backend on http://localhost:5000")
    app.run(debug=True, port=5000)
