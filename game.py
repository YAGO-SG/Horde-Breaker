from config import window, keyboard, mouse, click
from Sprites import Sprites_game
from Player import init_player, default, update_player_rotation, shooting_funcionality, mover_player, get_player_world_pos, dash_funcionality
import Player
from inimigos import mover_e_desenhar_inimigos, spawn_inimigo_aleatorio
import pygame
from pplay.sprite import Sprite
import json
from datetime import datetime
import random

def posições_sprites_heart():
    full_heart, heartless, mapa, game_over, yes_button, no_button, furia, round_2, round_3 = Sprites_game() #importa os Sprites do arquivo Sprites.py
    # define as posições dos Sprites
    for i, heart in enumerate(full_heart):
        heart.set_position( (window.width - heart.width) - (heart.width * i + 30),30)
    for l, heart2 in enumerate(heartless):
        heart2.set_position( (window.width - heart2.width) - (heart2.width * l + 30),30)
    mapa.set_position(0, 0)

    return full_heart, heartless, mapa, game_over, yes_button, no_button, furia, round_2, round_3

def posições_sprites_map(mapa):
    # Pegue a posição do player no mundo
    player_world_x, player_world_y = get_player_world_pos()

    # Calcule o offset do mapa
    tela_x = -500 - player_world_x + window.width // 2
    tela_y = -900 - player_world_y + window.height // 2

    mapa.set_position(tela_x, tela_y)
    mapa.draw()

