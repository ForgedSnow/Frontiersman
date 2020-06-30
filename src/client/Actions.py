import sys

sys.path.insert(0, '../src')
from gameboard.NodeRoads import *


def buildRoadCheck(actor, free=False):
    hand = actor.resourceHand
    if (free and actor.numRoads > 0):
        return True
    if hand.brick < 1 or hand.lumber < 1 or actor.numRoads == 0:
        return False
    else:
        return True


def buildRoadAvailable(actor, free=False):
    toReturn = list()
    if buildRoadCheck(actor, free):
        for edgeBase in actor.ownedRoads:
            for corner in edgeBase.corners:
                for edge in corner.edges:
                    if edge is not None:
                        if edge.available and edge not in toReturn:
                            toReturn.append(edge)
        return toReturn
    else:
        return toReturn


def buildSettlementCheck(actor):
    hand = actor.resourceHand
    if hand.brick < 1 or hand.lumber < 1 or hand.grain < 1 or hand.wool < 1 or actor.numSettlements == 0:
        return False
    else:
        return True


def buildSettlementAvailable(actor):
    toReturn = list()
    if buildSettlementCheck(actor):
        for edgeBase in actor.ownedRoads:
            for corner in edgeBase.corners:
                if corner.available and corner not in toReturn:
                    toReturn.append(corner)
        return toReturn
    else:
        return toReturn


def buildCityCheck(actor):
    hand = actor.resourceHand
    if hand.grain < 2 or hand.ore < 3:  # or actor.numCities == 0 or actor.numSettlements == 5:
        return False
    else:
        return True


def buildCityAvailable(actor):
    toReturn = list()
    if buildCityCheck(actor):
        for corner in actor.ownedNodes:
            if not corner.city:
                toReturn.append(corner)
        return toReturn
    else:
        return toReturn


def buyDevelopmentCheck(actor):
    hand = actor.resourceHand
    if hand.grain < 1 or hand.ore < 1 or hand.wool < 1:
        return False
    else:
        return True


def buyDevelopment(actor, bank):
    if buyDevelopmentCheck(actor):
        '''
        randomCard = random.uniform(0, bank.totalDevelopments)

        if randomCard - bank.knights < 0:
            bank.knights -= 1
            actor.developmentHand.knights += 1
        else:
            randomCard -= bank.knights

        if randomCard - bank.roadBuildings < 0:
            bank.roadBuildings -= 1
            actor.developmentHand.roadBuildings += 1
        else:
            randomCard -= bank.roadBuildings

        if randomCard - bank.yearOfPlenty < 0:
            bank.yearOfPlenty -= 1
            actor.developmentHand.yearOfPlenty += 1
        else:
            randomCard -= bank.yearOfPlenty

        if randomCard - bank.monopolies < 0:
            bank.monopolies -= 1
            actor.developmentHand.monopolies += 1
        else:
            randomCard -= bank.monopolies

        if randomCard - bank.victoryPoints < 0:
            bank.victoryPoints -= 1
            actor.developmentHand.victoryPoints += 1
        else:
            randomCard -= bank.victoryPoints
        '''
        print("check passed")

    else:
        return None


def trade(offeredCards, requestedCards, playerResources, bankResources):
    pass
