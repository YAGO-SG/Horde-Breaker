from config import window
from Sprites import Sprites_enemy
from math import hypot
import random

def criar_inimigo(x, y, speed=5):
    sprite = Sprites_enemy()
    sprite.set_position(x, y)
    return {"sprite": sprite, "x": x, "y": y, "speed": speed}

def mover_e_desenhar_inimigos(enemies, player_world_x, player_world_y, player, disparos, kills, invencivel):
    to_remove_enemies = []
    to_remove_disparos = []
    player_hit = False

    for enemy in enemies:
        # Centro do player no mundo
        player_center_x = player_world_x
        player_center_y = player_world_y

        # Centro do inimigo no mundo
        enemy_center_x = enemy["x"] + enemy["sprite"].width / 2
        enemy_center_y = enemy["y"] + enemy["sprite"].height / 2

        # Direção normalizada até o player
        dx = player_center_x - enemy_center_x
        dy = player_center_y - enemy_center_y
        dist = hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist

        # Move o inimigo no mundo
        enemy["x"] += dx * enemy["speed"] * window.delta_time() * 500
        enemy["y"] += dy * enemy["speed"] * window.delta_time() * 500

        # Offset da câmera para desenhar na tela
        tela_x = enemy["x"] - player_world_x + window.width // 2
        tela_y = enemy["y"] - player_world_y + window.height // 2
        enemy["sprite"].set_position(tela_x, tela_y)
        enemy["sprite"].draw()

        # Checa colisão com player (no mundo)
        if not invencivel and abs(enemy["x"] - player_world_x) < player.width and abs(enemy["y"] - player_world_y) < player.height:
            to_remove_enemies.append(enemy)
            player_hit = True

        # Checa colisão com disparos (no mundo)
        for disparo in disparos:
            if abs(enemy["x"] - disparo["x"]) < enemy["sprite"].width and abs(enemy["y"] - disparo["y"]) < enemy["sprite"].height:
                to_remove_enemies.append(enemy)
                to_remove_disparos.append(disparo)
                kills += 1

    # Remove inimigos que colidiram
    for enemy in to_remove_enemies:
        if enemy in enemies:
            enemies.remove(enemy)
    # Remove disparos que colidiram
    for disparo in to_remove_disparos:
        if disparo in disparos:
            disparos.remove(disparo)
    return kills, player_hit

def spawn_inimigo_aleatorio():
    # Decide em qual borda spawnar: 0=topo, 1=baixo, 2=esquerda, 3=direita
    borda = random.randint(0, 3)
    raio = 500  # Aumente este valor para spawnar mais longe das bordas
    if borda == 0:  # Topo
        x = random.randint(0, window.width)
        y = -raio
    elif borda == 1:  # Baixo
        x = random.randint(0, window.width)
        y = window.height + raio * 3
    elif borda == 2:  # Esquerda
        x = -raio
        y = random.randint(0, window.height * 3)
    else:  # Direita
        x = window.width + raio * 4
        y = random.randint(0, window.height * 3)
    speed = random.uniform(0.05, 0.2)  # Velocidade aleatória
    return criar_inimigo(x, y, speed)