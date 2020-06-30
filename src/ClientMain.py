import queue
import socket
import sys
import threading

'''
from src.gameboard.Board import Board
from src.client.Client import Client
from src.gameboard.NodeRoads import *
from src.gameboard.Board import *
from src.client.Client import *
from src.client.Player import *

'''
sys.path.insert(0, '../src')
from gameboard.Board import Board
from client.Gui import Client
from client import Actions
from gameboard.NodeRoads import *
from gameboard.Board import *
from client.Gui import *
from client.Player import *

sep = '\n'
enemy_list = []


class client:
    @staticmethod
    def get_valid_player_input(query_string):
        while True:
            try:
                innie = int(input(query_string))
            except ValueError:
                print("invalid number of players")
                continue
            if 0 < innie <= 4:
                return innie
            elif innie > 4:
                print("Maximum number of players is 4")
                continue
            elif innie < 0:
                print("number of players cannot be negative")

    @staticmethod
    def read_from_buffer(sock):
        totalMessage = ""
        while sep not in totalMessage:
            totalMessage += sock.recv(1).decode('utf-8')
        return totalMessage[:-1]

    def board_thread(self, board):
        self.client_instance.run(board)

    def __init__(self, host_ip, port_ip, player_name='John'):
        board_update = queue.Queue()
        board_input = queue.Queue()
        board = Board()
        self.client_instance = Client(board_input)
        self.player = None
        ClientSocket = socket.socket()
        xy = ''
        # Color = input('Choose a color: ')
        print('Waiting for connection')
        try:
            ClientSocket.connect((host_ip, int(port_ip)))
        except socket.error as e:
            print(str(e))
        ClientSocket.send(str.encode(player_name + '\n'))
        Color = ''
        while True:
            Response = self.read_from_buffer(ClientSocket)
            # print(Response)
            if Response == 'host':
                num_players = self.get_valid_player_input(
                    "How many players(including you)? ")  # add error checking from pakuri here
                ClientSocket.send(str.encode(str(num_players) + '\n'))
            elif Response == "quit":
                break
            elif Response == 'set':
                # xy=input("x,y: ")
                self.client_instance.set_board_action("initialsettlement")
                coordinates = board_input.get()
                board_input.task_done()
                settle = self.client_instance.building_locations.claimSettlement(int(coordinates.split(',')[0]),
                                                                                 int(coordinates.split(',')[1]), Color)
                self.client_instance.property_list.append(settle)
                self.client_instance.player.acquireNode(settle)
                port=self.client_instance.game_board.xy_give_port((settle.cord1, settle.cord2))
                print(settle.cord1, settle.cord2)
                if port is not None:
                    self.client_instance.player.bankTrading.update(port.resource)
                self.client_instance.set_board_updated(True)
                ClientSocket.send(str.encode(coordinates + '\n'))
                ClientSocket.send(str.encode("enemyu," + self.client_instance.player.getSendToEnemies() + '\n'))
            elif Response == "startroad":
                self.client_instance.set_board_action("initialroad")
                coordinates = board_input.get()
                board_input.task_done()
                # player.add
                road = self.client_instance.building_locations.claimRoad(int(coordinates.split(',')[0]),
                                                                         int(coordinates.split(',')[1]), Color)
                self.client_instance.road_list.append(road)
                self.client_instance.player.acquireRoad(road)
                self.client_instance.set_board_updated(True)
                ClientSocket.send(str.encode(coordinates + '\n'))
                ClientSocket.send(str.encode("enemyu," + self.client_instance.player.getSendToEnemies() + '\n'))
            elif Response.split(',')[0] == "set":
                print("new settlement" + Response.split(',')[1] + Response.split(',')[1])
                self.client_instance.property_list.append(
                    self.client_instance.building_locations.claimSettlement(int(Response.split(',')[1]),
                                                                            int(Response.split(',')[2]),
                                                                            Response.split(',')[3]))
                self.client_instance.set_board_updated(True)
            elif Response.split(',')[0] == "road":
                print("new road")
                print("new settlement" + Response.split(',')[1] + Response.split(',')[1])
                self.client_instance.road_list.append(
                    self.client_instance.building_locations.claimRoad(int(Response.split(',')[1]),
                                                                      int(Response.split(',')[2]),
                                                                      Response.split(',')[3]))
                self.client_instance.set_board_updated(True)
            elif Response.split(',')[0] == "city":
                self.client_instance.building_locations.settlements[int(Response.split(',')[1])][
                    int(Response.split(',')[2])].city = True
                self.client_instance.set_board_updated(True)
            elif Response.split(',')[0] == "color":
                print("hi")
                Color = Response.split(',')[1]
                self.client_instance.set_player(Player(player_name, Color))
                print(Color)
            elif Response.split(',')[0] == "bank":
                arr = [int(x) for x in Response.split(',')[1:]]
                self.client_instance.bank.update(arr)
                self.client_instance.set_board_updated(True)
            elif Response.split('|')[0] == "board":
                print("hello")
                number_list = [int(elem) for elem in Response.split('|')[1].split(',')]
                resource_list = Response.split('|')[2].split(',')
                port_list = Response.split('|')[3].split(',')
                board.generate_land(number_list, resource_list)
                board.generate_ports(port_list)
                self.client_instance.enemy_list = enemy_list
                threading.Thread(target=self.board_thread, args=(board,)).start()
            elif Response == "getstart":
                print("get starting resources")
                self.client_instance.start_resources()
                message = board_input.get()
                board_input.task_done()
                ClientSocket.send(str.encode(message + '\n'))
                ClientSocket.send(str.encode("enemyu," + self.client_instance.player.getSendToEnemies() + '\n'))
                # bank_update = board_input.get()
                # board_input.task_done()
            elif Response.split(',')[0] == "dice":
                roll = [int(x) for x in Response.split(',')[1:]]
                self.client_instance.display_dice(roll)
                self.client_instance.process_dice(sum(roll))
                message = board_input.get()
                board_input.task_done()
                ClientSocket.send(str.encode(message + '\n'))
                ClientSocket.send(str.encode("enemyu," + self.client_instance.player.getSendToEnemies() + '\n'))
            elif Response == "turn" or Response == "robber":
                self.client_instance.player.development_card_played = False
                if (Response == "robber"):
                    self.client_instance.set_board_action("robber", 'turn')
                else:
                    self.client_instance.set_board_action("turn")
                while True:
                    message = board_input.get()
                    if (message.split(',')[0] == "road"):
                        road = self.client_instance.building_locations.claimRoad(int(message.split(',')[1]),
                                                                                 int(message.split(',')[2]), Color)
                        self.client_instance.road_list.append(road)
                        self.client_instance.player.acquireRoad(road)
                        self.client_instance.set_board_updated(True)
                        self.client_instance.pay_cards([1, 0, 1, 0, 0])
                        ClientSocket.send(str.encode(message + ',' + Color + '\n'))
                        ClientSocket.send(str.encode("enemyu," + self.client_instance.player.getSendToEnemies() + '\n'))
                    if (message.split(',')[0] == "robber"):
                        self.client_instance.game_board.set_robber(
                            (int(message.split(',')[1]), int(message.split(',')[2])))
                        self.client_instance.set_board_updated(True)
                        ClientSocket.send(str.encode(message + '\n'))
                    if (message.split(',')[0] == "set"):
                        settle = self.client_instance.building_locations.claimSettlement(int(message.split(',')[1]),
                                                                                         int(message.split(',')[2]),
                                                                                         Color)
                        self.client_instance.property_list.append(settle)
                        self.client_instance.player.acquireNode(settle)
                        port=self.client_instance.game_board.xy_give_port((settle.cord1,settle.cord2))
                        if port is not None:
                            self.client_instance.player.bankTrading.update(port.resource)
                        self.client_instance.set_board_updated(True)
                        self.client_instance.pay_cards([1, 1, 1, 0, 1])
                        ClientSocket.send(str.encode(message + ',' + Color + '\n'))
                        ClientSocket.send(str.encode("enemyu," + self.client_instance.player.getSendToEnemies() + '\n'))
                    if (message == "dev"):
                        ClientSocket.send(str.encode(message + '\n'))
                        card = self.read_from_buffer(ClientSocket)
                        print(card)
                        self.client_instance.get_dev_card(card)
                        self.client_instance.player.developmentHand.add_card(card)
                        if(card=='victoryPoint'):
                            self.client_instance.player.hiddenVictoryPoints+=1
                        self.client_instance.pay_cards([0,1,0,1,1])
                        ClientSocket.send(str.encode("enemyu,"+self.client_instance.player.getSendToEnemies()+ '\n'))  
                    if(message.split(',')[0]=="monopoly"):
                        ClientSocket.send(str.encode(message+ '\n'))
                        ClientSocket.send(str.encode("enemyu,"+self.client_instance.player.getSendToEnemies()+ '\n'))
                    if(message.split(',')[0]=="city"):
                        settle = self.client_instance.building_locations.settlements[int(message.split(',')[1])][int(message.split(',')[2])].city=True
                        self.client_instance.player.acquireCity()
                        self.client_instance.set_board_updated(True)
                        self.client_instance.pay_cards([0, 2, 0, 3, 0])
                        ClientSocket.send(str.encode(message + ',' + '\n'))
                        ClientSocket.send(str.encode("enemyu," + self.client_instance.player.getSendToEnemies() + '\n'))
                    elif (message == "end"):
                        if(self.client_instance.player.victoryPoints+self.client_instance.player.hiddenVictoryPoints>=10):
                            ClientSocket.send(str.encode('winner,'+self.client_instance.player.name+ '\n'))
                        else:
                            ClientSocket.send(str.encode(message + '\n'))
                            ClientSocket.send(str.encode("enemyu," + self.client_instance.player.getSendToEnemies() + '\n'))
                        break
                    elif (message.split(',')[0] == "bank"):
                        ClientSocket.send(str.encode(message + '\n'))
                        ClientSocket.send(str.encode("enemyu," + self.client_instance.player.getSendToEnemies() + '\n'))

                    elif (message == "roadroad"):
                        board_input.task_done()
                        if (len(Actions.buildRoadAvailable(self.client_instance.player, True)) > 0):
                            self.client_instance.set_board_action("roadfree", 'turn')
                            message = board_input.get()
                            board_input.task_done()
                            road = self.client_instance.building_locations.claimRoad(int(message.split(',')[1]),
                                                                                     int(message.split(',')[2]), Color)
                            self.client_instance.road_list.append(road)
                            self.client_instance.player.acquireRoad(road)
                            self.client_instance.set_board_updated(True)
                            ClientSocket.send(str.encode(message + ',' + Color + '\n'))
                            ClientSocket.send(
                                str.encode("enemyu," + self.client_instance.player.getSendToEnemies() + '\n'))
                        if (len(Actions.buildRoadAvailable(self.client_instance.player, True)) > 0):
                            self.client_instance.set_board_action("roadfree", 'turn')
                            message = board_input.get()
                            board_input.task_done()
                            road = self.client_instance.building_locations.claimRoad(int(message.split(',')[1]),
                                                                                     int(message.split(',')[2]), Color)
                            self.client_instance.road_list.append(road)
                            self.client_instance.player.acquireRoad(road)
                            self.client_instance.set_board_updated(True)
                            ClientSocket.send(str.encode(message + ',' + Color + '\n'))
                            ClientSocket.send(
                                str.encode("enemyu," + self.client_instance.player.getSendToEnemies() + '\n'))
                board_input.task_done()

                # while turn:
            elif Response.split(',')[0] == "robber":
                self.client_instance.game_board.set_robber((int(Response.split(',')[1]), int(Response.split(',')[2])))
                self.client_instance.set_board_updated(True)
            elif Response.split(',')[0] == "monopoly":
                self.client_instance.pay_monopoly(Response.split(',')[1])
                self.client_instance.set_board_updated(True)
            elif Response == "notturn":
                self.client_instance.set_board_action("display", 'display')
            elif Response.split(',')[0] == "enemy":
                enemy_list.append(EnemyPlayer(Response.split(',')[1], Response.split(',')[2]))
            elif Response.split(',')[0] == "enemyu":
                arr = Response.split(',')[1:]
                for en in self.client_instance.enemy_list:
                    if en.color == arr[1]:
                        en.updateEnemy(arr)
            elif Response.split(',')[0] == "winner":
                self.client_instance.running=False
                break
            elif Response != "":
                print(Response.split(',')[0])

        # while True:
        # Input = input('Say Something: ')
        # ClientSocket.send(str.encode(Input))
        # Response = ClientSocket.recv(1024)
        # print(Response.decode('utf-8'))
        # roadMap.printAllSettlements()
        # roadMap.printAllRoads()
        self.client_instance.quit()
        ClientSocket.close()


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 1233
    xy = ''
    #Name = input('Enter your name: ')
    #1Name=sys.argv[1]
    Name = "Name"
    test = client(host, port, Name)
