from config import window, keyboard
from Sprites import Sprites_game
from Player import init_player, default, update_player_rotation, shooting_funcionality, mover_player, get_player_world_pos, dash_funcionality
from inimigos import mover_e_desenhar_inimigos, spawn_inimigo_aleatorio
import pygame
from pplay.sprite import Sprite

def posições_sprites_heart():
    full_heart, heartless, mapa, game_over, yes_button, no_button = Sprites_game() #importa os Sprites do arquivo Sprites.py
    # define as posições dos Sprites
    for i, heart in enumerate(full_heart):
        heart.set_position( (window.width - heart.width) - (heart.width * i + 30),30)
    for l, heart2 in enumerate(heartless):
        heart2.set_position( (window.width - heart2.width) - (heart2.width * l + 30),30)
    mapa.set_position(0, 0)

    return full_heart, heartless, mapa, game_over, yes_button, no_button

def posições_sprites_map(mapa):
    # Pegue a posição do player no mundo
    player_world_x, player_world_y = get_player_world_pos()

    # Calcule o offset do mapa
    tela_x = -500 - player_world_x + window.width // 2
    tela_y = -900 - player_world_y + window.height // 2

    mapa.set_position(tela_x, tela_y)
    mapa.draw()

def gameloop_game(game_mode):
    player = init_player()

    pygame.init()# inserido para poder utilizar as funcionalidade do pygame
    pygame.font.init() #tem a função de importar a fontes disponiveis no pygame
    font = pygame.font.SysFont("arial", 32)#define a fonte utilizada nos texto da janela game

    last_shot_time = 0

    full_heart, heartless, mapa, game_over, yes_button, no_button  = posições_sprites_heart() #chama a função posições_Sprites_game() para utilizar suas variaveis dentro desta função
    #variáveis para determinar os valores aparecidos na HUD como a quantidade de eliminações, round atual e quantidade de dash's disponíveis
    kills = 0
    rounds = 1
    # funcionalidade de dano entre o player e os monstros
    vidas = 3
    invencivel = False
    invencivel_timer = 0
    piscando = False
    # funcionalidades do meu dash
    dash = 3
    dash_cooldown = 0.5  # 0.5 segundo entre dashes
    dash_recharge_time = 5.0  # 5 segundos para recarregar um dash
    last_dash_time = -dash_cooldown  # permite dash logo no início
    dash_recharge_queue = []  # lista de tempos em que cada dash foi usado
    #Meu relogio dentro do jogo
    start_time = pygame.time.get_ticks()

    #lista utilizada na função "shooting_funcionality", para não rezetar a cada loop
    disparos = []

    # configurações de spown dos inimigos
    enemies = []
    for _ in range(100):  # Spawna inimigos aleatórios
        enemies.append(spawn_inimigo_aleatorio())
    spawn_timer = 0
    spawn_interval = 0.2



    while game_mode == 1:
        window.set_background_color([108,100,20])
        current_time = pygame.time.get_ticks() / 1000
        posições_sprites_map(mapa)

        if keyboard.key_pressed("m"):
            vidas = 0

        if vidas <= 0:
            # Centraliza o sprite game_over
            game_over.set_position(
                (window.width - game_over.width) // 2,
                (window.height - game_over.height) // 6
            )
            
            save_option = font.render(f"você quer salvar as infomações desta partida?", True, (255, 255, 255))
            window.screen.blit(save_option, (window.width // 3, window.height // 1.5))

            yes_button.set_position((window.width - yes_button.width)/2.5, (window.height - yes_button.height)/1.2)
            no_button.set_position((window.width - no_button.width)/1.7, (window.height - no_button.height)/1.205)

            no_button.draw()
            yes_button.draw()
            game_over.draw()
            window.update()

            while True:
                if keyboard.key_pressed("ESC"):
                    return 0
                window.update()
            

        #lista com intuito de printar as tres vidas do personagem
        for k in range(3):
            heartless[k].draw()
        for heart in full_heart:
            heart.draw()

        player_world_x, player_world_y = get_player_world_pos()
        last_shot_time = shooting_funcionality(disparos, last_shot_time, current_time, player_world_x, player_world_y)
        kills, player_hit = mover_e_desenhar_inimigos(enemies, player_world_x, player_world_y, player, disparos, kills, invencivel)

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

        #funcionalidade do relogio
        elapsed_ms = pygame.time.get_ticks() - start_time
        elapsed_sec = int(elapsed_ms / 1000)
        minutes = elapsed_sec // 60
        seconds = elapsed_sec % 60


        #comando do pygame para configurar os textos na janela do game
        ellimination_count = font.render(f"kills {kills}", True, (255, 255, 255))
        round_count = font.render(f"round {rounds}", True, (255, 255, 255))
        dash_count = font.render(f"{dash}", True, (255, 255, 255))
        timer_text = font.render(f"{minutes:02d}:{seconds:02d}", True, (255, 255, 255))

        #imprimi os textos na tela do jogo
        window.screen.blit(ellimination_count, (20, 20))
        window.screen.blit(round_count, (20, (window.height - 60)))
        window.screen.blit(dash_count, (window.width/2 - 20, window.height/2 - 80))
        window.screen.blit(timer_text, (window.width // 2 - 40, 10))  # Centralizado no topo

        current_time = pygame.time.get_ticks() / 1000
        dash_recharge_queue = [t for t in dash_recharge_queue if current_time - t < dash_recharge_time]
        dash = 3 - len(dash_recharge_queue)

        # Dash ao apertar espaço
        if keyboard.key_pressed("SPACE"):
            if dash > 0 and current_time - last_dash_time >= dash_cooldown:
                dash_funcionality()
                last_dash_time = current_time
                dash_recharge_queue.append(current_time)

        # Spawna inimigos a cada intervalo
        if current_time - spawn_timer > spawn_interval:
            enemies.append(spawn_inimigo_aleatorio())
            spawn_timer = current_time

        mover_player()
        update_player_rotation()
        default(piscando)
        window.update()