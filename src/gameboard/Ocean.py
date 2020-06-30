
class Tile:
    def __init__(self, resource='Ocean', location=[0, 0, 0]):
        self.__resource = resource
        self.__robber = False
        self.__location = location

    def get_resource(self):
        return self.__resource

    def set_robber(self, value):
        self.__robber = value

    def get_robber(self):
        return self.__robber

    def on_roll(self):
        if self.__robber:
            pass
        else:
            pass
        # iterate settlements-cities around this tile
        # each get 1-2 of this ones resource

    def get_location(self):
        return self.__location

    def set_location(self, location):
        self.__location = location

    robber = property(get_robber, set_robber)
    resource = property(get_resource)
    location = property(get_location, set_location)
