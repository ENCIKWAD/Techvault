"""
🎯 OBSERVER PATTERN IMPLEMENTATION
===================================
This file demonstrates the OBSERVER design pattern for notification system.

Pattern: Behavioral Design Pattern
Purpose: Define a one-to-many dependency between objects.
         When order status changes, all observers are notified automatically.

Key Classes:
- Observer: Abstract observer interface
- EmailNotifier: Concrete observer for email notifications
- SMSNotifier: Concrete observer for SMS notifications
- OrderNotificationManager: Subject that notifies all observers

Observers:
- EmailNotifier: Sends email when order status changes
- SMSNotifier: Sends SMS when order status changes
- (Can add more observers without changing existing code)

Related Files:
- backend/app/routes/order.py: Creates notification_manager and calls notify_status_change()
- backend/app/data_access/order_repository.py: Updates order status in database

Usage Flow:
1. OrderNotificationManager initialized with observers (Email, SMS)
2. Order status changes (pending → paid, paid → shipped, etc.)
3. notify_status_change() called
4. All attached observers are notified automatically
5. Each observer handles its own notification logic independently
6. New observers can be added without modifying existing code

Benefits:
- Loose coupling between subject and observers
- Easy to add/remove observers at runtime
- Each observer has single responsibility
"""

from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, order_id, status):
        pass

class EmailNotifier(Observer):
    def update(self, order_id, status):
        print(f"   📧 EmailNotifier: Sending email for order #{order_id} - Status: {status}")
        return True

class SMSNotifier(Observer):
    def update(self, order_id, status):
        print(f"   📱 SMSNotifier: Sending SMS for order #{order_id} - Status: {status}")
        return True

class OrderNotificationManager:
    def __init__(self):
        self.observers = []

    def attach(self, observer: Observer):
        self.observers.append(observer)
        print(f"   ➕ Attached observer: {observer.__class__.__name__}")

    def detach(self, observer: Observer):
        self.observers.remove(observer)

    def notify_status_change(self, order_id, status):
        print(f"   🔔 OrderNotificationManager: Status change notification")
        print(f"      Order #{order_id} → {status}")
        print(f"      Notifying {len(self.observers)} observers:")
        for observer in self.observers:
            observer.update(order_id, status)