def gameloop_game(game_mode):
    import Player
    player = init_player()
    Player.player_world_x = 1000
    Player.player_world_y = 1000

    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("arial", 32)

    last_shot_time = 0

    full_heart, heartless, mapa, game_over, yes_button, no_button, furia, round_2, round_3 = posições_sprites_heart()
    start_time = pygame.time.get_ticks()
    disparos = []
    enemies = []
    for _ in range(100):
        enemies.append(spawn_inimigo_aleatorio())
    spawn_timer = 0
    spawn_interval = 0.2

    furia_sprite_time = 3
    furia_duration = 20
    furia_sprite_start = None
    furia_state_start = None
    furia_displayed = False

    rounds = 1
    round_state = "normal"
    round_start_time = start_time / 1000
    show_round_sprite = False
    round_sprite_timer = 0

    kills = 0
    vidas = 35555555
    invencivel = False
    invencivel_timer = 0
    piscando = False

    dash = 3
    dash_cooldown = 0.5
    dash_recharge_time = 5.0
    last_dash_time = -dash_cooldown
    dash_recharge_queue = []

    while game_mode == 1:
        window.set_background_color([108,100,20])
        current_time = pygame.time.get_ticks() / 1000
        posições_sprites_map(mapa)

        if keyboard.key_pressed("ESC"):
            return 0

        # Game Over
        if vidas <= 0:
            game_over.set_position(
                (window.width - game_over.width) // 2,
                (window.height - game_over.height) // 6
            )
            save_option = font.render("você quer salvar as infomações desta partida?", True, (255, 255, 255))
            window.screen.blit(save_option, (window.width // 3, window.height // 1.5))
            yes_button.set_position((window.width - yes_button.width)/2.5, (window.height - yes_button.height)/1.2)
            no_button.set_position((window.width - no_button.width)/1.7, (window.height - no_button.height)/1.205)
            no_button.draw()
            yes_button.draw()
            game_over.draw()
            window.update()
            while True:
                if click(yes_button):
                    elapsed_ms = pygame.time.get_ticks() - start_time
                    elapsed_sec = int(elapsed_ms / 1000)
                    minutes = elapsed_sec // 60
                    seconds = elapsed_sec % 60
                    tempo_str = f"{minutes:02d}:{seconds:02d}"
                    now = datetime.now()
                    data_hora = now.strftime("%d/%m/%Y %H:%M:%S")
                    partida = {
                        "data_hora": data_hora,
                        "tempo": elapsed_sec,
                        "tempo_str": tempo_str,
                        "kills": kills
                    }
                    try:
                        with open("Score.json", "r", encoding="utf-8") as f:
                            scores = json.load(f)
                    except:
                        scores = []
                    scores.append(partida)
                    scores.sort(key=lambda x: x["tempo"], reverse=True)
                    with open("Score.json", "w", encoding="utf-8") as f:
                        json.dump(scores, f, indent=4, ensure_ascii=False)
                    return 0
                if click(no_button):
                    return 0
                window.update()

        # HUD de vidas
        for k in range(3):
            heartless[k].draw()
        for heart in full_heart:
            heart.draw()

        player_world_x, player_world_y = get_player_world_pos()
        last_shot_time = shooting_funcionality(disparos, last_shot_time, current_time, player_world_x, player_world_y)
        kills, player_hit, vida_perdida = mover_e_desenhar_inimigos(enemies, player_world_x, player_world_y, player, disparos, kills, invencivel)




        # Controle de rounds e fúria
        elapsed_round_sec = current_time - round_start_time

        # Exibe Sprite do round quando muda de round
        if show_round_sprite:
            if rounds == 2:
                round_2.set_position((window.width - round_2.width)//2, (window.height - round_2.height)//2)
                round_2.draw()
            elif rounds == 3:
                round_3.set_position((window.width - round_3.width)//2, (window.height - round_3.height)//2)
                round_3.draw()
            window.update()
            if current_time - round_sprite_timer >= 3:
                show_round_sprite = False
            else:
                continue

        # ROUND 1: Fúria após 40s
        if rounds == 1:
            if round_state == "normal" and elapsed_round_sec >= 40:
                round_state = "furia"
                enemies.clear()
                furia_displayed = True
                furia_sprite_start = current_time
                furia_state_start = current_time
            if round_state == "furia":
                # Mostra Sprite "furia" por 3 segundos
                if furia_displayed:
                    furia.set_position((window.width - furia.width)//2, (window.height - furia.height)//2)
                    furia.draw()
                    window.update()
                    if current_time - furia_sprite_start >= furia_sprite_time:
                        furia_displayed = False
                # Após 20 segundos, termina a fúria e inicia round 2
                if current_time - furia_state_start >= furia_duration:
                    rounds = 2
                    round_state = "normal"
                    round_start_time = current_time
                    show_round_sprite = True
                    round_sprite_timer = current_time
                     # Limpa e recria os inimigos ao mudar de round
                    enemies.clear()
                    for _ in range(100):
                        enemies.append(spawn_inimigo_aleatorio())
                # Durante a fúria, não spawna inimigos
                if furia_displayed:
                    continue
            # Spawna inimigos normais
            spawn_interval = 0.2
            enemy_speed_multiplier = 1.0
            if current_time - spawn_timer > spawn_interval:
                tipo = "explotion_monster" if elapsed_round_sec > 30 else "normal"
                enemies.append(spawn_inimigo_aleatorio(tipo=tipo, speed_multiplier=enemy_speed_multiplier))
                spawn_timer = current_time

        # ROUND 2: Fúria após 40s
        elif rounds == 2:
            if round_state == "normal" and elapsed_round_sec >= 40:
                round_state = "furia"
                enemies.clear()
                furia_displayed = True
                furia_sprite_start = current_time
                furia_state_start = current_time
            if round_state == "furia":
                if furia_displayed:
                    furia.set_position((window.width - furia.width)//2, (window.height - furia.height)//2)
                    furia.draw()
                    window.update()
                    if current_time - furia_sprite_start >= furia_sprite_time:
                        furia_displayed = False
                if current_time - furia_state_start >= furia_duration:
                    rounds = 3
                    round_state = "normal"
                    round_start_time = current_time
                    show_round_sprite = True
                    round_sprite_timer = current_time
                    # Limpa e recria os inimigos ao mudar de round
                    enemies.clear()
                    for _ in range(100):
                        enemies.append(spawn_inimigo_aleatorio())
                # Durante a fúria, spawna inimigos mais rápidos e em maior quantidade
                spawn_interval = 0.1
                enemy_speed_multiplier = 2.0
                if current_time - spawn_timer > spawn_interval:
                    tipo = "explotion_monster" if random.random() < 0.5 else "normal"
                    enemies.append(spawn_inimigo_aleatorio(tipo=tipo, speed_multiplier=enemy_speed_multiplier))
                    spawn_timer = current_time
                if furia_displayed:
                    continue
            # Spawna ambos os tipos de inimigos normalmente
            spawn_interval = 0.2
            enemy_speed_multiplier = 1.0
            if current_time - spawn_timer > spawn_interval:
                tipo = "explotion_monster" if random.random() < 0.5 else "normal"
                enemies.append(spawn_inimigo_aleatorio(tipo=tipo, speed_multiplier=enemy_speed_multiplier))
                spawn_timer = current_time

        # ROUND 3: apenas inimigos normais e explosivos, sem fúria
        elif rounds == 3:
            spawn_interval = 0.2
            enemy_speed_multiplier = 1.0
            if current_time - spawn_timer > spawn_interval:
                tipo = "explotion_monster" if random.random() < 0.5 else "normal"
                enemies.append(spawn_inimigo_aleatorio(tipo=tipo, speed_multiplier=enemy_speed_multiplier))
                spawn_timer = current_time





        # Controle de vida/invencibilidade
        if vida_perdida and not invencivel and vidas > 0:
            vidas -= 1
            invencivel = True
            invencivel_timer = current_time

        if player_hit and not invencivel and vidas > 0:
            vidas -= 1
            if full_heart:
                full_heart.pop()
            invencivel = True
            invencivel_timer = current_time
            piscando = True

        # Invencibilidade por 2 segundos
        if invencivel:
            if current_time - invencivel_timer >= 2:
                invencivel = False
                piscando = False

        # HUD e textos
        elapsed_ms = pygame.time.get_ticks() - start_time
        elapsed_sec = int(elapsed_ms / 1000)
        minutes = elapsed_sec // 60
        seconds = elapsed_sec % 60

        ellimination_count = font.render(f"kills {kills}", True, (255, 255, 255))
        round_count = font.render(f"round {rounds}", True, (255, 255, 255))
        dash_count = font.render(f"{dash}", True, (255, 255, 255))
        timer_text = font.render(f"{minutes:02d}:{seconds:02d}", True, (255, 255, 255))

        window.screen.blit(ellimination_count, (20, 20))
        window.screen.blit(round_count, (20, (window.height - 60)))
        window.screen.blit(dash_count, (window.width/2 - 20, window.height/2 - 80))
        window.screen.blit(timer_text, (window.width // 2 - 40, 10))

        dash_recharge_queue = [t for t in dash_recharge_queue if current_time - t < dash_recharge_time]
        dash = 3 - len(dash_recharge_queue)

        # Dash ao apertar espaço
        if keyboard.key_pressed("SPACE"):
            if dash > 0 and current_time - last_dash_time >= dash_cooldown:
                dash_funcionality()
                last_dash_time = current_time
                dash_recharge_queue.append(current_time)

        mover_player()
        update_player_rotation()
        default(piscando)
        window.update()