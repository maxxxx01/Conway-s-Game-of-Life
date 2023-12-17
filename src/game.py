import argparse

import graphics
import logic

def preparation():
    parser = argparse.ArgumentParser(description = r"Watch the Conway's Game of Life taking shape.")
    parser.add_argument("-ww", "--width", type = int, help = "width of the window [min 640]")
    parser.add_argument("-wh", "--height", type = int, help = "height of the window [min 360]")
    parser.add_argument("-gr", "--rows", type = int, help = r"number of rows of the Conway's grid [max 100]")
    parser.add_argument("-gc", "--columns", type = int, help = r"number of columns of the Conway's grid [max 100]")
    args = parser.parse_args()
    
    window = graphics.Window((args.width if args.width else 720), (args.height if args.height else 480))
    
    grid = logic.Grid((args.rows if args.rows else 10), (args.columns if args.columns else 10))
    
    return window, grid

def play(window, grid):
    window.print_grid(grid)
    
    update = True
    updates = 0
    while (window.is_alive()):
        grid.update()
        if grid.is_equal_to_prev():
            update = False
        else:
            window.print_grid(grid)
            window.clear()
            updates += 1
    
    print("The grid has been updated " + str(updates) + " times.\n")