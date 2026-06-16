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
