from config import window, mouse, keyboard, click
from Sprites import Sprites_Menu, Sprite_Score
import json
import pygame

#define as posições dos Sprite na janela de menu
def posições_Sprites_menu():
    background, play, score, mute, close = Sprites_Menu()
    background.set_position((window.width - background.width)/2, (window.height - background.height)/2)
    play.set_position((window.width - play.width)/2, 550)
    score.set_position((window.width - score.width)/2, 635)
    mute.set_position((window.width - mute.width)/2 - 80, 720)
    close.set_position((window.width - close.width)/2 + 85, 720)
    return background, play, score, mute, close

def gameloop_score(game_mode):
    score_background = Sprite_Score()
    score_background.set_position((window.width - score_background.width)/2, (window.height - score_background.height)/2)
    font = pygame.font.SysFont("arial", 28)
    try:
        with open("Score.json", "r", encoding="utf-8") as f:
            scores = json.load(f)
    except:
        scores = []
    while game_mode == 2:
        if keyboard.key_pressed("ESC"):
            return 0

        score_background.draw()
        # Mostra os 5 melhores
        for i, partida in enumerate(scores[:5]):
            texto = f"{i+1}. {partida['data_hora']} | Tempo: {partida['tempo_str']} | Kills: {partida['kills']}"
            img = font.render(texto, True, (255,255,255))
            window.screen.blit(img, (100, 150 + i*40))
        window.update()
        

    
    
def gameloop_menu(game_mode):
    background, play, score, mute, close = posições_Sprites_menu() #importa as variáveis da função posição_sprites_menu() para utilizar nesta função

    while game_mode == 0:

        if click(play):
            game_mode = 1
        elif click(score):
            game_mode = 2
        elif click(close):
            window.close()

        background.draw()
        play.draw()
        score.draw()
        mute.draw()
        close.draw()
        window.update()
    
    return game_mode



                    
                          