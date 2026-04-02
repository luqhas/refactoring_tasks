class OrderManager:
    def __init__(self, db_conn, smtp_host, smtp_port, tax_rate, currency):
        self.db = db_conn
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.tax_rate = tax_rate
        self.currency = currency
        self.orders = []
        self.users = {}
        self.inventory = {}

    def create_order(self, user_id, items, promo_code=None):
        # validate user
        if user_id not in self.users:
            raise Exception('User not found')
        if self.users[user_id]['banned']:
            raise Exception('User is banned')
        # validate items
        for item_id, qty in items.items():
            if item_id not in self.inventory:
                raise Exception(f'Item {item_id} not found')
            if self.inventory[item_id]['stock'] < qty:
                raise Exception(f'Insufficient stock for {item_id}')
        # calculate price
        total = 0
        for item_id, qty in items.items():
            price = self.inventory[item_id]['price'] * qty
            total += price
        if promo_code == 'SAVE10': total *= 0.9
        elif promo_code == 'SAVE20': total *= 0.8
        total = total * (1 + self.tax_rate)
        # update inventory
        for item_id, qty in items.items():
            self.inventory[item_id]['stock'] -= qty
        # save to db
        order = {'id': len(self.orders)+1, 'user': user_id,
                 'items': items, 'total': total, 'status': 'new'}
        self.orders.append(order)
        self.db.execute(f'INSERT INTO orders VALUES ({order})')
        # send email
        import smtplib
        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        server.sendmail('shop@store.com', self.users[user_id]['email'],
                        f'Order {order["id"]} confirmed. Total: {total}')
        server.quit()
        return order