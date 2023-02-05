myProgram is the file with the program executed. There user can make order and 
get a piece of furniture. 
User is able to order three types of furniture: Table, Cabinet and Wardrobe. Each 
of them has appropriate parameters: 
- table: length of legs _legs_height_
- cabinet: number of drawers, number of sections
- wardrobe: number of drawers _drawer_number_, number of sections _section_number_, 
and number of shelves _shelves_number_
common parameters for all furniture:
- _name_
- _color_
- _width_
- _height_
- _material_

First step to get a piece of furniture is to apply manager, so that the manager could
create an order with a price of the particular piece of furniture. After that manager fills
the order with appropriate information about parameters.
After the user provides paid bill manager moves the order forward.
At the end the user gets their piece of furniture.

Patterns:
Observer. Manager has built-in program that notifies accounting and warehouse about
every order status changing. Meanwhile, manager creates a new order they register this new 
order in observer. Manager changes status when the order gets paid. Another status changes are
fixated automatically

Proxy. Prepares materials and details according to the input order before it gets built. After
preparing, builder is called and assembles the ordered piece of furniture and packs it.

Chain of responsibility. There are three handlers in the building process: cutter to cut material,
assembler to assemble the piece of furniture and packager to prepare it before the user gets their order

Builder. Builder returns new piece of furniture

Perhaps, something is inconsistent in my scenario. I tried to adapt this story as close as I could to real 
furniture building process