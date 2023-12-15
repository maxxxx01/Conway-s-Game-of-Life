import argparse
import ctypes
import numpy as np
import pygame as pg

def window_init(width = 700, height = 550):
    pg.init()
    
    # Check wether the width is acceptable (not None & >= 400 & <= YourSystemsWidth); if not, use the optimized width (700)
    # GetSystemMetrics(0) get the width of your system, while GetSystemMetrics(1) get its height
    wh = width if (width and (width >= 400) and (width <= ctypes.windll.user32.GetSystemMetrics(0))) else 700
    # Same check, but for the height
    ht = height if (height and (height >= 400) and (height <= ctypes.windll.user32.GetSystemMetrics(1))) else 550
    return pg.display.set_mode((wh, ht))

def make_grid(n_rows = 10, n_columns = 10):
    # Check if the numbers of rows and columns are between the limits [3 - 100]
    d1 = n_rows if (n_rows and (n_rows >= 3) and (n_rows <= 100)) else 10
    d2 = n_columns if (n_columns and (n_columns >= 3) and (n_columns <= 100)) else 10
    return np.random.randint(2, size = (d1, d2))

def get_square(grid, ni, nj):
    i1 = ni if ((ni - 1) < 0) else (ni - 1)
    i2 = (ni + 1) if ((ni + 1) == grid.shape[0]) else (ni + 2)
    j1 = nj if ((nj - 1) < 0) else (nj - 1)
    j2 = (nj + 1) if ((nj + 1) == grid.shape[1]) else (nj + 2)
    return grid[i1 : i2, j1 : j2]

def update_state(grid, ni, nj):
    block_sum = get_square(grid, ni, nj).sum() - grid[ni, nj]
    grid[ni, nj] = 0 if ((block_sum < 2) or (block_sum > 3)) else (1 if (block_sum == 3) else grid[ni, nj])

def update_grid(grid):
    old_grid = np.empty((grid.shape[0], grid.shape[1]), dtype = int)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            old_grid[i, j] = grid[i, j]
            update_state(grid, i, j)
    return old_grid

def print_grid(grid, win):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            pg.draw.circle(win, (200, 0, 0), (i * 40, j * 40), 10) if (grid[i, j] == 1) else pg.draw.circle(win, (0, 200, 150), (i * 40, j * 40), 10)
            pg.display.update()

def clear_window(win, delay = 500):
    win.fill(0)
    pg.time.delay(delay)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = r"Watch the Conway's Game of Life taking shape.")
    parser.add_argument("-ww", "--win_width", type = int, help = "width of the window")
    parser.add_argument("-wh", "--win_height", type = int, help = "height of the window")
    parser.add_argument("-gr", "--rows", type = int, help = r"number of rows of the Conway's grid")
    parser.add_argument("-gc", "--columns", type = int, help = r"number of columns of the Conway's grid")
    args = parser.parse_args()
    #print(args)
    
    win = window_init(args.win_width, args.win_height)
    
    grid = make_grid(args.rows, args.columns)
    print_grid(grid, win)
    
    run, freeze = True, False
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        
        if not freeze:
            old_grid = update_grid(grid)
            if not np.array_equal(old_grid, grid):
                print_grid(grid, win)
                clear_window(win)
            else:
                freeze = True