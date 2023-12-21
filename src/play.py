from pygame import init

import game

init()

if __name__ == "__main__":
    print("BEGIN OF THE GAME\n")
    window, grid = game.preparation()
    game.play(window, grid)
    print("END OF THE GAME", end = "")