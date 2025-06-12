from menu import gameloop_menu
from config import window
from game import gameloop_game

game_mode = 0


while True:

    if game_mode == 0: #modo Menu
        game_mode = gameloop_menu(game_mode)
    elif game_mode == 1: #modo Game
        gameloop_game(game_mode)
        