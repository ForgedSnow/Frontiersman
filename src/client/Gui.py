import ctypes;

ctypes.windll.user32.SetProcessDPIAware()
import os
import random
import sys

import pygame
import pygame.gfxdraw
import pygame_gui as pg_g

'''
from src.client import ClientHelper
from src.client.Bank import Bank
from src.gameboard.NodeRoads import CornerNode, EdgeNode, StructureBoard
from src.gameboard.SettlementButtons import CircleButton
from src.client import Actions

'''
sys.path.insert(0, '../src')
from gameboard.NodeRoads import *
from gameboard.SettlementButtons import *
from gameboard.Tile import *
from client.Bank import *
from client.Player import *
from client import ClientHelper
from client import Actions
from client.CardPickerGui import CardPickerGui
from client.TraderGui import TradeGui
from gameboard.Board import *
from client.GuiConstants import CARD_SIZE, SPACING
'''
os.environ['SDL_AUDIODRIVER'] = 'dsp'
os.putenv("DISPLAY", "localhost:0")
os.environ['SDL_VIDEODRIVER'] = 'x11'
'''
# todo move some of these to GuiConstants.py
RESOLUTION = (1920, 1080)
FRAME_RATE = 60
ACTION_SIZE = (70, 98)
SCALE = 5 / 16
HEX_SIZE = 600 * SCALE
WINDOW_CENTER = (RESOLUTION[0] / 2, RESOLUTION[1] / 2)
COLORS = {
    'red': (127, 0, 0),
    'cyan': (0, 255, 255),
    'orange': (255, 106, 0),
    'blue': (0, 38, 255),
    'green': (0, 153, 15),
    'pink': (255, 0, 110),
    'yellow': (255, 216, 0)
}
CARD_IMAGES = ClientHelper.texture_scale.scale_cards(CARD_SIZE)
ClientHelper.button_resources.save_scaled_cards(CARD_IMAGES)
PORT_TEXTURES = ClientHelper.texture_scale.scale_port_tiles(HEX_SIZE)
TILE_TEXTURES = ClientHelper.texture_scale.scale_resource_tiles(HEX_SIZE)
ROAD_POINTS = ClientHelper.road_hardware_art.generate_road_polygons(HEX_SIZE / 4, 1 / 15)
INFO_WIDTH = 320
BANK_HEIGHT = 100
BANK_CARD_WIDTH = (INFO_WIDTH - 8 * SPACING - BANK_HEIGHT) / 6
BANK_HALF_HEIGHT = (BANK_HEIGHT - 3 * SPACING) / 2
PLAYER_HEIGHT = 150
PLAYER_SECTION_WIDTH = (INFO_WIDTH - 4 * SPACING) / 5
PLAYER_QUARTER_HEIGHT = (PLAYER_HEIGHT - 2 * SPACING) / 4


