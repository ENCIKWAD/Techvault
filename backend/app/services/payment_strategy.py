"""
🎯 STRATEGY PATTERN IMPLEMENTATION
===================================
This file demonstrates the STRATEGY design pattern for payment processing.

Pattern: Behavioral Design Pattern
Purpose: Define a family of payment algorithms (Credit Card, Cash on Delivery)
         and make them interchangeable.

Key Classes:
- PaymentStrategy: Abstract strategy interface
- CreditCardPayment: Concrete strategy for card payments
- CashOnDeliveryPayment: Concrete strategy for COD payments
- PaymentProcessor: Context that uses the strategy

Related Files:
- backend/app/routes/order.py: Uses PaymentProcessor to execute payment
- frontend/js/cart.js: Selects payment method (triggers strategy selection)

Usage Flow:
1. User selects payment method at checkout
2. Appropriate strategy is instantiated (CreditCardPayment or CashOnDeliveryPayment)
3. PaymentProcessor executes the selected strategy
4. Different payment logic runs without modifying existing code
"""

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
