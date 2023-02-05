
class OrderObserver:
    def __init__(self):
        self.name = 'OrderObserver'
        self.orders = []
        self.recipients = {Accounting(), Warehouse()}

    def fixate_event(self, oid):
        for order in self.orders:
            if order.__dict__['oid'] == oid:
                self.updated_order = order
        self.notify_all()


    def notify_all(self):
        for recipient in self.recipients:
            recipient.react_order_updated(
                self.updated_order.oid,
                self.updated_order.status
            )


class Accounting:
    def __init__(self):
        pass

    def react_order_updated(self, oid, status):
        if status == 'paid':
            print('Order status has been updated to ' + status)
            self.send_order_to_warehouse(oid)

    def send_order_to_warehouse(self, oid):
        print('The order ' + str(oid) + ' has been paid. It can be built and given out')


class Warehouse:
    def __init__(self):
        pass

    def react_order_updated(self, oid, status):
        if status == 'built':
            print('Order status has been updated to ' + status)
            self.give_out_order(oid)

    def give_out_order(self, oid):
        print('The order ' + str(oid) + ' has been built and given out')






