import pygame
import pygame_gui as pg_g
from client.GuiConstants import CARD_SIZE, SPACING

CARDS = ['Brick', 'Ore', 'Sheep', 'Wheat', 'Wood']


class CardPickerGui:
    def __init__(self, top_left, manager, callback, container=None):
        self.manager = manager
        self.callback = callback
        self.panel = pg_g.elements.UIPanel(
            relative_rect=pygame.Rect(top_left, ((CARD_SIZE[0] + SPACING) * 5 + 10 * SPACING, CARD_SIZE[1] + 10 * SPACING)),
            starting_layer_height=1,
            manager=self.manager,
            container=container,
        )
        self.cards = []

        for i, card in enumerate(CARDS):
            self.cards.append(pg_g.elements.UIButton(
                relative_rect=pygame.Rect((i * (CARD_SIZE[0] + SPACING) + 4 * SPACING, 4 * SPACING), CARD_SIZE),
                text="",
                manager=self.manager,
                container=self.panel,
                object_id="#" + card
            ))

    def kill(self):
        self.panel.kill()

    def handle_ui_button_pressed(self, event):
        try:
            index = self.cards.index(event.ui_element)
            self.callback(CARDS[index])
        except ValueError:
            pass
