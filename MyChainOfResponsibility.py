class Cut:
    def __init__(self):
        self.operation_type = 'cut'
        pass

    def handle(self, order):
        if order.status == 'paid':
            for details_type in order.details:
                for key in details_type.keys():
                    if key != 'furniture':
                        print(key + ' has been cut successfully')
            order.status = self.operation_type
            order.observer.fixate_event(order.oid)


class Assemble:
    def __init__(self):
        self.operation_type = 'built'

    def handle(self, order):
        if order.status == 'cut':
            print(order.name + ' has been assembled successfully')
            order.status = self.operation_type
            order.observer.fixate_event(order.oid)


class Package:
    def __init__(self):
        self.operation_type = 'packed'

    def handle(self, order):
        if order.status == 'built':
            print(order.name + ' has been packed successfully')
            order.status = self.operation_type
            order.observer.fixate_event(order.oid)

