from abc import ABC, abstractmethod
import pytest

class VendingMachine:
    def __init__(self, products):
        self.products = products
        self.balance = 0
        self.state = IdleState(self)

    def set_state(self, state):
        self.state = state

    def insert_coin(self, amount):
        self.state.insert_coin(amount)

    def select_product(self, product_id):
        self.state.select_product(product_id)

    def cancel(self):
        self.state.cancel()

    def refill(self, product_id, amount):
        self.state.refill(product_id, amount)


class State(ABC):
    def __init__(self, machine):
        self.machine = machine

    @abstractmethod
    def insert_coin(self, amount): pass

    @abstractmethod
    def select_product(self, product_id): pass

    @abstractmethod
    def cancel(self): pass

    @abstractmethod
    def refill(self, product_id, amount): pass


class IdleState(State):
    def insert_coin(self, amount):
        self.machine.balance += amount
        self.machine.set_state(HasMoneyState(self.machine))

    def select_product(self, product_id):
        pass

    def cancel(self):
        pass

    def refill(self, product_id, amount):
        if product_id in self.machine.products:
            self.machine.products[product_id]["stock"] += amount


class HasMoneyState(State):
    def insert_coin(self, amount):
        self.machine.balance += amount

    def select_product(self, product_id):
        product = self.machine.products.get(product_id)
        if not product:
            return

        if product["stock"] == 0:
            self.machine.set_state(OutOfStockState(self.machine))
            return

        if self.machine.balance < product["price"]:
            return

        self.machine.balance -= product["price"]
        product["stock"] -= 1

        if product["stock"] == 0:
            self.machine.set_state(OutOfStockState(self.machine))
        else:
            self.machine.set_state(IdleState(self.machine))

    def cancel(self):
        self.machine.balance = 0
        self.machine.set_state(IdleState(self.machine))

    def refill(self, product_id, amount):
        pass


class DispensingState(State):
    def insert_coin(self, amount): pass
    def select_product(self, product_id): pass
    def cancel(self): pass
    def refill(self, product_id, amount): pass


class OutOfStockState(State):
    def insert_coin(self, amount): pass

    def select_product(self, product_id): pass

    def cancel(self):
        self.machine.balance = 0
        self.machine.set_state(IdleState(self.machine))

    def refill(self, product_id, amount):
        if product_id in self.machine.products:
            self.machine.products[product_id]["stock"] += amount
            self.machine.set_state(IdleState(self.machine))


class MaintenanceState(State):
    def insert_coin(self, amount): pass
    def select_product(self, product_id): pass
    def cancel(self): pass

    def refill(self, product_id, amount):
        if product_id in self.machine.products:
            self.machine.products[product_id]["stock"] += amount
            

# Tests

def create_machine():
    products = {
        "cola": {"name": "Cola", "price": 10, "stock": 1},
        "water": {"name": "Water", "price": 5, "stock": 1}
    }
    return VendingMachine(products)


def test_insert_coin_changes_state():
    vm = create_machine()
    vm.insert_coin(10)
    assert isinstance(vm.state, HasMoneyState)


def test_successful_purchase():
    vm = create_machine()
    vm.insert_coin(10)
    vm.select_product("cola")

    assert vm.balance == 0
    assert vm.products["cola"]["stock"] == 0
    assert isinstance(vm.state, OutOfStockState)


def test_insufficient_funds():
    vm = create_machine()
    vm.insert_coin(5)
    vm.select_product("cola")

    assert vm.balance == 5
    assert vm.products["cola"]["stock"] == 1
    assert isinstance(vm.state, HasMoneyState)


def test_cancel_refunds_and_returns_idle():
    vm = create_machine()
    vm.insert_coin(10)
    vm.cancel()

    assert vm.balance == 0
    assert isinstance(vm.state, IdleState)


def test_out_of_stock_transition():
    vm = create_machine()

    vm.insert_coin(10)
    vm.select_product("cola")

    vm.insert_coin(10)
    vm.select_product("cola")

    assert isinstance(vm.state, OutOfStockState)


def test_refill_from_out_of_stock():
    vm = create_machine()

    vm.insert_coin(10)
    vm.select_product("cola")

    vm.refill("cola", 1)

    assert vm.products["cola"]["stock"] == 1
    assert isinstance(vm.state, IdleState)