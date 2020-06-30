import math, sys

# Class defining corners of hexagons
class CornerNode:
    @staticmethod
    def translate_settlement(location, origin, radius, sideLength=3):
        toReturnX = 0
        toReturnY = 0
        edgeDist = (radius / 2) * math.sqrt(3)
        cornerDist = radius

        toReturnX = location[0] * edgeDist
        if (location[0] % 2) == 0:
            toReturnY = (radius / 2) + \
                        (int(location[1] / 2) * (3 * radius)) + \
                        ((location[1] % 2) * radius)
        elif (location[0] % 2) == 1:
            toReturnY = (int(location[1] / 2) * (3 * radius)) + \
                        ((location[1] % 2) * (radius * 2))

        ourXOffset = ((sideLength - 1) * 2) * edgeDist
        ourYOffset = edgeDist + ((sideLength - 1.5) * ((radius / 2) * 3))
        totalXOffset = origin[0] - ourXOffset + 12.5
        totalYOffset = origin[1] - ourYOffset + 12.5

        return int(toReturnX + totalXOffset), int(toReturnY + totalYOffset)

    def __init__(self, r=False, c1=None, c2=None):
        self.real = r
        self.hexs = list()
        self.edges = list()
        self.cord1 = c1
        self.cord2 = c2
        self.available = r
        self.color = None
        self.city = False

    def addHexs(self, h1, h2, h3):
        self.hexs.clear()
        self.hexs.append(h1)
        self.hexs.append(h2)
        self.hexs.append(h3)

    def addEdges(self, e1, e2, e3):
        self.edges.clear()
        self.edges.append(e1)
        self.edges.append(e2)
        self.edges.append(e3)

    def addAll(self, h1, h2, h3, e1, e2, e3):
        self.hexs.clear()
        self.hexs.append(h1)
        self.hexs.append(h2)
        self.hexs.append(h3)
        self.edges.clear()
        self.edges.append(e1)
        self.edges.append(e2)
        self.edges.append(e3)

    def claimPlace(self, color):
        for edge in self.edges:
            if edge is not None:
                if edge.getOpposite(self) is not None:
                    edge.getOpposite(self).adjacentClaimed()
        self.color = color
        self.available = False

    def adjacentClaimed(self):
        self.available = False


class EdgeNode:
    @staticmethod
    def translate_road(location, origin, radius, sideLength=3):
        toReturnX = 0
        toReturnY = 0
        edgeDist = (radius / 2) * math.sqrt(3)
        cornerDist = radius

        toReturnX = location[0] * (edgeDist / 2)
        l1Plus = location[1] + 1
        toReturnY = (radius / 4) \
                    + (location[1] / 2) * (radius * 1.5)

        ourXOffset = ((sideLength - 1) * 2) * edgeDist
        ourYOffset = edgeDist + ((sideLength - 1.5) * ((radius / 2) * 3))
        totalXOffset = origin[0] - ourXOffset + 12.5
        totalYOffset = origin[1] - ourYOffset + 12.5

        return int(toReturnX + totalXOffset), int(toReturnY + totalYOffset)

    def __init__(self, r=False, c1=None, c2=None):
        self.real = r
        self.hexs = list()
        self.corners = list()
        self.cord1 = c1
        self.cord2 = c2
        self.available = r
        self.color = None

    def addHexs(self, h1, h2):
        self.hexs.clear()
        self.hexs.append(h1)
        self.hexs.append(h2)

    def addCorners(self, c1, c2):
        self.corners.append(c1)
        self.corners.append(c2)

    def addAll(self, h1, h2, c1, c2):
        self.hexs.clear()
        self.hexs.append(h1)
        self.hexs.append(h2)
        self.corners.append(c1)
        self.corners.append(c2)

    def getOpposite(self, baseCorner):
        for corner in self.corners:
            if corner != baseCorner and corner is not None:
                return corner
        else:
            print("Error, not a corner not attached to this edge")

    def claim(self, color):
        self.color = color
        self.available = False


