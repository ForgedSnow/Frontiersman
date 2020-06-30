import pygame
import pygame_gui as pg_g

'''
        GUI_outsource = ClientGUI.GUI_Helper.client_gui(SPACING, ACTION_SIZE, self.manager, RESOLUTION, CARD_SIZE,
                                             INFO_WIDTH, self.card_images)
        end_turn_button = GUI_outsource[0]
        trade_button = GUI_outsource[1]
        self.info_panel = GUI_outsource[2]
        self.action_panel = GUI_outsource[3]
        self.card_panel = GUI_outsource[4]
'''


class GUI_Helper:
    @staticmethod
    def client_gui(spacing, action_size, manager, resolution, card_size, info_width, card_images):
        action_panel_layout = pygame.Rect(0, 0, 6 * action_size[0] + 7 * spacing, action_size[1] + 2 * spacing)
        action_panel_layout.bottomright = (-spacing, -spacing)
        action_panel = pg_g.elements.UIPanel(relative_rect=action_panel_layout,
                                             starting_layer_height=1,
                                             manager=manager,
                                             anchors={'left': 'right',
                                                      'right': 'right',
                                                      'top': 'bottom',
                                                      'bottom': 'bottom'}
                                             )

        trade_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((0 * action_size[0] + 0 * spacing, 0), action_size),
            container=action_panel,
            manager=manager,
            text="TRADE")

        road_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((1 * action_size[0] + 1 * spacing, 0), action_size),
            container=action_panel,
            manager=manager,
            text="ROAD")

        settlement_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((2 * action_size[0] + 2 * spacing, 0), action_size),
            container=action_panel,
            manager=manager,
            text="SETTLE")

        city_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((3 * action_size[0] + 3 * spacing, 0), action_size),
            container=action_panel,
            manager=manager,
            text="CITY")

        development_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((4 * action_size[0] + 4 * spacing, 0), action_size),
            container=action_panel,
            manager=manager,
            text="DEV CARD")

        end_turn_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((5 * action_size[0] + 5 * spacing, 0), action_size),
            container=action_panel,
            manager=manager,
            text="END",
        )

        card_panel_layout = pygame.Rect(0, 0, resolution[0] - action_panel_layout.width - 2 * spacing,
                                        card_size[1] + 2 * spacing)
        print(action_panel_layout.width, '| Spacing: ', spacing, )
        card_panel_layout.bottomleft = (spacing, -spacing)
        card_panel = pg_g.elements.UIPanel(relative_rect=card_panel_layout,
                                           starting_layer_height=1,
                                           manager=manager,
                                           anchors={'left': 'left',
                                                    'right': 'right',
                                                    'top': 'bottom',
                                                    'bottom': 'bottom'}
                                           )

        info_panel_layout = pygame.Rect(0, 0, info_width, resolution[1] - action_panel_layout.height - 2 * spacing)
        info_panel_layout.topright = (-spacing, spacing)
        info_panel = pg_g.elements.UIPanel(relative_rect=info_panel_layout,
                                           starting_layer_height=1,
                                           manager=manager,
                                           anchors={'left': 'right',
                                                    'right': 'right',
                                                    'top': 'top',
                                                    'bottom': 'top'}
                                           )

        bank_panel = pg_g.elements.UIPanel(relative_rect=pygame.Rect(0, 0, info_width - 2 * spacing, 100),
                                           container=info_panel,
                                           starting_layer_height=1,
                                           manager=manager)

        bank_logo = pg_g.elements.UITextBox(relative_rect=pygame.Rect(spacing, spacing, 60, 60),
                                            container=bank_panel,
                                            manager=manager,
                                            html_text="Bank"
                                            )

        wood_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(bank_logo.relative_rect.right + spacing, spacing, 40, 50),
            image_surface=card_images["Wood"],
            manager=manager,
            container=bank_panel)

        wood_bank = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(wood_logo.relative_rect.left, wood_logo.relative_rect.bottom + spacing, 40, 40),
            html_text="20",
            manager=manager,
            container=bank_panel)

        brick_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(wood_logo.relative_rect.right + spacing, spacing, 40, 50),
            image_surface=card_images["Brick"],
            manager=manager,
            container=bank_panel)

        brick_bank = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(brick_logo.relative_rect.left, brick_logo.relative_rect.bottom + spacing, 40, 40),
            html_text="20",
            manager=manager,
            container=bank_panel)

        sheep_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(brick_logo.relative_rect.right + spacing, spacing, 40, 50),
            image_surface=card_images["Sheep"],
            manager=manager,
            container=bank_panel)

        sheep_bank = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(sheep_logo.relative_rect.left, sheep_logo.relative_rect.bottom + spacing, 40, 40),
            html_text="20",
            manager=manager,
            container=bank_panel)

        wheat_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(sheep_logo.relative_rect.right + spacing, spacing, 40, 50),
            image_surface=card_images["Wheat"],
            manager=manager,
            container=bank_panel)

        wheat_bank = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(wheat_logo.relative_rect.left, wheat_logo.relative_rect.bottom + spacing, 40, 40),
            html_text="20",
            manager=manager,
            container=bank_panel)

        ore_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(wheat_logo.relative_rect.right + spacing, spacing, 40, 50),
            image_surface=card_images["Ore"],
            manager=manager,
            container=bank_panel)

        ore_bank = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(ore_logo.relative_rect.left, ore_logo.relative_rect.bottom + spacing, 40, 40),
            html_text="20",
            manager=manager,
            container=bank_panel)

        end_turn_button.disable()
        development_button.disable()
        city_button.disable()
        settlement_button.disable()
        road_button.disable()
        trade_button.disable()

        return end_turn_button, trade_button, info_panel, action_panel, card_panel
