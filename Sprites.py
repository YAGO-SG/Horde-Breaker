from pplay.sprite import Sprite

#Sprites da janela Menu
def Sprites_Menu(): 
    background = Sprite('Sprites/Menu/background.png')
    play = Sprite('Sprites/Menu/play.png')
    score = Sprite('Sprites/Menu/score.png')
    mute = Sprite('Sprites/Menu/mute.png')
    close = Sprite('Sprites/Menu/quit.png')
    return background, play, score, mute, close

#Spites da janela game
def Sprites_game():
    player = Sprite('Sprites/Game/player machinegun.gif')
    full_heart = [Sprite('Sprites/Game/HUD/full_heart.png') for _ in range(3)]
    heartless = [Sprite('Sprites/Game/HUD/heartless.png') for _ in range(3)]

    return player, full_heart, heartless
