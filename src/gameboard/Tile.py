class Tile:
    def __init__(self, resource='Wheat', location=[0, 0, 0]):
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

    def update_buildings(self, index, player):
        self.__buildings[index]

    def get_robber(self):
        return self.__robber

    def get_buildings(self):
        return self.__buildings

    def get_location(self):
        return self.__location

    def set_location(self, location):
        self.__location = location

    robber = property(get_robber, set_robber)
    buildings = property(get_buildings, update_buildings)
    resource = property(get_resource)
    location = property(get_location, set_location)
    number = property(get_number, set_number)
