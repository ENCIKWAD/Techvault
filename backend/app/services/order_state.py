"""
🎯 STATE PATTERN IMPLEMENTATION
================================
This file demonstrates the STATE design pattern for order lifecycle management.

Pattern: Behavioral Design Pattern
Purpose: Allow an order to change behavior as its internal state changes.
         Different states (Pending, Paid, Shipped, Received) have different behaviors.

Key Classes:
- OrderState: Abstract state interface
- PendingState: Order is pending
- PaidState: Payment confirmed
- ShippedState: Order shipped to customer
- ReceivedState: Customer received order (final state)
- Order: Context that manages state

State Transitions:
Pending → Paid → Shipped → Received

Related Files:
- backend/app/routes/order.py: Calls update_order_status to transition states
- backend/app/data_access/order_repository.py: Persists state in database
- frontend/js/orders.js: Displays current state to users

Usage Flow:
1. Order created in Pending state
2. Payment processed → Transition to Paid state
3. Admin ships → Transition to Shipped state
4. Customer receives → Transition to Received state (final)
5. Each state handles its own transitions and behaviors
"""

from abc import ABC, abstractmethod

class OrderState(ABC):
    @abstractmethod
    def next_state(self):
        pass

    @abstractmethod
    def get_status(self):
        pass

class PendingState(OrderState):
    def next_state(self):
        return PaidState()

    def get_status(self):
        return 'pending'

class PaidState(OrderState):
    def next_state(self):
        return ShippedState()

    def get_status(self):
        return 'paid'

class ShippedState(OrderState):
    def next_state(self):
        return ReceivedState()

    def get_status(self):
        return 'shipped'

class ReceivedState(OrderState):
    def next_state(self):
        return None

    def get_status(self):
        return 'received'

class Order:
    def __init__(self):
        self.state = PendingState()

    def advance_state(self):
        next_state = self.state.next_state()
        if next_state:
            self.state = next_state

    def get_current_status(self):
        return self.state.get_status()
