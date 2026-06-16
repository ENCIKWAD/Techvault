from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount, user_id):
        pass

class CreditCardPayment(PaymentStrategy):
    def process_payment(self, amount, user_id):
        print(f"   💳 CreditCardPayment: Processing RM{amount} for user {user_id}")
        print(f"   💳 CreditCardPayment: Payment authorized ✓")
        return {'success': True, 'method': 'credit_card', 'amount': amount}

class CashOnDeliveryPayment(PaymentStrategy):
    def process_payment(self, amount, user_id):
        print(f"   💵 CashOnDeliveryPayment: COD order RM{amount} for user {user_id}")
        print(f"   💵 CashOnDeliveryPayment: Awaiting cash on delivery ⏳")
        return {'success': True, 'method': 'cod', 'amount': amount}

class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        print(f"   🏗️ PaymentProcessor: Initialized with {strategy.__class__.__name__}")
        self.strategy = strategy

    def pay(self, amount, user_id):
        print(f"   💰 PaymentProcessor.pay(): Executing payment strategy...")
        return self.strategy.process_payment(amount, user_id)
