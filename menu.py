from config import window, mouse, keyboard, click
from Sprites import Sprites_Menu

#define as posições dos Sprite na janela de menu
def posições_Sprites_menu():
    background, play, score, mute, close = Sprites_Menu()
    background.set_position((window.width - background.width)/2, (window.height - background.height)/2)
    play.set_position(window.width - play.width - 50, 190)
    score.set_position(window.width - score.width - 50, 240)
    mute.set_position(window.width - mute.width - 50, 290)
    close.set_position(window.width - close.width - 50, 350)
    return background, play, score, mute, close


#função usada para interação do mouse com sprite

    
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



                    
                          