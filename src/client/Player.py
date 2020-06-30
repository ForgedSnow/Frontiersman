class PlayerResourceHand:
    def __init__(self):
        self.brick = 0
        self.grain = 0
        self.lumber = 0
        self.ore = 0
        self.wool = 0
        self.totalResources = 0


class PlayerDevelopmentHand:
    def __init__(self):
        self.knights = 0
        self.roadBuildings = 0
        self.yearOfPlenty = 0
        self.monopolies = 0
        self.victoryPoints = 0
        self.totalDevelopments = 0
    def add_card(self, card):
        if card=='knight':
            self.knights += 1
        elif card=='roadBuilding':
            self.roadBuildings  += 1
        elif card=='yearOfPlenty':
            self.yearOfPlenty  += 1
        elif card=='monopoly':
            self.monopolies += 1
        elif card=='victoryPoint':
            self.victoryPoints  += 1
        self.totalDevelopments +=1
    def remove_card(self, card):
        if card=='knight':
            self.knights -= 1
        elif card=='roadBuilding':
            self.roadBuildings  -= 1
        elif card=='yearOfPlenty':
            self.yearOfPlenty  -= 1
        elif card=='monopoly':
            self.monopolies -= 1
        elif card=='victoryPoint':
            self.victoryPoints  -= 1
        self.totalDevelopments -=1

class TradeRatios:
    def __init__(self):
        self.brick = 4
        self.grain = 4
        self.lumber = 4
        self.ore = 4
        self.wool = 4

    def update(self, resource):
        if resource == "Brick":
            self.brick = 2
        elif resource == "Wheat":
            self.grain = 2
        elif resource == "Wood":
            self.lumber = 2
        elif resource == "Ore":
            self.ore = 2
        elif resource == "Sheep":
            self.wool = 2
        elif resource == "None":
            self.brick = min(self.brick, 3)
            self.grain = min(self.grain, 3)
            self.lumber = min(self.lumber, 3)
            self.ore = min(self.ore, 3)
            self.wool = min(self.wool, 3)


class EnemyPlayer:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.handSize = '0'
        self.developmentSize = '0'
        self.visibleVictoryPoints = '0'
        self.numRoads = '15'
        self.numSettlements = '5'
        self.numCities = '4'
        self.longestRoad = '0'
        self.largestArmy = '0'

    def updateEnemy(self, data):
        self.name = data[0]
        self.color = data[1]
        self.handSize = data[2]
        self.developmentSize = data[3]
        self.visibleVictoryPoints = data[4]
        self.numRoads = data[5]
        self.numSettlements = data[6]
        self.numCities = data[7]
        self.longestRoad = data[8]
        self.largestArmy = data[9]


class Player:
    def __init__(self, name, color):
        self.color = color
        self.name = name
        self.numRoads = 15
        self.numSettlements = 5
        self.numCities = 4
        self.longestRoad = 0
        self.claimLongestRoad = False
        self.largestArmy = 0
        self.claimLargestArmy = False
        self.victoryPoints = 0
        self.hiddenVictoryPoints = 0
        self.resourceHand = PlayerResourceHand()
        self.developmentHand = PlayerDevelopmentHand()
        self.bankTrading = TradeRatios()
        self.development_card_played=False
        self.ownedRoads = list()
        self.ownedNodes = list()

    def getNumResources(self):
        return self.resourceHand.totalResources

    def getNumDevelopment(self):
        return self.developmentHand.totalDevelopments

    def getSendToEnemies(self):
        toSend = ','.join([self.name, self.color,
                           str(self.resourceHand.totalResources), str(self.developmentHand.totalDevelopments),
                           str(self.victoryPoints), str(self.numRoads), str(self.numSettlements), str(self.numCities),
                           str(self.numCities),
                           str(self.longestRoad), str(self.largestArmy)])
        return toSend


    # todo has problem with joining established roads

    def acquireRoad(self, road):
        self.ownedRoads.append(road)

        roadStack = list()
        roadStack.append(road)
        roadChecked = list()
        roadChecked.append(road)

        toCheck = self.longestRoadValue(roadStack, roadChecked)
        if self.longestRoad < toCheck:
            self.longestRoad = toCheck

    def longestRoadValue(self, roadStack, roadChecked, length=1):
        current = roadStack.pop()
        toReturn = length
        for corner in current.corners:
            for edge in corner.edges:
                if edge is not None and (edge not in roadChecked) and (edge.color == self.color):
                    roadStack.append(edge)
                    roadChecked.append(edge)
                    lengthCheck = self.longestRoadValue(roadStack, roadChecked, length + 1)
                    if toReturn < lengthCheck:
                        toReturn = lengthCheck
        return toReturn


    def acquireNode(self, node):
        self.ownedNodes.append(node)
        self.numSettlements -= 1
        self.victoryPoints += 1

    def acquireCity(self):
        self.numCities -= 1
        self.numSettlements += 1
        self.victoryPoints += 1

    def addResources(self, updateframe):
        self.resourceHand.brick += updateframe[0]
        self.resourceHand.grain += updateframe[1]
        self.resourceHand.lumber += updateframe[2]
        self.resourceHand.ore += updateframe[3]
        self.resourceHand.wool += updateframe[4]

        self.resourceHand.totalResources += sum(updateframe)
