from MyChainOfResponsibility import Assemble
from MyChainOfResponsibility import Package

class FurnitureBuilder:
    def __init__(self):
        self.handlers = {Assemble(), Package()}

    def build_furniture(self, order):
        while order.status != 'packed':
            for handler in self.handlers:
                handler.handle(order)
        return Furniture(order)


class Furniture:
    def __init__(self, order):
        self.name = order.name
        self.color = order.color
        self.material = order.material
        self.description = 'You get a ' + self.name + ', having a ' + self.color + ' color, ' + 'created from ' + self.material + '.'
        self.details = order.details
