import math
import os

import pygame


class road_hardware_art:
    @staticmethod
    def generate_road_polygons(road_length, road_ratio):
        # create 3 types of roads, |, /, \
        road_points = []
        road_width = road_length * road_ratio

        road_points.append([
            [-road_width, road_length],
            [road_width, road_length],
            [road_width, -road_length],
            [-road_width, -road_length]
        ])

        angle = math.pi * 5 / 6
        half_angle = math.pi / 2
        end_points = [[road_length * math.cos(angle), road_length * math.sin(angle)],
                      [-1 * road_length * math.cos(angle), -1 * road_length * math.sin(angle)]]
        road_points.append([])

        road_points[1].append([end_points[0][0] - road_width * math.cos(angle + half_angle),
                               end_points[0][1] - road_width * math.sin(angle + half_angle)])
        road_points[1].append([end_points[0][0] - road_width * math.cos(angle - half_angle),
                               end_points[0][1] - road_width * math.sin(angle - half_angle)])
        road_points[1].append([end_points[1][0] - road_width * math.cos(angle - half_angle),
                               end_points[1][1] - road_width * math.sin(angle - half_angle)])
        road_points[1].append([end_points[1][0] - road_width * math.cos(angle + half_angle),
                               end_points[1][1] - road_width * math.sin(angle + half_angle)])

        angle = math.pi / 6
        end_points = [[road_length * math.cos(angle), road_length * math.sin(angle)],
                      [-1 * road_length * math.cos(angle), -1 * road_length * math.sin(angle)]]
        road_points.append([])

        road_points[2].append([end_points[0][0] - road_width * math.cos(angle + half_angle),
                               end_points[0][1] - road_width * math.sin(angle + half_angle)])
        road_points[2].append([end_points[0][0] - road_width * math.cos(angle - half_angle),
                               end_points[0][1] - road_width * math.sin(angle - half_angle)])
        road_points[2].append([end_points[1][0] - road_width * math.cos(angle - half_angle),
                               end_points[1][1] - road_width * math.sin(angle - half_angle)])
        road_points[2].append([end_points[1][0] - road_width * math.cos(angle + half_angle),
                               end_points[1][1] - road_width * math.sin(angle + half_angle)])

        return road_points


class texture_scale:
    @staticmethod
    def scale_resource_tiles(hex_size):

        base_path = os.path.dirname(__file__)

        texture_dictionary = {
            'Desert': pygame.image.load(os.path.join(base_path, '../assets/desert_hex.png')),
            'Ocean': pygame.image.load(os.path.join(base_path, '../assets/ocean_hex.png')),
            'Wheat': pygame.image.load(os.path.join(base_path, '../assets/field_hex.png')),
            'Brick': pygame.image.load(os.path.join(base_path, '../assets/clay_hex.png')),
            'Ore': pygame.image.load(os.path.join(base_path, '../assets/mountain_hex.png')),
            'Sheep': pygame.image.load(os.path.join(base_path, '../assets/grass_hex.png')),
            'Wood': pygame.image.load(os.path.join(base_path, '../assets/forest_hex.png')),
        }

        for key in texture_dictionary:
            picture = texture_dictionary.get(key)
            texture_dictionary[key] = pygame.transform.scale(picture, (int(hex_size), int(hex_size)))

        return texture_dictionary

    @staticmethod
    def scale_port_tiles(hex_size):

        base_path = os.path.dirname(__file__)

        port_textures = {
            'None': pygame.image.load(os.path.join(base_path, '../assets/default_port.png')),
            'Wheat': pygame.image.load(os.path.join(base_path, '../assets/wheat_port.png')),
            'Brick': pygame.image.load(os.path.join(base_path, '../assets/brick_port.png')),
            'Ore': pygame.image.load(os.path.join(base_path, '../assets/ore_port.png')),
            'Sheep': pygame.image.load(os.path.join(base_path, '../assets/sheep_port.png')),
            'Wood': pygame.image.load(os.path.join(base_path, '../assets/wood_port.png')),
        }

        for key in port_textures:
            picture = port_textures.get(key)
            port_textures[key] = pygame.transform.scale(picture, (int(hex_size), int(hex_size)))

        return port_textures

    @staticmethod
    def scale_cards(card_size):

        base_path = os.path.dirname(__file__)

        CARD_IMAGES = {
            'knight': pygame.image.load(os.path.join(base_path, '../assets/cards/dev/Knight.png')),
            'monopoly': pygame.image.load(os.path.join(base_path, '../assets/cards/dev/Monopoly.png')),
            'roadBuilding': pygame.image.load(os.path.join(base_path, '../assets/cards/dev/Road_Building.png')),
            'yearOfPlenty': pygame.image.load(os.path.join(base_path, '../assets/cards/dev/Year_Of_Plenty.png')),
            'victoryPoint': pygame.image.load(os.path.join(base_path, '../assets/cards/dev/Victory_Point.png')),
            'Brick': pygame.image.load(os.path.join(base_path, '../assets/cards/res/bricks.png')),
            'Ore': pygame.image.load(os.path.join(base_path, '../assets/cards/res/ore.png')),
            'Sheep': pygame.image.load(os.path.join(base_path, '../assets/cards/res/sheep.png')),
            'Wheat': pygame.image.load(os.path.join(base_path, '../assets/cards/res/wheat.png')),
            'Wood': pygame.image.load(os.path.join(base_path, '../assets/cards/res/wood.png'))
        }

        for key in CARD_IMAGES:
            picture = CARD_IMAGES.get(key)
            CARD_IMAGES[key] = pygame.transform.scale(picture, card_size)

        return CARD_IMAGES


class button_resources:
    @staticmethod
    def save_scaled_cards(scaled_cards):
        base_path = os.path.dirname(__file__)

        for key in scaled_cards.keys():
            card = scaled_cards[key]
            pygame.image.save(card, os.path.join(base_path, '../assets/scaled/' + key + '.png'))

            darkened_amount = 10
            darkened_card = card.copy()
            dark = pygame.Surface((card.get_width(), card.get_height()), flags=pygame.SRCALPHA)
            dark.fill((darkened_amount, darkened_amount, darkened_amount, 0))
            darkened_card.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            pygame.image.save(darkened_card, os.path.join(base_path, '../assets/scaled/' + key + '_disabled.png'))

            lightened_amount = 10
            lightened_card = card.copy()
            light = pygame.Surface((card.get_width(), card.get_height()), flags=pygame.SRCALPHA)
            light.fill((lightened_amount, lightened_amount, lightened_amount, 0))
            lightened_card.blit(light, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            pygame.image.save(lightened_card, os.path.join(base_path, '../assets/scaled/' + key + '_hovered.png'))
