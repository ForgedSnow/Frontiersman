import pygame
import pygame_gui as pg_g
from client.GuiConstants import CARD_SIZE, SPACING

CARDS = ['Brick', 'Ore', 'Sheep', 'Wheat', 'Wood']


class TradeGui:
    def __init__(self, top_left, resource_hand, trade_ratios, manager, callback, container=None):
        self.resource_hand = resource_hand
        self.trade_ratios = trade_ratios
        self.manager = manager
        self.callback = callback
        self.is_valid = False

        self.panel = pg_g.elements.UIPanel(
            relative_rect=pygame.Rect(top_left, ((CARD_SIZE[0] + SPACING) * 20, (CARD_SIZE[1] + SPACING) * 3)),
            starting_layer_height=1,
            manager=self.manager,
            container=container,
        )
        self.give_panel = pg_g.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, self.panel.relative_rect.width / 2, CARD_SIZE[1] + 2 * SPACING),
            starting_layer_height=1,
            manager=self.manager,
            container=self.panel,
        )
        self.give_card_keys = []
        self.give_card_elements = []
        self.take_panel = pg_g.elements.UIPanel(
            relative_rect=pygame.Rect(self.give_panel.relative_rect.right, 0, self.panel.relative_rect.width / 2, CARD_SIZE[1] + 2 * SPACING),
            starting_layer_height=1,
            manager=self.manager,
            container=self.panel,
        )
        self.take_card_keys = []
        self.take_card_elements = []

        card_offset = (self.panel.relative_rect.width / 2 - 5 * CARD_SIZE[0]) / 6

        self.give_buttons = [
            pg_g.elements.UIButton(
                relative_rect=pygame.Rect(
                    (self.give_panel.relative_rect.left + card_offset + i * (CARD_SIZE[0] + card_offset), self.give_panel.relative_rect.bottom + SPACING), CARD_SIZE),
                text="",
                manager=self.manager,
                container=self.panel,
                object_id="#" + card,
            ) for i, card in enumerate(CARDS)
        ]
        self.take_buttons = [
            pg_g.elements.UIButton(
                relative_rect=pygame.Rect(
                    (self.take_panel.relative_rect.left + card_offset + i * (CARD_SIZE[0] + card_offset), self.take_panel.relative_rect.bottom + SPACING), CARD_SIZE),
                text="",
                manager=self.manager,
                container=self.panel,
                object_id="#" + card
            ) for i, card in enumerate(CARDS)
        ]

        pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(
                self.give_buttons[0].relative_rect.left, self.give_buttons[0].relative_rect.bottom + SPACING,
                self.give_buttons[0].relative_rect.width, 35
            ),
            html_text=str(self.trade_ratios.brick)+":1",  # todo replace with value from self.trade_ratios
            manager=self.manager,
            container=self.panel,
        )

        pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(
                self.give_buttons[1].relative_rect.left, self.give_buttons[1].relative_rect.bottom + SPACING,
                self.give_buttons[1].relative_rect.width, 35
            ),
            html_text=str(self.trade_ratios.ore)+":1",  # todo replace with value from self.trade_ratios
            manager=self.manager,
            container=self.panel,
        )

        pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(
                self.give_buttons[2].relative_rect.left, self.give_buttons[2].relative_rect.bottom + SPACING,
                self.give_buttons[1].relative_rect.width, 35
            ),
            html_text=str(self.trade_ratios.wool)+":1",  # todo replace with value from self.trade_ratios
            manager=self.manager,
            container=self.panel,
        )

        pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(
                self.give_buttons[3].relative_rect.left, self.give_buttons[3].relative_rect.bottom + SPACING,
                self.give_buttons[3].relative_rect.width, 35
            ),
            html_text=str(self.trade_ratios.grain)+":1",  # todo replace with value from self.trade_ratios
            manager=self.manager,
            container=self.panel,
        )

        pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(
                self.give_buttons[4].relative_rect.left, self.give_buttons[4].relative_rect.bottom + SPACING,
                self.give_buttons[4].relative_rect.width, 35
            ),
            html_text=str(self.trade_ratios.lumber)+":1",  # todo replace with value from self.trade_ratios
            manager=self.manager,
            container=self.panel,
        )

        button_width = 300
        button_spacing = (self.take_panel.relative_rect.width - 2 * button_width) / 3
        self.trade_with_bank_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect(
                self.take_panel.relative_rect.left + button_spacing, self.take_buttons[0].relative_rect.bottom + SPACING,
                button_width, 45
            ),
            text="Trade with bank",
            manager=self.manager,
            container=self.panel,
        )
        self.trade_with_player_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect(
                self.take_panel.relative_rect.left + 2 * button_spacing + button_width, self.take_buttons[0].relative_rect.bottom + SPACING,
                button_width, 45
            ),
            text="Trade with players",
            manager=self.manager,
            container=self.panel,
        )

        self.info_text = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(
                0, self.trade_with_bank_button.relative_rect.bottom, self.panel.relative_rect.width - 2 * SPACING, 35
            ),
            html_text="Error text goes here",  # todo update this
            manager=self.manager,
            container=self.panel
        )
        self.trade_with_bank_button.disable()
        self.trade_with_player_button.disable()
    def kill(self):
        self.panel.kill()

    def update_give_cards(self):
        for elem in self.give_card_elements:
            elem.kill()
        self.give_card_elements = []

        if len(self.give_card_keys) == 0:
            return

        if len(self.give_card_keys) > 1:
            card_width = (self.give_panel.relative_rect.width - CARD_SIZE[0]) / (len(self.give_card_keys) - 1)
        else:
            card_width = CARD_SIZE[0] + SPACING
        if card_width >= CARD_SIZE[0] + SPACING:
            card_width = CARD_SIZE[0] + SPACING
            offset = (self.give_panel.relative_rect.width - card_width * len(self.give_card_keys)) / 2
        else:
            offset = 0

        for i, card in enumerate(self.give_card_keys):
            self.give_card_elements.append(pg_g.elements.UIButton(
                relative_rect=pygame.Rect((offset + i * card_width, SPACING), CARD_SIZE),
                text="",
                manager=self.manager,
                container=self.give_panel,
                object_id="#" + card
            ))
        self.validate_trade()

    def update_take_cards(self):
        for elem in self.take_card_elements:
            elem.kill()
        self.take_card_elements = []

        if len(self.take_card_keys) == 0:
            return

        if len(self.take_card_keys) > 1:
            card_width = (self.give_panel.relative_rect.width - CARD_SIZE[0]) / (len(self.take_card_keys) - 1)
        else:
            card_width = CARD_SIZE[0] + SPACING
        if card_width >= CARD_SIZE[0] + SPACING:
            card_width = CARD_SIZE[0] + SPACING
            offset = (self.give_panel.relative_rect.width - card_width * len(self.take_card_keys)) / 2
        else:
            offset = 0

        for i, card in enumerate(self.take_card_keys):
            self.take_card_elements.append(pg_g.elements.UIButton(
                relative_rect=pygame.Rect((offset + i * card_width, SPACING), CARD_SIZE),
                text="",
                manager=self.manager,
                container=self.take_panel,
                object_id="#" + card
            ))
        self.validate_trade()

    def validate_trade(self):
        # todo, if problem with trading return string indicating problem. e.g. "Not enough wood."
        if len(self.give_card_keys)==self.trade_ratios.brick and self.give_card_keys.count(CARDS[0])==self.trade_ratios.brick and len(self.take_card_keys)==1:
            self.trade_with_bank_button.enable()
        elif len(self.give_card_keys)==self.trade_ratios.ore and self.give_card_keys.count(CARDS[1])==self.trade_ratios.ore and len(self.take_card_keys)==1:
            self.trade_with_bank_button.enable()
        elif len(self.give_card_keys)==self.trade_ratios.wool and self.give_card_keys.count(CARDS[2])==self.trade_ratios.wool and len(self.take_card_keys)==1:
            self.trade_with_bank_button.enable()
        elif len(self.give_card_keys)==self.trade_ratios.grain and self.give_card_keys.count(CARDS[3])==self.trade_ratios.grain and len(self.take_card_keys)==1:
            self.trade_with_bank_button.enable()
        elif len(self.give_card_keys)==self.trade_ratios.lumber and self.give_card_keys.count(CARDS[4])==self.trade_ratios.lumber and len(self.take_card_keys)==1:
            self.trade_with_bank_button.enable()
        self.is_valid = True
        self.error_text = "Error text goes here"
        # todo change the buttons to enabled/disabled
        # todo update error text
        
    def handle_ui_button_pressed(self, event):  # Todo
        if event.ui_element in self.give_buttons:
            try:
                index = self.give_buttons.index(event.ui_element)
                if index==0 and self.give_card_keys.count(CARDS[index])<self.resource_hand.brick:
                   self.give_card_keys.append(CARDS[index])
                elif index==1 and self.give_card_keys.count(CARDS[index])<self.resource_hand.ore:
                    self.give_card_keys.append(CARDS[index])
                elif index==2 and self.give_card_keys.count(CARDS[index])<self.resource_hand.wool:
                    self.give_card_keys.append(CARDS[index])
                elif index==3 and self.give_card_keys.count(CARDS[index])<self.resource_hand.grain:
                    self.give_card_keys.append(CARDS[index])
                elif index==4 and self.give_card_keys.count(CARDS[index])<self.resource_hand.lumber:
                    self.give_card_keys.append(CARDS[index]) 
                self.update_give_cards()
            except ValueError:
                pass
        elif event.ui_element in self.take_buttons:
            try:
                index = self.take_buttons.index(event.ui_element)
                self.take_card_keys.append(CARDS[index])
                self.update_take_cards()
            except ValueError:
                pass
        elif event.ui_element in self.give_card_elements:
            try:
                index = self.give_card_elements.index(event.ui_element)
                self.give_card_keys.pop(index)
                self.update_give_cards()
            except ValueError:
                pass
        elif event.ui_element in self.take_card_elements:
            try:
                index = self.take_card_elements.index(event.ui_element)
                self.take_card_keys.pop(index)
                self.update_take_cards()
            except ValueError:
                pass
        elif event.ui_element == self.trade_with_bank_button:
            self.callback('tradebank', self.give_card_keys, self.take_card_keys)
        elif event.ui_element == self.trade_with_player_button:
            self.callback('tradeplayer', self.give_card_keys, self.take_card_keys)
