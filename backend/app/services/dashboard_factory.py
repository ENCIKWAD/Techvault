"""
🎯 FACTORY METHOD PATTERN IMPLEMENTATION
=========================================
This file demonstrates the FACTORY METHOD design pattern for dashboard creation.

Pattern: Creational Design Pattern
Purpose: Define an interface for creating objects, but let subclasses decide
         which class to instantiate based on parameters.

Key Classes:
- Dashboard: Abstract product interface
- AdminDashboard: Concrete product for admin users
- CustomerDashboard: Concrete product for customer users
- DashboardFactory: Factory that creates appropriate dashboard

Factory Method:
- DashboardFactory.create_dashboard(user_role): Creates correct dashboard type

Dashboard Types:
- AdminDashboard: Shows product management, order management
- CustomerDashboard: Shows product catalog, cart, orders

Related Files:
- frontend/js/admin.js: Determines user role and displays appropriate dashboard
- frontend/pages/admin.html: Admin dashboard UI
- frontend/pages/index.html: Customer dashboard UI

Usage Flow:
1. User logs in, role is stored (admin or customer)
2. Frontend determines which dashboard to show
3. DashboardFactory.create_dashboard(role) is called
4. Factory returns appropriate dashboard instance
5. Dashboard data and actions are displayed
6. No client code knows concrete dashboard classes

Benefits:
- Encapsulation of object creation
- Easy to add new dashboard types
- Single responsibility: factory only creates
- Open/closed principle: open for extension, closed for modification
- Clients don't depend on concrete classes
"""

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
