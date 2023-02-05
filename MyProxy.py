from MyBuilder import FurnitureBuilder
from MyChainOfResponsibility import Cut

class FurnitureProxyBuilder:
    def __init__(self):
        self.builder = FurnitureBuilder()
        self.handler = Cut()
        self.new_furniture_parameters = []

    # Build new piece of furniture
    def build(self, order):
        order.details = self.get_list_of_elements(order)
        self.handler.handle(order)


        return self.builder.build_furniture(order)

    # Figure out amount of marerials, fitting, etc.
    def get_list_of_elements(self, order):
        details = []
        if order.name == 'Table':
            details.append({'dsp': [{f'{order.width} * {order.height}': 1}]})
            details.append({'tree': [
                {f'{order.legs_height} * {0.04} * {0.04}': 4},
                {f'{order.height - 0.2} * {0.1} * {0.02}': 2},
                {f'{order.width - 0.2 - 0.04}* {0.1} * {0.02}': 2}
            ]})
            details.append({'fittings': [
                {'stiazhka': 4},
                {'kreplenije': 8},
                {'samorezy': 8}
            ]})
        elif order.name == 'Cabinet':
            # details.append({'dsp': [
            dsp = [
                {f'{order.width} * {0.6}': 2},
                {f'{order.height} * {0.6}': 2},
                {f'{0.58} * {0.15}': order.drawer_number * 2}
            ]
            drawer_width = order.width - 0.036 - 0.024
            if order.section_number > 1:
                drawer_width = (drawer_width - (order.section_number - 1) * 0.018) / order.section_number
                drawer_front_width = order.width / order.section_number - (order.section_number - 1)
                drawer_front_height = ((order.height - 0.038) / (
                            order.drawer_number / (order.section_number - 1))) - (
                                                (order.drawer_number / (order.section_number - 1)) - 1)
                dsp.append(
                    {f'{order.height - 0.036} * {0.582}': order.section_number - 1}
                )
            else:
                drawer_front_width = order.width
                drawer_front_height = ((order.height - 0.038) / order.drawer_number) - (order.drawer_number - 1)

            drawer_details = [
                {f'{drawer_width - 0.036} *{0.15}': order.drawer_number * 2},
                {f'{drawer_width - 0.036} * {0.58 - 0.036}': order.drawer_number}
            ]
            dsp.extend(drawer_details)
            details.append({'dsp': dsp})
            details.append({'fittings': [
                {'nozhki': 4},
                {'napravliajuschie': order.drawer_number * 2},
                {'samorezy': 16 + order.drawer_number * 2 * 3},
                {'ugolki': 8},
                {'konfirmat': order.drawer_number * 12 + 6},
                {'gvozdi': 12},
                {'ruchki': order.drawer_number}
            ]})
            details.append({'mdf': [{f'{drawer_front_width} * {drawer_front_height}': order.drawer_number}]})
            details.append({'hdf': [{f'{order.width - 4} *{order.height - 4}': 1}]})

        elif order.name == 'Wardrobe':
            # details.append({'dsp': [
            dsp = [
                {f'{order.width} * {0.6}': 2},
                {f'{order.height} * {0.6}': 2},
                {f'{order.height - 0.036} * {0.6}': order.section_number - 1},
                {f'{0.58} * {0.15}': order.drawer_number * 2}
            ]
            section_width = ((order.width - 0.036) / (order.section_number - 1)) - (
                        (order.section_number - 1) * 0.018)

            wardrobe_details = [
                {f'{section_width - 0.024} * {0.15}': order.drawer_number * 2},
                {f'{section_width - 0.024 - 0.036} * {0.58 - 0.036}': order.drawer_number},
                {f'{section_width} * {0.58}': order.shelf_number}
            ]
            dsp.extend(wardrobe_details)
            details.append({'dsp': dsp})
            details.append({'mdf': [
                {f'{section_width - 0.024} * {0.2}': order.drawer_number},
                {f'{order.width / order.section_number - (order.section_number - 1)} * {order.height}': order.section_number}
            ]})

            details.append({'fittings': [
                {'nozhki': 4},
                {'napravliajuschie': order.drawer_number * 2},
                {'samorezy': 8},
                {'konfirmat': order.drawer_number * 12 + (order.section_number - 1) * 4 + 8},
                {'gvozdi': 20},
                {'ugolki': 4},
                {'ruchki': order.section_number}
            ]})

            details.append({'hdf': [{f'{order.width - 4} * {order.height - 4}': 1}]})

        return details
