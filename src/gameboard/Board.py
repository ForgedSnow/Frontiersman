class Vertex:
    def __init__(self, location=(0, 0, 0)):
        self.location = location
        self.neighbors = [None, None, None]


class Tile:
    def __init__(self, resource='Wheat', location=(0, 0, 0)):
        self.__resource = resource
        self.__robber = False
        self.__location = location
        self.__roads = []
        self.__buildings = []
        self.__number = 0
        # roads and building list start due north and iterate clockwise

    def get_number(self):
        return self.__number

    def set_number(self, integer):
        self.__number = integer

    def get_resource(self):
        return self.__resource

    def set_robber(self, value):
        self.__robber = value

    # def update_buildings(self, index, player):
    #    self.__buildings[index]

    def get_robber(self):
        return self.__robber

    def get_buildings(self):
        return self.__buildings

    def get_location(self):
        return self.__location

    def set_location(self, location):
        self.__location = location

    robber = property(get_robber, set_robber)
    buildings = property(get_buildings)  # , update_buildings)
    resource = property(get_resource)
    location = property(get_location, set_location)
    number = property(get_number, set_number)


class Port:
    def __init__(self, location=(0, 0, 0)):
        self.location = location
        self.specialty = False
        self.trade = 'None'
        self.is_port = False
        self.rate = 4

    def set_property(self, location, resource='None'):
        self.location = location
        self.trade = resource

    def get_type(self):
        return self.trade

    def set_type(self, trade):
        if trade == 'None':
            self.rate = 3
        else:
            self.rate = 2
        self.trade = trade
        self.is_port = True

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location

    resource = property(get_type, set_type)


class Board:
    def __init__(self):
        self.num_resource_tiles = 19
        self.num_ocean_tiles = 18
        self.num_ports = 9
        self.ocean_location_list = []
        self.fill_ocean_location_list()
        self.lookup_table = {2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
        self.location_list = []
        self.fill_location_list()
        self.__ocean_tiles = []
        self.ports = []
        self.robber = None
        self.__resource_tiles = []
        self.direction_array = [
            (0, 1, -1),  # top left
            (1, 0, -1),  # top right
            (1, -1, 0),  # right
            (0, -1, 1),  # bottom right
            (-1, 0, 1),  # bottom left
            (-1, 1, 0)  # left
        ]

        # 2d array to reference tiles by coordinate
        self.__array = []
        for index in range(0, 7):
            self.__array.append([0, 0, 0, 0, 0, 0, 0])
        self.translate_to_3d()

    def form_ocean(self):
        pass

    def get_array(self):
        return self.__array

    def translate_to_3d(self):
        for tile in self.__resource_tiles:
            self.__array[int(tile.location[0]) + 3][int(tile.location[1]) + 3] = tile
        for port in self.ports:
            self.__array[int(port.location[0]) + 3][int(port.location[1]) + 3] = port

    def get_tile(self, tup):
        return self.__array[int(tup[0] + 3)][int(tup[1] + 3)]

    def get_resource_list(self):
        return self.__resource_tiles

    def get_ocean_list(self):
        return self.__ocean_tiles

    def get_port_list(self):
        return self.ports

    def generate_land(self, number_list, resource_list):
        count = 0

        # assign tile resource
        for index in self.location_list:
            self.__resource_tiles.append(
                Tile(resource_list[count], index))
            count += 1

        # assign tile numbers
        index = 0
        for tile in self.__resource_tiles:
            if tile.resource == 'Desert':
                tile.number = 7
                tile.set_robber(True)
                self.robber = tile
            else:
                tile.number = number_list[index]
                self.lookup_table[number_list[index]].append(tile)
                index += 1
    def xy_give_port(self, location):
        valid_ports = \
            [
                [0, 0, 1, 1, 0, 2, 2, 0, 0, 0, 0],
                [0, 9, 0, 0, 0, 0, 0, 0, 3, 3, 0],
                [0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 4],
                [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 4],
                [0, 8, 0, 0, 0, 0, 0, 0, 5, 5, 0],
                [0, 0, 7, 7, 0, 6, 6, 0, 0, 0, 0]]
        index = valid_ports[location[1]][location[0]]
        if index == 0:
            return None
        else:
            return self.ports[index - 1]

    def generate_ocean(self):
        # add ocean, not really used
        for index in self.ocean_location_list:
            self.__ocean_tiles.append(Port(index))

    def print_ports(self):
        for port in self.__ocean_tiles:
            if port.is_port:
                print(port.location, port.rate, port.resource)

    def generate_ports(self, port_list):
        self.generate_ocean()
        index = 0
        even = 0
        for tile in self.__ocean_tiles:
            if even % 2 == 0:
                tile.set_type(port_list[index])
                self.ports.append(tile)
                index += 1
            even += 1

    def set_robber(self, location):
        self.robber.set_robber(False)
        self.robber = self.get_tile(location)
        self.robber.set_robber(True)

    def get_robber(self):
        return (self.robber)

    def fill_ocean_location_list(self):
        self.ocean_location_list.append([0, 3, -3])
        self.ocean_location_list.append([1, 2, -3])
        self.ocean_location_list.append([2, 1, -3])
        self.ocean_location_list.append([3, 0, -3])
        self.ocean_location_list.append([3, -1, -2])
        self.ocean_location_list.append([3, -2, -1])
        self.ocean_location_list.append([3, -3, 0])
        self.ocean_location_list.append([2, -3, 1])
        self.ocean_location_list.append([1, -3, 2])
        self.ocean_location_list.append([0, -3, 3])
        self.ocean_location_list.append([-1, -2, 3])
        self.ocean_location_list.append([-2, -1, 3])
        self.ocean_location_list.append([-3, 0, 3])
        self.ocean_location_list.append([-3, 1, 2])
        self.ocean_location_list.append([-3, 2, 1])
        self.ocean_location_list.append([-3, 3, 0])
        self.ocean_location_list.append([-2, 3, -1])
        self.ocean_location_list.append([-1, 3, -2])

    def fill_location_list(self):
        self.location_list.append([0, 2, -2])
        self.location_list.append([1, 1, -2])
        self.location_list.append([2, 0, -2])
        self.location_list.append([-1, 2, -1])
        self.location_list.append([0, 1, -1])
        self.location_list.append([1, 0, -1])
        self.location_list.append([2, -1, -1])
        self.location_list.append([-2, 2, 0])
        self.location_list.append([-1, 1, 0])
        self.location_list.append([0, 0, 0])
        self.location_list.append([1, -1, 0])
        self.location_list.append([2, -2, 0])
        self.location_list.append([-2, 1, 1])
        self.location_list.append([-1, 0, 1])
        self.location_list.append([0, -1, 1])
        self.location_list.append([1, -2, 1])
        self.location_list.append([-2, 0, 2])
        self.location_list.append([-1, -1, 2])
        self.location_list.append([0, -2, 2])

    land_list = property(get_resource_list)
    ocean_list = property(get_ocean_list)
    port_list = property(get_port_list)