class Client:
    # for mapping hexagon tiles to x,y
    @staticmethod
    def translate_hex_to_xy(location, origin, radius):
        if location == (0, 0, 0):
            return origin
        x_off = 0
        y_off = 3 / 2 * radius * location[2]
        x_constant = .5 * radius * (3 ** 0.5)
        x_factor = location[0] - location[1]
        x_off = x_factor * x_constant

        return int(origin[0] + x_off), int(origin[1] + y_off)

    @staticmethod
    def quit():
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    @staticmethod
    def add_event(event):
        pygame.event.post(event)

    def __init__(self, board_input):
        self.board_input = board_input
        self.board_action = "display"
        self.last_board_action = "display"
        self.board_updated = False
        self.board_input = board_input
        self.settlementButtons = []
        self.property_list = []
        self.road_list = []
        self.manual_card_list = []
        self.card_hand = []
        self.bank = Bank()
        self.running = False
        self.is_rolling = False

        # todo initialize the rest of these
        self.card_keys = []
        self.cards_updated = False
        self.card_element_list = []
        self.player_element_list = []
        self.dice_image = None
        self.dice_button = None
        self.player = None
        self.enemy_list = []
        self.game_board = None
        self.building_locations = None
        self.font = None
        self.manager = None
        self.clock = None
        self.house_points = None
        self.object_textures = None
        self.board_center = None
        self.resource_hexes = None
        self.port_hexes = None
        self.game_window = None
        self.action_panel = None
        self.grid_size = None
        self.set_butts = None
        self.card_panel = None
        self.info_panel = None
        self.road_butts = None
        self.trade_button = None
        self.road_button = None
        self.settlement_button = None
        self.city_button = None
        self.development_button = None
        self.end_turn_button = None
        self.bank_panel = None
        self.bank_logo = None
        self.wood_logo = None
        self.wood_bank = None
        self.brick_logo = None
        self.brick_bank = None
        self.sheep_logo = None
        self.sheep_bank = None
        self.wheat_logo = None
        self.wheat_bank = None
        self.ore_logo = None
        self.ore_bank = None
        self.dev_logo = None
        self.dev_bank = None
        self.card_picker = None
        self.card_trader = None

        # constants translated to the previously used instance variables
        self.hex_size = HEX_SIZE
        self.port_textures = PORT_TEXTURES
        self.texture_dictionary = TILE_TEXTURES
        self.scale = SCALE
        self.card_images = CARD_IMAGES
        self.road_points = ROAD_POINTS

    def set_player(self, player):
        self.player = player

    def board_setup_coordinates_display(self, data):
        print(data)
        self.board_input.put(','.join(data))
        self.board_action = self.last_board_action

    def initial_settlement_buttons(self):
        settlement_buttons = []
        for j in range(0, self.building_locations.settleRowLength):
            for i in range(0, self.building_locations.settleColLength):
                if self.building_locations.settlements[i][j].available:
                    settlement_buttons.append(
                        CircleButton((125, 125, 255), (255, 255, 255), (40, 40),
                                     CornerNode.translate_settlement((i, j), self.board_center, int(self.hex_size / 2)),
                                     "center", self.board_setup_coordinates_display,
                                     [str(i), str(j)]))
        return settlement_buttons

    def initial_road_buttons(self, prop):
        road_buttons = []
        for edge in prop.edges:
            if edge is not None:
                if edge.real:
                    road_buttons.append(
                        CircleButton((125, 125, 255), (255, 255, 255), (40, 40),
                                     EdgeNode.translate_road((edge.cord1, edge.cord2), self.board_center,
                                                             int(self.hex_size / 2)), "center",
                                     self.board_setup_coordinates_display,
                                     [str(edge.cord1), str(edge.cord2)]))
        return road_buttons

    def get_settlement_buttons(self):
        settlement_buttons = []
        list_o_setts = Actions.buildSettlementAvailable(self.player)
        for settle in list_o_setts:
            settlement_buttons.append(
                CircleButton((125, 125, 255), (255, 255, 255), (40, 40),
                             CornerNode.translate_settlement((settle.cord1, settle.cord2), self.board_center,
                                                             int(self.hex_size / 2)),
                             "center", self.board_setup_coordinates_display,
                             ["set", str(settle.cord1), str(settle.cord2)]))
        return settlement_buttons

    def get_city_buttons(self):
        settlement_buttons = []
        list_o_setts = Actions.buildCityAvailable(self.player)
        for settle in list_o_setts:
            settlement_buttons.append(
                CircleButton((125, 125, 255), (255, 255, 255), (40, 40),
                             CornerNode.translate_settlement((settle.cord1, settle.cord2), self.board_center,
                                                             int(self.hex_size / 2)),
                             "center", self.board_setup_coordinates_display,
                             ["city", str(settle.cord1), str(settle.cord2)]))
        return settlement_buttons

    def get_road_buttons(self, free=False):
        road_buttons = []
        list_o_roads = Actions.buildRoadAvailable(self.player, free)
        for edge in list_o_roads:
            road_buttons.append(
                CircleButton((125, 125, 255), (255, 255, 255), (40, 40),
                             EdgeNode.translate_road((edge.cord1, edge.cord2), self.board_center,
                                                     int(self.hex_size / 2)), "center",
                             self.board_setup_coordinates_display,
                             ["road", str(edge.cord1), str(edge.cord2)]))
        return road_buttons

    def get_robber_buttons(self):
        road_buttons = []
        for tile in self.resource_hexes:
            if (not tile.get_robber()):
                loc = self.translate_hex_to_xy(tile.location, self.board_center, int(self.hex_size / 2))
                (loc[0] + int(self.hex_size / 3), loc[1] + int(self.hex_size / 3))
                road_buttons.append(
                    CircleButton((125, 125, 255), (255, 255, 255), (40, 40),
                                 (loc[0] + int(self.hex_size / 3), loc[1] + int(self.hex_size / 3)), "center",
                                 self.board_setup_coordinates_display,
                                 ["robber", str(tile.location[0]), str(tile.location[1])]))
        return road_buttons

    def set_cards(self, card_keys):
        self.card_keys = card_keys
        self.cards_updated = True

    def update_cards(self):
        for card in self.card_element_list:
            card.kill()

        self.card_element_list = []
        if len(self.card_keys) > 0:
            area_width = self.card_panel.relative_rect.width - CARD_SIZE[0] - 8
            if len(self.card_keys) == 1:
                offset = 0
            else:
                offset = min(area_width / (len(self.card_keys) - 1), CARD_SIZE[0] + SPACING)

            start = (area_width - offset * (len(self.card_keys) - 1)) / 2
            self.card_keys.sort()
            for i, key in enumerate(self.card_keys):
                self.card_element_list.append(pg_g.elements.UIButton(
                    relative_rect=pygame.Rect((start + i * offset, 0), CARD_SIZE),
                    text="",
                    manager=self.manager,
                    container=self.card_panel,
                    object_id='#' + key,
                ))

    # todo figure out how to make scrollable
    def set_player_info(self, curr_player, enemy_players):
        for panel in self.player_element_list:
            panel.kill()

        self.player_element_list = []

        curr_player_info = pg_g.elements.UIPanel(
            relative_rect=pygame.Rect(0, self.bank_panel.relative_rect.bottom + SPACING, INFO_WIDTH - 2 * SPACING,
                                      PLAYER_HEIGHT + SPACING),
            container=self.info_panel,
            starting_layer_height=1,
            manager=self.manager
        )
        name = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(SPACING, SPACING, PLAYER_SECTION_WIDTH * 2 + SPACING, PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text=curr_player.name,
            manager=self.manager,
        )
        hand_logo = pg_g.elements.UITextBox(  # todo replace with logo
            relative_rect=pygame.Rect(name.relative_rect.left, name.relative_rect.bottom, PLAYER_SECTION_WIDTH,
                                      2 * PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text="Cs",
            manager=self.manager,
        )
        hand_value = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(hand_logo.relative_rect.left, hand_logo.relative_rect.bottom,
                                      PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text=str(curr_player.resourceHand.totalResources),
            manager=self.manager,
        )
        dev_logo = pg_g.elements.UITextBox(  # todo replace with logo
            relative_rect=pygame.Rect(hand_logo.relative_rect.right, name.relative_rect.bottom, PLAYER_SECTION_WIDTH,
                                      2 * PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text="Ds",
            manager=self.manager,
        )
        dev_value = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(dev_logo.relative_rect.left, dev_logo.relative_rect.bottom, PLAYER_SECTION_WIDTH,
                                      PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text=str(curr_player.developmentHand.totalDevelopments),
            manager=self.manager,
        )

        vp_logo = pg_g.elements.UITextBox(  # todo replace with logo
            relative_rect=pygame.Rect(name.relative_rect.right, name.relative_rect.top, PLAYER_SECTION_WIDTH,
                                      PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text="VP",
            manager=self.manager,
        )
        if curr_player.hiddenVictoryPoints!=0:
            vp_value = pg_g.elements.UITextBox(
                relative_rect=pygame.Rect(vp_logo.relative_rect.left, vp_logo.relative_rect.bottom, PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
                container=curr_player_info,
                html_text=str(curr_player.victoryPoints)+'('+ str(curr_player.victoryPoints+curr_player.hiddenVictoryPoints)+')',
                manager=self.manager,
            )
        else:
            vp_value = pg_g.elements.UITextBox(
                relative_rect=pygame.Rect(vp_logo.relative_rect.left, vp_logo.relative_rect.bottom, PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
                container=curr_player_info,
                html_text=str(curr_player.victoryPoints),
                manager=self.manager,
            )

        roads_logo = pg_g.elements.UITextBox(  # todo replace with logo
            relative_rect=pygame.Rect(vp_value.relative_rect.left, vp_value.relative_rect.bottom, PLAYER_SECTION_WIDTH,
                                      PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text="Rs",
            manager=self.manager,
        )
        roads_value = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(roads_logo.relative_rect.left, roads_logo.relative_rect.bottom,
                                      PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text=str(curr_player.numRoads),
            manager=self.manager,
        )

        settlements_logo = pg_g.elements.UITextBox(  # todo replace with logo
            relative_rect=pygame.Rect(vp_logo.relative_rect.right, vp_logo.relative_rect.top, PLAYER_SECTION_WIDTH,
                                      PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text="Ss",
            manager=self.manager,
        )
        settlements_value = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(settlements_logo.relative_rect.left, settlements_logo.relative_rect.bottom,
                                      PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text=str(curr_player.numSettlements),
            manager=self.manager,
        )
        cities_logo = pg_g.elements.UITextBox(  # todo replace with logo
            relative_rect=pygame.Rect(settlements_value.relative_rect.left, settlements_value.relative_rect.bottom,
                                      PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text="Cs",
            manager=self.manager,
        )
        cities_value = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(cities_logo.relative_rect.left, cities_logo.relative_rect.bottom,
                                      PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text=str(curr_player.numCities),
            manager=self.manager,
        )

        longest_road_logo = pg_g.elements.UITextBox(  # todo replace with logo
            relative_rect=pygame.Rect(settlements_logo.relative_rect.right, settlements_logo.relative_rect.top,
                                      PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text="LR",
            manager=self.manager,
        )
        longest_road_value = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(longest_road_logo.relative_rect.left, longest_road_logo.relative_rect.bottom,
                                      PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text=str(curr_player.longestRoad),
            manager=self.manager,
        )
        largest_army_logo = pg_g.elements.UITextBox(  # todo replace with logo
            relative_rect=pygame.Rect(longest_road_value.relative_rect.left, longest_road_value.relative_rect.bottom,
                                      PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text="LA",
            manager=self.manager,
        )
        largest_army_value = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(largest_army_logo.relative_rect.left, largest_army_logo.relative_rect.bottom,
                                      PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
            container=curr_player_info,
            html_text=str(curr_player.largestArmy),
            manager=self.manager,
        )

        self.player_element_list.append(curr_player_info)

        for enemy_player in enemy_players:
            enemy_player_info = pg_g.elements.UIPanel(
                relative_rect=pygame.Rect(0, self.player_element_list[-1].relative_rect.bottom + SPACING,
                                          INFO_WIDTH - 2 * SPACING, PLAYER_HEIGHT + SPACING),
                container=self.info_panel,
                starting_layer_height=1,
                manager=self.manager
            )
            name = pg_g.elements.UITextBox(
                relative_rect=pygame.Rect(SPACING, SPACING, PLAYER_SECTION_WIDTH * 2 + SPACING, PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text=enemy_player.name,
                manager=self.manager,
            )

            hand_logo = pg_g.elements.UITextBox(  # todo replace with logo
                relative_rect=pygame.Rect(name.relative_rect.left, name.relative_rect.bottom, PLAYER_SECTION_WIDTH,
                                          2 * PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text="Cs",
                manager=self.manager,
            )
            hand_value = pg_g.elements.UITextBox(
                relative_rect=pygame.Rect(hand_logo.relative_rect.left, hand_logo.relative_rect.bottom,
                                          PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text=str(enemy_player.handSize),
                manager=self.manager,
            )
            dev_logo = pg_g.elements.UITextBox(  # todo replace with logo
                relative_rect=pygame.Rect(hand_logo.relative_rect.right, name.relative_rect.bottom,
                                          PLAYER_SECTION_WIDTH, 2 * PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text="Ds",
                manager=self.manager,
            )
            dev_value = pg_g.elements.UITextBox(
                relative_rect=pygame.Rect(dev_logo.relative_rect.left, dev_logo.relative_rect.bottom,
                                          PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text=str(enemy_player.developmentSize),
                manager=self.manager,
            )

            vp_logo = pg_g.elements.UITextBox(  # todo replace with logo
                relative_rect=pygame.Rect(name.relative_rect.right, name.relative_rect.top, PLAYER_SECTION_WIDTH,
                                          PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text="VP",
                manager=self.manager,
            )
            vp_value = pg_g.elements.UITextBox(
                relative_rect=pygame.Rect(vp_logo.relative_rect.left, vp_logo.relative_rect.bottom,
                                          PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text=str(enemy_player.visibleVictoryPoints),
                manager=self.manager,
            )

            roads_logo = pg_g.elements.UITextBox(  # todo replace with logo
                relative_rect=pygame.Rect(vp_value.relative_rect.left, vp_value.relative_rect.bottom,
                                          PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text="Rs",
                manager=self.manager,
            )
            roads_value = pg_g.elements.UITextBox(
                relative_rect=pygame.Rect(roads_logo.relative_rect.left, roads_logo.relative_rect.bottom,
                                          PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text=str(enemy_player.numRoads),
                manager=self.manager,
            )

            settlements_logo = pg_g.elements.UITextBox(  # todo replace with logo
                relative_rect=pygame.Rect(vp_logo.relative_rect.right, vp_logo.relative_rect.top, PLAYER_SECTION_WIDTH,
                                          PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text="Ss",
                manager=self.manager,
            )
            settlements_value = pg_g.elements.UITextBox(
                relative_rect=pygame.Rect(settlements_logo.relative_rect.left, settlements_logo.relative_rect.bottom,
                                          PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text=str(enemy_player.numSettlements),
                manager=self.manager,
            )
            cities_logo = pg_g.elements.UITextBox(  # todo replace with logo
                relative_rect=pygame.Rect(settlements_value.relative_rect.left, settlements_value.relative_rect.bottom,
                                          PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text="Cs",
                manager=self.manager,
            )
            cities_value = pg_g.elements.UITextBox(
                relative_rect=pygame.Rect(cities_logo.relative_rect.left, cities_logo.relative_rect.bottom,
                                          PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text=str(enemy_player.numCities),
                manager=self.manager,
            )

            longest_road_logo = pg_g.elements.UITextBox(  # todo replace with logo
                relative_rect=pygame.Rect(settlements_logo.relative_rect.right, settlements_logo.relative_rect.top,
                                          PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text="LR",
                manager=self.manager,
            )
            longest_road_value = pg_g.elements.UITextBox(
                relative_rect=pygame.Rect(longest_road_logo.relative_rect.left, longest_road_logo.relative_rect.bottom,
                                          PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text=str(enemy_player.longestRoad),
                manager=self.manager,
            )
            largest_army_logo = pg_g.elements.UITextBox(  # todo replace with logo
                relative_rect=pygame.Rect(longest_road_value.relative_rect.left,
                                          longest_road_value.relative_rect.bottom, PLAYER_SECTION_WIDTH,
                                          PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text="LA",
                manager=self.manager,
            )
            largest_army_value = pg_g.elements.UITextBox(
                relative_rect=pygame.Rect(largest_army_logo.relative_rect.left, largest_army_logo.relative_rect.bottom,
                                          PLAYER_SECTION_WIDTH, PLAYER_QUARTER_HEIGHT),
                container=enemy_player_info,
                html_text=str(enemy_player.largestArmy),
                manager=self.manager,
            )

            self.player_element_list.append(enemy_player_info)

    @staticmethod
    def translate_from_3d_tile(coordinates):
        center = [5, 2.5]
        y = coordinates[2]
        x = coordinates[0] - coordinates[1]
        array = [[center[0] + x, int(center[1] + y + .5)], [center[0] + x - 1, int(center[1] + y + .5)],
                 [center[0] + x + 1, int(center[1] + y + .5)], [center[0] + x, int(center[1] + y - .5)],
                 [center[0] + x - 1, int(center[1] + y - .5)], [center[0] + x + 1, int(center[1] + y - .5)]]
        return array

    @staticmethod
    def translate_from_2d_tile(coordinates):
        center = [5, 2.5]
        y = 1 - coordinates[0] - coordinates[1]
        x = coordinates[0] - coordinates[1]
        array = [[center[0] + x, int(center[1] + y + .5)], [center[0] + x - 1, int(center[1] + y + .5)],
                 [center[0] + x + 1, int(center[1] + y + .5)], [center[0] + x, int(center[1] + y - .5)],
                 [center[0] + x - 1, int(center[1] + y - .5)], [center[0] + x + 1, int(center[1] + y - .5)]]
        return array

    @staticmethod
    def get_tiles_from_vertex(coordinates):
        x = coordinates[0]
        y = coordinates[1]

        tile_array = []

        location_list = [
            [0, 2, -2],
            [1, 1, -2],
            [2, 0, -2],
            [-1, 2, -1],
            [0, 1, -1],
            [1, 0, -1],
            [2, -1, -1],
            [-2, 2, 0],
            [-1, 1, 0],
            [0, 0, 0],
            [1, -1, 0],
            [2, -2, 0],
            [-2, 1, 1],
            [-1, 0, 1],
            [0, -1, 1],
            [1, -2, 1],
            [-2, 0, 2],
            [-1, -1, 2],
            [0, -2, 2]
        ]    
        translate_list = []
        for tile in location_list:
            for point in Client.translate_from_3d_tile(tile):
                if point == [x, y]:
                    tile_array.append(tile)

        return tile_array

    def process_dice(self, roll):
        cards_to_get = []
        if roll == 7:
            print('discard cards')  # todo do discard here
        else:
            for prop in self.player.ownedNodes:
                for tile_coordinate in Client.get_tiles_from_vertex([prop.cord1, prop.cord2]):
                    tile = self.game_board.get_tile(tile_coordinate)
                    if tile.number == roll and not tile.get_robber():
                        if prop.city:
                            cards_to_get.append(tile.get_resource())
                            cards_to_get.append(tile.get_resource())
                        else:
                            cards_to_get.append(tile.get_resource())
        self.get_cards(cards_to_get)

    def pay_cards(self, res):
        for r in range(0, res[0]):
            self.card_hand.remove('Brick')
        for r in range(0, res[1]):
            self.card_hand.remove('Wheat')
        for r in range(0, res[2]):
            self.card_hand.remove('Wood')
        for r in range(0, res[3]):
            self.card_hand.remove('Ore')
        for r in range(0, res[4]):
            self.card_hand.remove('Sheep')
        self.set_cards(self.card_hand)
        self.bank.update(res)
        array2 = [0 - x for x in res]
        self.player.addResources(array2)
        self.set_board_updated(True)
        self.board_input.put('bank,' + ','.join([str(x) for x in array2]))
    def trade_cards(self, trade, get):
        array1 = [0, 0, 0, 0, 0]
        for r in trade:
            if r == 'Brick':
                array1[0] -= 1
                self.card_hand.remove('Brick')
            elif r == 'Wheat':
                array1[1] -= 1
                self.card_hand.remove('Wheat')
            elif r == 'Wood':
                array1[2] -= 1
                self.card_hand.remove('Wood')
            elif r == 'Ore':
                array1[3] -= 1
                self.card_hand.remove('Ore')
            elif r == 'Sheep':
                array1[4] -= 1
                self.card_hand.remove('Sheep')
        for r in get:
            if r == 'Brick':
                array1[0] += 1
                self.card_hand.append('Brick')
            elif r == 'Wheat':
                array1[1] += 1
                self.card_hand.append('Wheat')
            elif r == 'Wood':
                array1[2] += 1
                self.card_hand.append('Wood')
            elif r == 'Ore':
                array1[3] += 1
                self.card_hand.append('Ore')
            elif r == 'Sheep':
                array1[4] += 1
                self.card_hand.append('Sheep')
        self.set_cards(self.card_hand)
        self.player.addResources(array1)
        array2 = [0 - x for x in array1]
        self.bank.update(array2)
        self.set_board_updated(True)
        self.board_input.put('bank,' + ','.join([str(x) for x in array2]))

    def get_dev_card(self, card):
        self.bank.get_dev_card()
        self.player.developmentHand.add_card(card)
        self.card_hand.append(card)
        self.set_cards(self.card_hand)
        self.set_board_updated(True)

    def get_cards(self, res):
        array1 = [0, 0, 0, 0, 0]
        for r in res:
            if r == 'Brick':
                array1[0] += 1
            elif r == 'Wheat':
                array1[1] += 1
            elif r == 'Wood':
                array1[2] += 1
            elif r == 'Ore':
                array1[3] += 1
            elif r == 'Sheep':
                array1[4] += 1
        self.card_hand += res
        self.set_cards(self.card_hand)
        self.player.addResources(array1)
        array2 = [0 - x for x in array1]
        self.bank.update(array2)
        self.set_board_updated(True)
        self.board_input.put('bank,' + ','.join([str(x) for x in array2]))
    def get_monopoly(self, r):
        res=[]
        array1 = [0, 0, 0, 0, 0]
        if r == 'Brick':
            for x in range(0,19-self.bank.brick-self.player.resourceHand.brick):
                res.append(r)
                array1[0]+=1
        elif r == 'Wheat':
            for x in range(0,19-self.bank.grain-self.player.resourceHand.grain):
                res.append(r)
                array1[1] += 1
        elif r == 'Wood':
            for x in range(0,19-self.bank.lumber-self.player.resourceHand.lumber):
                res.append(r)
                array1[2] += 1
        elif r == 'Ore':
            for x in range(0,19-self.bank.ore-self.player.resourceHand.ore):
                res.append(r)
                array1[3] += 1
        elif r == 'Sheep':
            for x in range(0,19-self.bank.sheep-self.player.resourceHand.wool):
                res.append(r)
                array1[4] += 1
        self.card_hand += res
        self.set_cards(self.card_hand)
        self.player.addResources(array1)
        self.set_board_updated(True)
        self.board_input.put('monopoly,' + r)
    def pay_monopoly(self, r):
        res=[]
        array1 = [0, 0, 0, 0, 0]
        if r == 'Brick':
            for x in range(0,self.player.resourceHand.brick):
                self.card_hand.remove(r)
                array1[0]-=1
        elif r == 'Wheat':
            for x in range(0,self.player.resourceHand.grain):
                self.card_hand.remove(r)
                self.card_hand.remove(r)
                array1[1] -= 1
        elif r == 'Wood':
            for x in range(0,self.player.resourceHand.lumber):
                self.card_hand.remove(r)  
                array1[2] -= 1
        elif r == 'Ore':
            for x in range(0,self.player.resourceHand.ore):
                self.card_hand.remove(r)
                array1[3] -= 1
        elif r == 'Sheep':
            for x in range(0,self.player.resourceHand.wool):
                self.card_hand.remove(r)
                array1[4] -= 1
        self.set_cards(self.card_hand)
        self.player.addResources(array1)
        self.set_board_updated(True)
    def start_resources(self):
        last = self.player.ownedNodes[-1]
        array = Client.get_tiles_from_vertex([last.cord1, last.cord2])
        res = []
        for h in array:
            if self.game_board.get_tile(h).get_resource() != 'Desert':
                res.append(self.game_board.get_tile(h).get_resource())
        self.get_cards(res)

    def set_board_action(self, bool1, last_action=None):
        if (self.board_action != bool1):
            self.board_updated = True
        if last_action == None:
            self.last_board_action = self.board_action
        else:
            self.last_board_action = last_action
        self.board_action = bool1

    def set_board_updated(self, bool1):
        self.board_updated = bool1

    def render_dice(self, rolls):
        size = 80
        width = len(rolls) * (2 * SPACING + size) - 2 * SPACING
        height = size

        dice_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        dice_surface.fill((0, 0, 0, 0))

        for i, roll in enumerate(rolls):
            x = i * (2 * SPACING + size) - 2 * SPACING
            y = 0
            pygame.draw.rect(dice_surface, (255, 255, 255), pygame.Rect(x, y, size, size))
            text_surface = self.font.render(str(roll), True, (0, 0, 0))
            dice_surface.blit(text_surface,
                              (x + (size - text_surface.get_width()) / 2, y + (size - text_surface.get_height()) / 2))

        return dice_surface

    def display_dice(self, rolls):
        if self.dice_image:
            self.dice_image.kill()

        dice_render = self.render_dice(rolls)
        dice_rect = pygame.Rect(self.info_panel.relative_rect.left - dice_render.get_width() - SPACING,
                                self.action_panel.relative_rect.top - dice_render.get_height() - SPACING,
                                dice_render.get_width(),
                                dice_render.get_height())

        if self.dice_button is None:
            self.dice_button = pg_g.elements.UIButton(
                relative_rect=dice_rect,
                manager=self.manager,
                text="",
                anchors={'left': 'right',
                         'right': 'right',
                         'top': 'bottom',
                         'bottom': 'bottom'},
            )

        self.dice_image = pg_g.elements.UIImage(
            relative_rect=dice_rect,
            manager=self.manager,
            image_surface=dice_render,
            anchors={'left': 'right',
                     'right': 'right',
                     'top': 'bottom',
                     'bottom': 'bottom'}
        )

    def initialize_gui(self):
        pygame.init()
        pygame.display.set_caption('Client')

        font_size = 45
        self.font = pygame.font.SysFont('Comic Sans MS', font_size)

        self.game_window = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
        # self.game_window = pygame.display.set_mode(RESOLUTION)

        self.manager = pg_g.UIManager(RESOLUTION, 'themes/card_theme.json')
        self.clock = pygame.time.Clock()

        # creates settlement polygon
        house_width = 120 * self.scale / 2
        house_height = -135 * self.scale / 2
        self.house_points = [
            [-house_width, -house_height],
            [-house_width, 0],
            [0, house_height],
            [house_width, 0],
            [house_width, -house_height]
        ]

        # creates city polygon
        city_width = 120 * self.scale / 2
        city_height = -120 * self.scale / 2
        difference = -5

        self.city_points = [
            [-city_width, city_height],
            [-city_width / 2, city_height * 5 / 4],
            [0, city_height],
            [0, 0 + difference],
            [city_width, 0 + difference],
            [city_width, -city_height],
            [-city_width, -city_height]
        ]

        base_path = os.path.dirname(__file__)

        self.object_textures = {
            'Board': pygame.image.load(os.path.join(base_path, '../assets/gameboard_grid_v4.png'))
        }

        self.board_center = (
            RESOLUTION[0] / 2 - int(self.hex_size / 2), RESOLUTION[1] / 2 - int(self.hex_size / 2) - CARD_SIZE[1] / 2)

        self.resource_hexes = self.game_board.land_list
        self.port_hexes = self.game_board.port_list

        # game grid
        self.object_textures['Board'] = pygame.transform.scale(self.object_textures.get('Board'),
                                                               (int(3600 * self.scale), int(3600 * self.scale)))
        self.grid_size = self.object_textures.get('Board').get_size()
        self.set_butts = self.initial_settlement_buttons()
        self.road_butts = []

        action_panel_layout = pygame.Rect(0, 0, 6 * ACTION_SIZE[0] + 7 * SPACING, ACTION_SIZE[1] + 2 * SPACING)
        action_panel_layout.bottomright = (-SPACING, -SPACING)
        self.action_panel = pg_g.elements.UIPanel(relative_rect=action_panel_layout,
                                                  starting_layer_height=1,
                                                  manager=self.manager,
                                                  anchors={'left': 'right',
                                                           'right': 'right',
                                                           'top': 'bottom',
                                                           'bottom': 'bottom'}
                                                  )

        self.trade_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((0 * ACTION_SIZE[0] + 0 * SPACING, 0), ACTION_SIZE),
            container=self.action_panel,
            manager=self.manager,
            text="TRADE")

        self.road_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((1 * ACTION_SIZE[0] + 1 * SPACING, 0), ACTION_SIZE),
            container=self.action_panel,
            manager=self.manager,
            text="ROAD")

        self.settlement_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((2 * ACTION_SIZE[0] + 2 * SPACING, 0), ACTION_SIZE),
            container=self.action_panel,
            manager=self.manager,
            text="SETTLE")

        self.city_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((3 * ACTION_SIZE[0] + 3 * SPACING, 0), ACTION_SIZE),
            container=self.action_panel,
            manager=self.manager,
            text="CITY")

        self.development_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((4 * ACTION_SIZE[0] + 4 * SPACING, 0), ACTION_SIZE),
            container=self.action_panel,
            manager=self.manager,
            text="DEV CARD")

        self.end_turn_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((5 * ACTION_SIZE[0] + 5 * SPACING, 0), ACTION_SIZE),
            container=self.action_panel,
            manager=self.manager,
            text="END",
        )

        card_panel_layout = pygame.Rect(0, 0, RESOLUTION[0] - action_panel_layout.width - 2 * SPACING,
                                        CARD_SIZE[1] + 2 * SPACING)
        card_panel_layout.bottomleft = (SPACING, -SPACING)
        self.card_panel = pg_g.elements.UIPanel(relative_rect=card_panel_layout,
                                                starting_layer_height=1,
                                                manager=self.manager,
                                                anchors={'left': 'left',
                                                         'right': 'right',
                                                         'top': 'bottom',
                                                         'bottom': 'bottom'}
                                                )

        info_panel_layout = pygame.Rect(0, 0, INFO_WIDTH, RESOLUTION[1] - action_panel_layout.height - 2 * SPACING)
        info_panel_layout.topright = (-SPACING, SPACING)
        self.info_panel = pg_g.elements.UIPanel(relative_rect=info_panel_layout,
                                                starting_layer_height=1,
                                                manager=self.manager,
                                                anchors={'left': 'right',
                                                         'right': 'right',
                                                         'top': 'top',
                                                         'bottom': 'top'}
                                                )

        self.bank_panel = pg_g.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, INFO_WIDTH - 2 * SPACING, BANK_HEIGHT + SPACING),
            container=self.info_panel,
            starting_layer_height=1,
            manager=self.manager)

        self.bank_logo = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(SPACING, SPACING, BANK_HEIGHT - 2 * SPACING, BANK_HEIGHT - 2 * SPACING),
            container=self.bank_panel,
            manager=self.manager,
            html_text="Bank"
            )

        self.wood_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(self.bank_logo.relative_rect.right + SPACING, SPACING, BANK_CARD_WIDTH,
                                      BANK_HALF_HEIGHT),
            image_surface=self.card_images["Wood"],
            manager=self.manager,
            container=self.bank_panel)

        self.brick_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(self.wood_logo.relative_rect.right + SPACING, SPACING, BANK_CARD_WIDTH,
                                      BANK_HALF_HEIGHT),
            image_surface=self.card_images["Brick"],
            manager=self.manager,
            container=self.bank_panel)

        self.sheep_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(self.brick_logo.relative_rect.right + SPACING, SPACING, BANK_CARD_WIDTH,
                                      BANK_HALF_HEIGHT),
            image_surface=self.card_images["Sheep"],
            manager=self.manager,
            container=self.bank_panel)

        self.wheat_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(self.sheep_logo.relative_rect.right + SPACING, SPACING, BANK_CARD_WIDTH,
                                      BANK_HALF_HEIGHT),
            image_surface=self.card_images["Wheat"],
            manager=self.manager,
            container=self.bank_panel)

        self.ore_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(self.wheat_logo.relative_rect.right + SPACING, SPACING, BANK_CARD_WIDTH,
                                      BANK_HALF_HEIGHT),
            image_surface=self.card_images["Ore"],
            manager=self.manager,
            container=self.bank_panel)

        self.dev_logo = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(self.ore_logo.relative_rect.right + SPACING, SPACING, BANK_CARD_WIDTH,
                                      BANK_HALF_HEIGHT),
            html_text="D",
            manager=self.manager,
            container=self.bank_panel)

        self.update_bank_resources()

        self.end_turn_button.disable()
        self.development_button.disable()
        self.city_button.disable()
        self.settlement_button.disable()
        self.road_button.disable()
        self.trade_button.disable()
        self.card_hand =[]# ['Ore', 'Ore', 'Wheat', 'Ore', 'Wheat', 'Wheat', 'Wood']
        self.set_cards(self.card_hand)
        # self.card_hand = ['Ore', 'Ore', 'Wheat', 'Ore', 'Wheat', 'Wheat', 'Wood']
        # self.set_cards(self.card_hand)

    def update_bank_resources(self):
        if self.wood_bank is not None:
            self.wood_bank.kill()
        self.wood_bank = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(self.wood_logo.relative_rect.left, self.wood_logo.relative_rect.bottom + SPACING,
                                      BANK_CARD_WIDTH,
                                      BANK_HALF_HEIGHT),
            html_text=str(self.bank.lumber),
            manager=self.manager,
            container=self.bank_panel)
        if self.brick_bank is not None:
            self.brick_bank.kill()
        self.brick_bank = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(self.brick_logo.relative_rect.left,
                                      self.brick_logo.relative_rect.bottom + SPACING, BANK_CARD_WIDTH,
                                      BANK_HALF_HEIGHT),
            html_text=str(self.bank.brick),
            manager=self.manager,
            container=self.bank_panel)

        if self.sheep_bank is not None:
            self.sheep_bank.kill()
        self.sheep_bank = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(self.sheep_logo.relative_rect.left,
                                      self.sheep_logo.relative_rect.bottom + SPACING, BANK_CARD_WIDTH,
                                      BANK_HALF_HEIGHT),
            html_text=str(self.bank.wool),
            manager=self.manager,
            container=self.bank_panel)

        if self.wheat_bank is not None:
            self.wheat_bank.kill()
        self.wheat_bank = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(self.wheat_logo.relative_rect.left,
                                      self.wheat_logo.relative_rect.bottom + SPACING, BANK_CARD_WIDTH,
                                      BANK_HALF_HEIGHT),
            html_text=str(self.bank.grain),
            manager=self.manager,
            container=self.bank_panel)

        if self.ore_bank is not None:
            self.ore_bank.kill()
        self.ore_bank = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(self.ore_logo.relative_rect.left, self.ore_logo.relative_rect.bottom + SPACING,
                                      BANK_CARD_WIDTH, BANK_HALF_HEIGHT),
            html_text=str(self.bank.ore),
            manager=self.manager,
            container=self.bank_panel)

        if self.dev_bank is not None:
            self.dev_bank.kill()
        self.dev_bank = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(self.dev_logo.relative_rect.left, self.dev_logo.relative_rect.bottom + SPACING,
                                      BANK_CARD_WIDTH, BANK_HALF_HEIGHT),
            html_text=str(self.bank.totalDevelopment),
            manager=self.manager,
            container=self.bank_panel)

    def handle_board_actions(self):
        if self.board_updated and self.board_action == "initialsettlement":
            self.set_butts = self.initial_settlement_buttons()
            self.board_updated = False
        if self.board_updated and self.board_action == "road":
            print("road_butts_reset")
            self.road_butts = self.get_road_buttons()
            self.board_updated = False
        if self.board_updated and self.board_action == "roadfree":
            print("road_butts_reset")
            self.road_butts = self.get_road_buttons(True)
            self.board_updated = False
        if self.board_updated and self.board_action == "robber":
            self.robber_butts = self.get_robber_buttons()  # todo why is this uninitialized
            self.board_updated = False
        if self.board_updated and self.board_action == "set":
            self.set_butts = self.get_settlement_buttons()
            self.board_updated = False
        if self.board_updated and self.board_action == "city":
            self.set_butts = self.get_city_buttons()
            self.board_updated = False
        if self.board_updated and self.board_action == "initialroad":
            self.road_butts = self.initial_road_buttons(self.property_list[-1])
            self.board_updated = False
        if self.board_action != "turn":
            self.end_turn_button.disable()
            self.development_button.disable()
            self.city_button.disable()
            self.settlement_button.disable()
            self.road_button.disable()
            self.trade_button.disable()
        elif self.board_action == "turn" and self.board_updated:
            self.end_turn_button.enable()
            if Actions.buyDevelopmentCheck(self.player):
                self.development_button.enable()
            else:
                self.development_button.disable()
            if len(Actions.buildCityAvailable(self.player)) != 0:
                self.city_button.enable()
            else:
                self.city_button.disable()
            if len(Actions.buildSettlementAvailable(self.player)) != 0:
                self.settlement_button.enable()
            else:
                self.settlement_button.disable()
            if Actions.buildRoadCheck(self.player):
                self.road_button.enable()
            else:
                self.road_button.disable()
            self.trade_button.enable()
            self.board_updated = False

    def handle_mouse_motion(self, event):
        if self.board_action == "initialsettlement" or self.board_action == "set" or self.board_action == "city":
            for butt in self.set_butts:
                butt.on_mousemotion(event)
        elif self.board_action == "initialroad" or self.board_action == "road" or self.board_action == "roadfree":
            for butt in self.road_butts:
                butt.on_mousemotion(event)
        elif self.board_action == "robber":
            for butt in self.robber_butts:
                butt.on_mousemotion(event)

    def handle_mouse_button_down(self, event):
        if self.board_action == "initialsettlement" or self.board_action == "set" or self.board_action == "city":
            for butt in self.set_butts:
                butt.on_mousebuttondown(event)
        elif self.board_action == "initialroad" or self.board_action == "road" or self.board_action == "roadfree":
            for butt in self.road_butts:
                butt.on_mousebuttondown(event)
        elif self.board_action == "robber":
            for butt in self.robber_butts:
                butt.on_mousebuttondown(event)

    def handle_user_event(self, event):
        if event.user_type == pg_g.UI_BUTTON_PRESSED:
            if self.card_picker is not None:
                self.card_picker.handle_ui_button_pressed(event)
            if self.card_trader is not None:
                self.card_trader.handle_ui_button_pressed(event)
            if event.ui_element == self.trade_button:
                if self.card_trader is None:
                    def callback(trade_with, give_cards, take_cards):
                        '''
                        print("wants to trade with " + trade_with)
                        print("wants to give cards" + str(give_cards))
                        print("wants to take cards" + str(take_cards))
                        '''
                        self.trade_cards(give_cards,take_cards)
                        self.card_trader.kill()
                        self.card_trader = None

                    # todo replace the none arguments with resource hand and trade ratios
                    self.card_trader = TradeGui((50, 100), self.player.resourceHand, self.player.bankTrading, self.manager, callback)
                else:
                    self.card_trader.kill()
                    self.card_trader = None
            elif event.ui_element == self.end_turn_button:
                self.board_input.put("end")
            elif event.ui_element == self.road_button:
                self.set_board_action("road", 'turn')
            elif event.ui_element == self.settlement_button:
                self.set_board_action("set", 'turn')
            elif event.ui_element == self.city_button:
                self.set_board_action("city", 'turn')
            elif event.ui_element == self.development_button:
                self.board_input.put("dev")
            elif event.ui_element == self.dice_button:
                self.is_rolling = not self.is_rolling
            elif '#knight' in event.ui_element.object_ids and not self.player.development_card_played and self.board_action == "turn":
                self.player.development_card_played = True
                self.card_hand.remove('knight')
                self.player.developmentHand.remove_card('knight')
                self.set_cards(self.card_hand)
                self.set_board_action("robber", 'turn')
                self.player.largestArmy += 1
            elif '#roadBuilding' in event.ui_element.object_ids and not self.player.development_card_played and self.board_action == "turn":
                self.player.development_card_played = True
                self.card_hand.remove('roadBuilding')
                self.player.developmentHand.remove_card('roadBuilding')
                self.set_cards(self.card_hand)
                self.board_input.put('roadroad')
                print('roadBuilding clicked')
            elif '#yearOfPlenty' in event.ui_element.object_ids and not self.player.development_card_played and self.board_action == "turn":
                self.player.development_card_played = True
                if self.card_picker is None:
                    def callback(card_type):
                        print(card_type + ' was selected for year of plenty')
                        self.card_picker.kill()
                        self.card_picker = None
                        self.get_cards([card_type, card_type])
                        self.card_hand.remove('yearOfPlenty')
                        self.player.developmentHand.remove_card('yearOfPlenty')
                        self.set_cards(self.card_hand)
                    self.card_picker = CardPickerGui((50, 200), self.manager, callback)
                print('yearOfPlenty clicked')
            elif '#monopoly' in event.ui_element.object_ids and not self.player.development_card_played and self.board_action == "turn":
                self.player.development_card_played = True
                if self.card_picker is None:
                    def callback(card_type):
                        print(card_type + ' was selected for monopoly')
                        self.card_picker.kill()
                        self.card_picker = None
                        self.card_hand.remove('monopoly')
                        self.player.developmentHand.remove_card('monopoly')
                        self.get_monopoly(card_type)
                    self.card_picker = CardPickerGui((50, 200), self.manager, callback)
                print('monopoly clicked')
            elif '#victoryPoint' in event.ui_element.object_ids and not self.player.development_card_played and self.board_action == "turn":
                print('victoryPoint clicked')

    def run(self, board):
        self.game_board = board
        self.game_board.translate_to_3d()
        self.building_locations = StructureBoard(3, self.game_board.get_array())
        self.initialize_gui()
        #self.card_hand += ['roadBuilding', 'roadBuilding', 'knight', 'monopoly', '']
        self.set_cards(self.card_hand)
        pygame.display.flip()  # todo consider removing
        self.running = True
        self.robber_butts = []

        self.display_dice([random.randint(1, 6), random.randint(1, 6)])

        # testing, todo remove
        #self.set_player_info(self.player, self.enemy_list)
        #self.get_dev_card("yearOfPlenty")
        # end
        
        while self.running:
            time_delta = self.clock.tick(30) / 1000.0
            if self.board_updated:
                self.update_bank_resources()
                self.set_player_info(self.player, self.enemy_list)
            if self.cards_updated:
                self.update_cards()
                self.cards_updated = False

            self.handle_board_actions()

            for event in pygame.event.get():
                self.manager.process_events(event)
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down(event)
                elif event.type == pygame.USEREVENT:  # todo make a check that it is actually your turn
                    self.handle_user_event(event)

            self.manager.update(time_delta)

            self.draw_board()
            if self.is_rolling:
                self.display_dice([random.randint(1, 6), random.randint(1, 6)])  # todo check this
            self.manager.draw_ui(self.game_window)

            pygame.display.flip()

    def draw_board(self):
        # paint background
        self.game_window.fill((61, 120, 180))
        # draw hexes
        for tile in self.resource_hexes:
            self.game_window.blit(self.texture_dictionary.get(tile.resource),
                                  self.translate_hex_to_xy(tile.location, self.board_center, int(self.hex_size / 2)))

        # draw Board
        self.game_window.blit(self.object_textures.get('Board'),
                              (int(self.board_center[0] - self.grid_size[0] / 2 + self.hex_size / 2),
                               int(self.board_center[1] - self.grid_size[1] / 2 + self.hex_size / 2)))
        # draw resource numbers
        for tile in self.resource_hexes:
            if tile.resource == 'Desert':
                pass
            else:
                text_surface = self.font.render(str(tile.number), False, (255, 255, 255))
                coord = self.translate_hex_to_xy(tile.location, self.board_center, int(self.hex_size / 2))
                self.game_window.blit(text_surface, (coord[0] + self.hex_size / 2 - text_surface.get_width() / 2,
                                                     coord[1] + self.hex_size / 2 - text_surface.get_height() / 2))
        # draw ports
        for port in self.port_hexes:
            self.game_window.blit(self.port_textures.get(port.resource),
                                  self.translate_hex_to_xy(port.location, self.board_center, int(self.hex_size / 2)))

        # draw settlements
        for properties in self.property_list:
            # pygame.draw.circle(self.game_window, COLORS[properties.color],
            #                   CornerNode.translate_settlement((properties.cord1, properties.cord2), self.board_center,
            #                                                   int(self.hex_size / 2)), 30)
            shifted_points = []
            location = CornerNode.translate_settlement((properties.cord1, properties.cord2), self.board_center,
                                                       int(self.hex_size / 2))
            if properties.city:
                for points in self.city_points:
                    shifted_points.append((location[0] + points[0], location[1] + points[1]))

                pygame.gfxdraw.filled_polygon(self.game_window, shifted_points, COLORS[properties.color])
            else:
                for points in self.house_points:
                    shifted_points.append((location[0] + points[0], location[1] + points[1]))

                pygame.gfxdraw.filled_polygon(self.game_window, shifted_points, COLORS[properties.color])

        # draw roads
        for properties in self.road_list:
            location = EdgeNode.translate_road((properties.cord1, properties.cord2), self.board_center,
                                               int(self.hex_size / 2))
            shifted_points = []
            # variation 0, 1, 2 = |, /, \

            if properties.cord2 % 2 == 1:
                variation = 0
            elif (properties.cord2 + properties.cord1) % 4 == 1:
                variation = 1
            else:
                variation = 2

            for points in self.road_points[variation]:
                shifted_points.append((location[0] + points[0], location[1] + points[1]))

            pygame.gfxdraw.filled_polygon(self.game_window, shifted_points, COLORS[properties.color])
        loc = self.translate_hex_to_xy(self.game_board.get_robber().location, self.board_center, int(self.hex_size / 2))
        pygame.draw.circle(self.game_window, (50, 50, 50),
                           (loc[0] + int(self.hex_size / 3), loc[1] + int(self.hex_size / 3)), 30)

        if self.board_action == "initialsettlement" or self.board_action == "set" or self.board_action == "city":
            for butt in self.set_butts:
                butt.draw(self.game_window)
        if self.board_action == "initialroad" or self.board_action == "road" or self.board_action == "roadfree":
            for butt in self.road_butts:
                butt.draw(self.game_window)
        if self.board_action == "robber":
            for butt in self.robber_butts:
                butt.draw(self.game_window)
