from pplay.sprite import Sprite

#Sprites da janela Menu
def Sprites_Menu(): 
    background = Sprite('Sprites/Menu/background.png')
    play = Sprite('Sprites/Menu/play_2.png')
    score = Sprite('Sprites/Menu/scored_2.png')
    mute = Sprite('Sprites/Menu/mute_2.png')
    close = Sprite('Sprites/Menu/quit_2.png')
    return background, play, score, mute, close

def Sprite_Score():
    score_background = Sprite("Sprites/Menu/score_background.png")
    return score_background

#Spites da janela game
def Sprites_game():
    full_heart = [Sprite('Sprites/Game/HUD/full_heart.png') for _ in range(3)]
    heartless = [Sprite('Sprites/Game/HUD/heartless.png') for _ in range(3)]
    mapa = Sprite('Sprites/Game/mapa/mapa.png')
    game_over = Sprite('Sprites/Game/HUD/game_over.png')
    yes_button = Sprite('Sprites/Game/HUD/yes_button.png')
    no_button = Sprite('Sprites/Game/HUD/no_button.png')

    return full_heart, heartless, mapa, game_over, yes_button, no_button

def Sprites_jogador():
    player = Sprite('Sprites/Game/player.png')
    shooting = Sprite('Sprites/Game/small shooting.png')
    
    return player, shooting

def Sprites_enemy():
    enemy = Sprite('Sprites/Game/inimigos/inimigo_default.png')

    return enemy