class StructureBoard:
    def linkHexes(self, arrayOfHexes):
        cordToX = 0
        cordToY = 0
        cordToZ = 0
        for i in range(0, self.settleColLength):
            for j in range(0, self.settleRowLength):
                if self.settlements[i][j].real:
                    x = self.settlements[i][j].cord1
                    y = self.settlements[i][j].cord2
                    self.settlements[i][j].hexs.clear()
                    for i in range(0, 3):
                        if ((y % 2 == 0) and (x % 2 == 0)) or ((y % 2 == 1) and (x % 2 == 1)):
                            if i == 2:
                                cordToX = int((x - y - self.settleOffset) / 2) - 1
                            else:
                                cordToX = int((x - y - self.settleOffset) / 2)
                            if i == 0:
                                cordToZ = y - self.settleOffset + 1
                            else:
                                cordToZ = y - self.settleOffset + 2
                            cordToY = 0 - cordToX - cordToZ
                        else:
                            if i == 1:
                                cordToX = int((x - y - self.settleOffset) / 2) + 1
                            else:
                                cordToX = int((x - y - self.settleOffset) / 2)
                            if i == 2:
                                cordToZ = y - self.settleOffset + 2
                            else:
                                cordToZ = y - self.settleOffset + 1
                            cordToY = 0 - cordToX - cordToZ
                        try:
                            self.settlements[i][j].hexs.append(arrayOfHexes[cordToX][cordToY])
                        except IndexError:
                            continue

    def __init__(self, sideLength=3, arrayOfHexes=None):
        # Road Setup
        self.roadRowLength = (sideLength * 4) - 1
        self.roadColLength = (((sideLength * 2) - 1) * 4) + 1
        self.roadOffset = (sideLength * 2) - 2
        self.roads = list()

        for i in range(0, self.roadColLength):
            temp = []
            for j in range(0, self.roadRowLength):
                temp.append(EdgeNode())
            self.roads.append(temp)

        for i in range(0, self.roadColLength):
            for j in range(0, self.roadRowLength):
                # taking care of the corners
                if i > ((self.roadColLength - 1) / 2):
                    newCordi = self.roadColLength - 1 - i
                else:
                    newCordi = i

                if j > ((self.roadRowLength - 1) / 2):
                    newCordj = self.roadRowLength - 1 - j
                else:
                    newCordj = j

                if newCordi + newCordj <= self.roadOffset:
                    continue

                # dealing with even rows
                if (j % 2) == 0:
                    if (i % 2) == 1:
                        self.roads[i][j] = EdgeNode(True, i, j)

                # dealing with odd rows
                elif (j % 2) == 1:
                    if (j % 4) == 1:
                        if (i % 4) == 0:
                            self.roads[i][j] = EdgeNode(True, i, j)
                    elif (j % 4) == 3:
                        if (i % 4) == 2:
                            self.roads[i][j] = EdgeNode(True, i, j)

        # Settlement Setup
        self.settleRowLength = sideLength * 2
        self.settleColLength = (sideLength * 4) - 1
        self.settleOffset = sideLength - 1
        self.settlements = list()

        for i in range(0, self.settleColLength):
            temp = []
            for j in range(0, self.settleRowLength):
                temp.append(CornerNode())
            self.settlements.append(temp)

        for i in range(0, self.settleColLength):
            for j in range(0, self.settleRowLength):
                # taking care of the corners
                if i > ((self.settleColLength - 1) / 2):
                    newCordi = self.settleColLength - 1 - i
                else:
                    newCordi = i

                if j > (self.settleRowLength / 2):
                    newCordj = self.settleRowLength - 1 - j
                else:
                    newCordj = j

                if newCordi + newCordj < self.settleOffset:
                    continue

                self.settlements[i][j] = CornerNode(True, i, j)

        for j in range(0, self.roadRowLength):
            for i in range(0, self.roadColLength):
                if self.roads[i][j].real:
                    if (j % 2) == 0:
                        i1 = int(i / 2)
                        j1 = int(j / 2)
                        i2 = int(i / 2) + 1
                        j2 = int(j / 2)
                    else:
                        i1 = int(i / 2)
                        j1 = int(j / 2)
                        i2 = int(i / 2)
                        j2 = int(j / 2) + 1
                    self.roads[i][j].addCorners(self.settlements[i1][j1], self.settlements[i2][j2])

        for j in range(0, self.settleRowLength):
            for i in range(0, self.settleColLength):
                if self.settlements[i][j].real:
                    if ((i % 2) == 0 and (j % 2) == 0) or ((i % 2) == 1 and (j % 2) == 1):
                        i1 = i * 2 - 1
                        if i1 < 0:
                            i1 = None
                        j1 = j * 2
                        i2 = i * 2 + 1
                        if i2 >= self.roadColLength:
                            i2 = None
                        j2 = j * 2
                        i3 = i * 2
                        j3 = j * 2 + 1
                        if j3 >= self.roadRowLength:
                            j3 = None
                    else:
                        i1 = i * 2 - 1
                        if i1 < 0:
                            i1 = None
                        j1 = j * 2
                        i2 = i * 2 + 1
                        if i2 >= self.roadColLength:
                            i2 = None
                        j2 = j * 2
                        i3 = i * 2
                        j3 = j * 2 - 1
                        if j3 < 0:
                            j3 = None
                    insert1 = None
                    insert2 = None
                    insert3 = None

                    if (i1 is not None) and (j1 is not None):
                        insert1 = self.roads[i1][j1]
                    if (i2 is not None) and (j2 is not None):
                        insert2 = self.roads[i2][j2]
                    if (i3 is not None) and (j3 is not None):
                        insert3 = self.roads[i3][j3]

                    self.settlements[i][j].addEdges(insert1, insert2, insert3)

        self.emptySettlementList = list()
        for i in range(0, self.settleColLength):
            for j in range(0, self.settleRowLength):
                if self.settlements[i][j].real:
                    self.emptySettlementList.append(self.settlements[i][j])

        self.emptyRoadList = list()
        for i in range(0, self.roadColLength):
            for j in range(0, self.roadRowLength):
                if self.roads[i][j].real:
                    self.emptyRoadList.append(self.roads[i][j])
        # self.linkHexes(arrayOfHexes)

    def printAllSettlements(self):
        for j in range(0, self.settleRowLength):
            for i in range(0, self.settleColLength):
                print(int(self.settlements[i][j].available), end=" ")
            print()
        print()

        print(len(self.emptySettlementList))
        print()

    def printAllSettlementsArray(self):
        for j in range(0, self.settleRowLength):
            print('[', end="")
            for i in range(0, self.settleColLength):
                print(int(self.settlements[i][j].available), end=", ")
            print('],')
        print()

        print(len(self.emptySettlementList))
        print()

    def printAllRoads(self):
        for j in range(0, self.roadRowLength):
            for i in range(0, self.roadColLength):
                print(int(self.roads[i][j].available), end=" ")
            print()
        print()

        print(len(self.emptyRoadList))
        print()

    def claimInitialSettlement(self, x, y, color):
        toReturn = None
        print("Claimed " + str(x) + " " + str(y))
        print()
        print("Available Roads")
        toReturn = list()
        for settlement in self.emptySettlementList:
            if settlement.cord1 == x and settlement.cord2 == y:
                i = 0
                for edge in settlement.edges:
                    if edge is not None:
                        if edge.available:
                            print("Road " + str(i) + " " + str(edge.cord1) + " " + str(edge.cord2))
                    i += 1
                print()

        toReturn = self.claimSettlement(x, y, color)
        return toReturn

    def claimSettlement(self, x, y, color):
        toReturn = None
        for settlement in self.emptySettlementList:
            if settlement.cord1 == x and settlement.cord2 == y:
                settlement.claimPlace(color)
                toReturn = settlement

        for settlement in self.emptySettlementList:
            if not settlement.available:
                self.emptySettlementList.remove(settlement)

        for settlement in self.emptySettlementList:
            if not settlement.available:
                self.emptySettlementList.remove(settlement)

        for settlement in self.emptySettlementList:
            if not settlement.available:
                self.emptySettlementList.remove(settlement)

        return toReturn

    # def claimInitialRoad(self, x, y, color):

    def claimRoad(self, x, y, color):
        toReturn = None
        for road in self.emptyRoadList:
            if road.cord1 == x and road.cord2 == y:
                road.claim(color)
                toReturn = road

        for road in self.emptyRoadList:
            if not road.available:
                self.emptyRoadList.remove(road)

        for road in self.emptyRoadList:
            if not road.available:
                self.emptyRoadList.remove(road)

        return toReturn

    # def initilizaeHexes(self, hexArray):


def main():
    roadMap = StructureBoard(3)
    roadMap.printAllSettlements()
    roadMap.claimInitialSettlement(3, 1, "red")
    roadMap.printAllSettlements()
    roadMap.printAllRoads()
    roadMap.claimRoad(7, 2, "red")
    roadMap.printAllRoads()


if __name__ == "__main__":
    main()
