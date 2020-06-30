import sys

sys.path.insert(0, '../src')
import pygame


class ButtonState:  # credit to https://www.reddit.com/r/pygame/comments/hblj83/circular_button_with_variable_width_and_height/
    def __init__(self, color, size, position, anchor):
        self.rect = pygame.Rect((0, 0), size)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.image, color, self.rect)
        setattr(self.rect, anchor, position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class CircleButton:
    def __init__(self, normalcolor, hovercolor, size, position, anchor, callback, user_data=None):
        self.normal = ButtonState(normalcolor, size, position, "center")
        self.hover = ButtonState(hovercolor, size, position, "center")
        self.image = self.normal
        self.callback = callback
        self.user_data = user_data

    def draw(self, surface):
        self.image.draw(surface)

    def on_mousemotion(self, event):
        if self.normal.rect.collidepoint(event.pos):
            pos = event.pos[0] - self.normal.rect.x, event.pos[1] - self.normal.rect.y
            if self.normal.image.get_at(pos).a:
                self.image = self.hover
            else:
                self.image = self.normal
        else:
            self.image = self.normal

    def on_mousebuttondown(self, event):
        if self.hover.rect.collidepoint(event.pos):
            pos = event.pos[0] - self.hover.rect.x, event.pos[1] - self.hover.rect.y
            if self.hover.image.get_at(pos).a:
                self.callback(self.user_data)
