from config import window, mouse, keyboard, Sprite_player
from Sprites import Sprites_jogador
import pygame
import math

player = shooting = None

def init_player():
    global player, shooting
    player = Sprite_player()

    return player

def default(piscando=False):
    global player
    player.set_position(window.width // 2 - player.width // 2, window.height // 2 - player.height // 2)
    if piscando:
        # Pisca: desenha só em alguns frames
        if int(pygame.time.get_ticks() * 0.01) % 2 == 0:
            player.draw()
    else:
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

def shooting_funcionality(disparos, last_shot_time, current_time, player_world_x, player_world_y):
    global player

    if mouse.is_button_pressed(1):
        if current_time - last_shot_time >= 0.20: #intervalo entre disparos
            _, shooting_sprite = Sprites_jogador()
            # Centro do player no mundo
            player_center_x = player_world_x
            player_center_y = player_world_y + 11
            # Posição do mouse (na tela)
            mouse_x, mouse_y = mouse.get_position()
            # Converta mouse para coordenada do mundo
            mouse_world_x = mouse_x - window.width // 2 + player_world_x
            mouse_world_y = mouse_y - window.height // 2 + player_world_y
            # Direção normalizada
            dx = mouse_world_x - player_center_x
            dy = mouse_world_y - player_center_y
            dist = math.hypot(dx, dy)
            if dist == 0:
                dist = 1
            dx /= dist
            dy /= dist
            speed = 800 #velocidad de cada disparo
            disparos.append({
                "sprite": shooting_sprite,
                "x": player_center_x - shooting_sprite.width / 2,
                "y": player_center_y - shooting_sprite.height / 2,
                "dx": dx,
                "dy": dy,
                "speed": speed
            })
            last_shot_time = current_time

    # Atualiza e desenha disparos
    to_remove = []
    for disparo in disparos:
        disparo["x"] += disparo["dx"] * disparo["speed"] * window.delta_time()
        disparo["y"] += disparo["dy"] * disparo["speed"] * window.delta_time()
        # Offset da câmera
        tela_x = disparo["x"] - player_world_x + window.width // 2
        tela_y = disparo["y"] - player_world_y + window.height // 2
        disparo["sprite"].set_position(tela_x, tela_y)
        disparo["sprite"].draw()
        # Remove se sair da tela do mundo (ajuste se quiser limites maiores)
        if (disparo["x"] < 0 or disparo["x"] > 4000 or
            disparo["y"] < 0 or disparo["y"] > 3000):
            to_remove.append(disparo)
    for disparo in to_remove:
        disparos.remove(disparo)

    return last_shot_time

player_world_x = 1000  # posição inicial no mapa
player_world_y = 1000

def mover_player(velocidade=200):
    global player_world_x, player_world_y, keyboard
    if keyboard.key_pressed("W") or keyboard.key_pressed("UP"):
        player_world_y -= velocidade * window.delta_time()
    if keyboard.key_pressed("S") or keyboard.key_pressed("DOWN"):
        player_world_y += velocidade * window.delta_time()
    if keyboard.key_pressed("A") or keyboard.key_pressed("LEFT"):
        player_world_x -= velocidade * window.delta_time()
    if keyboard.key_pressed("D") or keyboard.key_pressed("RIGHT"):
        player_world_x += velocidade * window.delta_time()

def get_player_world_pos():
    global player_world_x, player_world_y
    return player_world_x, player_world_y

def dash_funcionality():
    global player_world_x, player_world_y, player
    angle = player.angle  # Use o ângulo atual do player
    dash_distance = 200  # pixels (ajuste como quiser)
    # Calcula o deslocamento baseado no ângulo
    dx = math.cos(math.radians(angle))
    dy = -math.sin(math.radians(angle))
    player_world_x += dx * dash_distance
    player_world_y += dy * dash_distance