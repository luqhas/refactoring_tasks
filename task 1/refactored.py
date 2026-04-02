from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, total):
        return total

class Save10Discount(DiscountStrategy):
    def apply(self, total):
        return total * 0.9

class Save20Discount(DiscountStrategy):
    def apply(self, total):
        return total * 0.8


class PricingService:
    def __init__(self, tax_rate, discount_strategy: DiscountStrategy):
        self.tax_rate = tax_rate
        self.discount_strategy = discount_strategy

    def calculate(self, items, inventory):
        total = sum(inventory[i]['price'] * q for i, q in items.items())
        total = self.discount_strategy.apply(total)
        return total * (1 + self.tax_rate)


class OrderValidator:
    def validate_user(self, user_id, users):
        if user_id not in users:
            raise Exception('User not found')
        if users[user_id]['banned']:
            raise Exception('User is banned')

    def validate_items(self, items, inventory):
        for item_id, qty in items.items():
            if item_id not in inventory:
                raise Exception(f'Item {item_id} not found')
            if inventory[item_id]['stock'] < qty:
                raise Exception(f'Insufficient stock for {item_id}')


class InventoryService:
    def update_stock(self, items, inventory):
        for item_id, qty in items.items():
            inventory[item_id]['stock'] -= qty


class OrderRepository:
    def __init__(self, db):
        self.db = db

    def save(self, order):
        self.db.execute(f'INSERT INTO orders VALUES ({order})')


class NotificationService:
    def __init__(self, smtp_client):
        self.smtp = smtp_client

    def send_order_confirmation(self, email, order_id, total):
        self.smtp.sendmail(
            'shop@store.com',
            email,
            f'Order {order_id} confirmed. Total: {total}'
        )


class OrderManager:
    def __init__(self, validator, pricing, inventory_service,
                 repository, notifier, users, inventory):
        self.validator = validator
        self.pricing = pricing
        self.inventory_service = inventory_service
        self.repository = repository
        self.notifier = notifier
        self.users = users
        self.inventory = inventory
        self.orders = []

    def create_order(self, user_id, items):
        self.validator.validate_user(user_id, self.users)
        self.validator.validate_items(items, self.inventory)

        total = self.pricing.calculate(items, self.inventory)

        self.inventory_service.update_stock(items, self.inventory)

        order = {
            'id': len(self.orders) + 1,
            'user': user_id,
            'items': items,
            'total': total,
            'status': 'new'
        }

        self.orders.append(order)
        self.repository.save(order)

        email = self.users[user_id]['email']
        self.notifier.send_order_confirmation(email, order['id'], total)

        return order
