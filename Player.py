from config import window, mouse, keyboard, Sprite_player
from Sprites import Sprites_jogador
import pygame
import math

player = None
def init_player():
    global player
    player = Sprites_jogador
    player = Sprite_player()  # Use a classe com rotação!
    player.set_position((window.width - player.width)/2, (window.height - player.height)/2)

def default():
    global player
    player.draw()

def update_player_rotation():
    global player
    # Centro do player
    player_center_x = player.x + player.width / 2
    player_center_y = player.y + player.height / 2

    # Posição do mouse
    mouse_x, mouse_y = mouse.get_position()

    # Calcula ângulo em graus
    dx = mouse_x - player_center_x
    dy = mouse_y - player_center_y
    angle = math.degrees(math.atan2(-dy, dx))  # -dy porque o eixo Y cresce para baixo

    # Rotaciona o sprite
    player.set_rotation(angle)