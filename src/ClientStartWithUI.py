import pygame
import pygame_gui
from pygame_gui.elements import UITextEntryLine

from src.ClientMain import client

'''
sys.path.insert(0, '../src')
from pygame_gui.elements import UITextEntryLine
from ClientMain import client
from GameBoard.NodeRoads import *
from GameBoard.Board import *
from client.Client import *
from client.Player import *
'''


# os.environ['SDL_AUDIODRIVER'] = 'dsp'
# os.putenv("DISPLAY", "localhost:0")
# os.environ['SDL_AUDIODRIVER'] = 'x11'


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


def board_thread():
    client.run()


class ClientStartWithUI:

    def __init__(self):
        self.children = []
        self.user_interface()

    def open_client(self):
        exec(open('client.py').read())

    def user_interface(self):
        WINDOW_WIDTH = 300
        WINDOW_HEIGHT = 200

        Colors = {
            'Red': (127, 0, 0),
            'Cyan': (0, 255, 255),
            'Orange': (255, 106, 0),
            'Blue': (0, 38, 255),
            'Green': (0, 153, 15),
            'Pink': (255, 0, 110),
            'Yellow': (255, 216, 0)
        }

        pygame.init()

        pygame.display.set_caption('Startup Menu')
        center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), './themes/button_theme.json')
        clock = pygame.time.Clock()

        background_color = (61, 120, 180)
        background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        background.fill(background_color)

        # color button dimensions
        button_center = [center[0], center[1] + 50]
        button_size = [30, 30]
        padding = 5
        num_buttons = 7

        colors = list(Colors.keys())

        color_buttons = []

        for index in range(-3, 4):
            position = (int(button_center[0] + index * (padding + button_size[0]) - button_size[0] / 2),
                        int(button_center[1] - padding - 75 - 3))
            pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, button_size),
                                         text='', manager=manager, object_id='#' + colors[index + 3])

        # button dimensions
        button_width = 240
        button_height = 40
        padding = 10

        # text box dimensions
        entry_width = 240
        entry_height = 40
        padding = 10

        position = (int(center[0] - button_width / 2),
                    int(center[1] + padding / 2 + 25))
        client_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (button_width, button_height)),
                                                     text='Connect', manager=manager, object_id='#standard_button')

        position = (int(center[0] - button_width / 2),
                    int(center[1] - padding / 2 - entry_height / 2 + 25))

        ip_entry = UITextEntryLine(relative_rect=pygame.Rect(position, (button_width - 80, button_height)),
                                   manager=manager, object_id='#text_entry')
        ip_entry.set_text('127.0.0.1')

        position = (int(center[0] - button_width / 2 + button_width - 80 + padding),
                    int(center[1] - padding / 2 - entry_height / 2 + 25))

        port_entry = UITextEntryLine(relative_rect=pygame.Rect(position, (80 - padding, button_height)),
                                     manager=manager, object_id='#text_entry')
        port_entry.set_text('1233')

        position = (int(center[0] - button_width / 2 + 3),
                    int(center[1] - padding / 2 - entry_height / 2 + 25 - 65 + 3))

        name_label = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(position, (50, button_height - 17)),
                                                          text='Name:', manager=manager, object_id='#text_entry')

        position = (int(center[0] - button_width / 2 + 55 + padding),
                    int(center[1] - padding / 2 - entry_height / 2 + 25 - 65))

        name_entry = UITextEntryLine(relative_rect=pygame.Rect(position, (button_width - 55 - padding, button_height)),
                                     manager=manager, object_id='#text_entry')

        # update screen
        pygame.display.flip()

        running = True
        client_flag = False
        server_flag = False

        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                # close if X is clicked
                if event.type == pygame.QUIT:
                    running = False

                # close if ESC is pressed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        # action if client is pressed
                        if event.ui_element == client_button:
                            client_flag = True
                            # print('Client created')

                manager.process_events(event)

            manager.update(time_delta)

            window.blit(background, (0, 0))
            manager.draw_ui(window)

            pygame.display.update()

            if client_flag:
                running = False
                client_flag = False
                # self.children.append(subprocess.Popen([sys.executable, './ClientMain.py']))
                pygame.quit()
                start_instance = client(ip_entry.text, port_entry.text, name_entry.text)


if __name__ == "__main__":
    ClientStartWithUI()
