import random
from MyObserver import *

class Manager:
    def __init__(self):
        self.order_observer = OrderObserver()

    def create_order(self, sum):
        print('Order created ' + str(sum))
        order = Order(sum)
        self.register_order_in_observer(order)
        return order

    def fill_order(self, order, **kwargs):
        order.name = kwargs['name']
        order.width = kwargs['width']
        order.height = kwargs['height']
        order.color = kwargs['color']
        order.material = kwargs['material']
        if kwargs['name'] == 'Table':
            order.legs_height = kwargs['legs_height']
        elif kwargs['name'] == 'Cabinet':
            order.drawer_number = kwargs['drawer_number']
            order.section_number = kwargs['section_number']
        elif kwargs['name'] == 'Wardrobe':
            order.drawer_number = kwargs['drawer_number']
            order.section_number = kwargs['section_number']
            order.shelf_number = kwargs['shelf_number']

    def register_order_in_observer(self, order):
        self.order_observer.orders.append(order)
        order.observer = self.order_observer

    def update_order_status(self, order, status):
        order.status = status
        self.order_observer.fixate_event(order.oid)


class Order:
    def __init__(self, sum):
        self.oid = random.randint(0, 500)
        self.sum = sum
        self.status = 'created'



