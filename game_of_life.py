import numpy as np

def make_grid(n = 10, m = 10):
    return np.random.randint(2, size = (n, m))

def neighbors(grid, ni, nj):
    i1 = ni if ((ni - 1) < 0) else (ni - 1)
    i2 = (ni + 1) if ((ni + 1) == grid.shape[0]) else (ni + 2)
    j1 = nj if ((nj - 1) < 0) else (nj - 1)
    j2 = (nj + 1) if ((nj + 1) == grid.shape[1]) else (nj + 2)
    return grid[i1 : i2, j1 : j2]

def update_state(grid, ni, nj):
    block_sum = neighbors(grid, ni, nj).sum() - grid[ni, nj]
    grid[ni, nj] = 0 if ((block_sum < 2) or (block_sum > 3)) else (1 if (block_sum == 3) else grid[ni, nj])

def update_grid(grid):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            update_state(grid, i, j)

if __name__ == "__main__":
    grid = make_grid(10, 10)
    print(grid)
    print()

    for i in range(10):
        update_grid(grid)
        print(grid)
        print()