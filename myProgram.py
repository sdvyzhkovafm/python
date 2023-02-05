from MyProxy import *
from WorkingClasses import *

manager = Manager()
builder = FurnitureProxyBuilder()

order = manager.create_order(300)
manager.fill_order(order, name="Table", width=0.9, height=1.2, color="black", material="dsp", legs_height=0.9)
manager.update_order_status(order, 'paid')
table = builder.build(order)
print(table.description)

order_cabinet = manager.create_order(1000)
manager.fill_order(order_cabinet,
    name='Cabinet', width=0.9, height=1.2, color="black", material="dsp", drawer_number=6, section_number=2)
manager.update_order_status(order_cabinet, 'paid')
cabinet = builder.build(order_cabinet)
print(cabinet.description)

order_wardrobe = manager.create_order(5000)
manager.fill_order(order_wardrobe,
    name='Wardrobe', width=3, height=2.5, color="black", material="dsp", drawer_number=8, section_number=3, shelf_number=8)
manager.update_order_status(order_wardrobe, 'paid')
wardrobe = builder.build(order_wardrobe)
print(wardrobe.description)

