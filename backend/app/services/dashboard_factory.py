from abc import ABC, abstractmethod

class Dashboard(ABC):
    @abstractmethod
    def get_data(self, user_id):
        pass

    @abstractmethod
    def get_actions(self):
        pass

class CustomerDashboard(Dashboard):
    def get_data(self, user_id):
        return {
            'type': 'customer',
            'my_orders': [],
            'recommendations': ['Product 1', 'Product 2'],
            'cart': {'items': 0, 'total': 0}
        }

    def get_actions(self):
        return ['browse', 'checkout', 'track_order']

class AdminDashboard(Dashboard):
    def get_data(self, user_id):
        return {
            'type': 'admin',
            'sales': 0,
            'inventory': 0,
            'users': 0,
            'pending_orders': []
        }

    def get_actions(self):
        return ['manage_orders', 'manage_inventory', 'view_users', 'generate_reports']

class DashboardFactory:
    @staticmethod
    def create_dashboard(user_role):
        if user_role == 'admin':
            return AdminDashboard()
        elif user_role == 'customer':
            return CustomerDashboard()
        else:
            raise ValueError(f"Unknown user role: {user_role}")
