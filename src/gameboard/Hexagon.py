import math


class Hexagon:
    def __init__(self, radius, flat=True):
        self.__radius = radius
        self.__points = []
        self.__flat = flat
        self.construct_hexagon()

    def construct_hexagon(self):
        # clockwise starting from north
        width = 0.5 * self.__radius
        height = self.__radius * math.sin(math.pi / 3)
        if self.__flat:
            # construct generic hexagon
            self.__points = [(0 + width, 0 + height),
                             (self.__radius, 0),
                             (0 + width, 0 - height),
                             (0 - width, 0 - height),
                             (-self.__radius, 0),
                             (0 - width, 0 + height)]
        else:
            self.__points = [(0, self.__radius),
                             (height, width),
                             (height, -width),
                             (0, -self.__radius),
                             (-height, -width),
                             (-height, width)]

    def get_points(self):
        return self.__points

    def offset_flat(self, location, origin):
        if location == (0, 0, 0):
            return self.__points

        y_constant = self.__radius * (3 ** 0.5) / 2

        if location[0] == 0:
            x_off = 0
        elif location[0] % 2 == 0:
            if location[0] > 0:
                x_off = self.__radius * (location[0] + 1)
            else:
                x_off = self.__radius * (location[0] - 1)
        else:
            if location[0] > 0:
                x_off = (location[0] + 0.5) * self.__radius
            else:
                x_off = (location[0] - 0.5) * self.__radius

        y_off = (location[1] - location[2]) * y_constant

        result = []

        for point in self.__points:
            result.append((int(point[0] + x_off + origin[0]),
                           int(point[1] - y_off + origin[1])))
        return result

    def offset_pointy(self, location, origin):
        if location == (0, 0, 0):
            return self.__points

        y_constant = self.__radius * (3 ** 0.5) / 2

        if location[0] == 0:
            x_off = 0
        elif location[0] % 2 == 0:
            if location[0] > 0:
                x_off = self.__radius * (location[0] + 1)
            else:
                x_off = self.__radius * (location[0] - 1)
        else:
            if location[0] > 0:
                x_off = (location[0] + 0.5) * self.__radius
            else:
                x_off = (location[0] - 0.5) * self.__radius

        y_off = (location[1] - location[2]) * y_constant

        result = []

        for point in self.__points:
            result.append((int(point[0] + y_off + origin[0]),
                           int(point[1] - x_off + origin[1])))
        return result

    points = property(get_points)
