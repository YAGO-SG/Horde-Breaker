from config import window, mouse
from Sprites import Sprites_game
import pygame
import math

def posições_sprites_game():
    player, full_heart, heartless = Sprites_game() #importa os Sprites do arquivo Sprites.py
    # define as posições dos Sprites
    player.set_position((window.width - player.width)/2, (window.height - player.height)/2)
    for i, heart in enumerate(full_heart):
        heart.set_position( (window.width - heart.width) - (heart.width * i + 30),30)
    for l, heart2 in enumerate(heartless):
        heart2.set_position( (window.width - heart2.width) - (heart2.width * l + 30),30)

    return player, full_heart, heartless

def gameloop_game(game_mode):
    player, full_heart, heartless = posições_sprites_game() #chama a função posições_Sprites_game() para utilizar suas variaveis dentro desta função

    pygame.init()# inserido para poder utilizar as funcionalidade do pygame
    pygame.font.init() #tem a função de importar a fontes disponiveis no pygame
    font = pygame.font.SysFont("arial", 32)#define a fonte utilizada nos texto da janela game

    #variáveis para determinar os valores aparecidos na HUD como a quantidade de eliminações, round atual e quantidade de dash's disponíveis
    kills = 0
    rounds = 1
    dash = 3

   

    while game_mode == 1:
        window.set_background_color([0,70,0])

        #comando do pygame para configurar os textos na janela do game
        ellimination_count = font.render(f"kills {kills}", True, (255, 255, 255))
        round_count = font.render(f"round {rounds}", True, (255, 255, 255))
        dash_count = font. render(f"{dash}", True, (255, 255, 255))

        #imprimi os textos na tela do jogo
        window.screen.blit(ellimination_count, (20, 20))
        window.screen.blit(round_count, (20, (window.height - 60)))
        window.screen.blit(dash_count, (window.width/2 - 20, window.height/2 - 80))

        #lista com intuito de printar as tres vidas do personagem
        for k in range(3):
            heartless[k].draw()
        for i in range(3):
            full_heart[i].draw()
        player.draw()
        window.update()