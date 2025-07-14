#arquivo utilizar o window,vmouse e keyboard como uma variável global, para usar em todos os outros arquivos
from pplay.window import Window
import pygame

window = Window(1500, 850)
window.set_title("window_main")
mouse = window.get_mouse()
keyboard = window.get_keyboard()

def click(sprite):
    if mouse.is_button_pressed(1):
        if mouse.is_over_object(sprite):
            return True

class Sprite_player:
    def __init__(self):
        self.original_image = pygame.image.load("Sprites/Game/player.png").convert_alpha()  # Use o caminho correto
        self.image = self.original_image
        self.x = 0
        self.y = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.angle = 0

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_rotation(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, angle)
        # Atualize width/height se necessário:
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def draw(self):
        # Centralize a imagem rotacionada
        rect = self.image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        window.screen.blit(self.image, rect.topleft)