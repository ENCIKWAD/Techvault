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
