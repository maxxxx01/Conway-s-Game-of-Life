import argparse

import graphics
import logic

def preparation():
    parser = argparse.ArgumentParser(description = r"Watch the Conway's Game of Life taking shape.")
    parser.add_argument("-ww", "--width", type = int, help = "width of the window [min 640]")
    parser.add_argument("-wh", "--height", type = int, help = "height of the window [min 360]")
    parser.add_argument("-gr", "--rows", type = int, help = r"number of rows of the Conway's grid [max 200]")
    parser.add_argument("-gc", "--columns", type = int, help = r"number of columns of the Conway's grid [max 200]")
    args = parser.parse_args()
    
    grid = logic.Grid((args.rows if args.rows else 20), (args.columns if args.columns else 20))
    
    window = graphics.Window((args.width if args.width else 1080), (args.height if args.height else 640), grid.get_rows(), grid.get_columns())
    
    return window, grid

def play(window, grid):
    window.draw(grid, how = "classic")
    print("Number of individuals = " + str(grid.get_num_alives()))
    
    update, it = True, 0
    while (window.is_alive()):
        if update:
            grid.update()
            if not grid.is_equal():
                window.clear()
                window.draw(grid, how = "classic")
                print("Number of individuals = " + str(grid.get_num_alives()))
                it += 1
            else:
                update = False
    
    print("The grid has been updated " + str(it) + " times.\n")