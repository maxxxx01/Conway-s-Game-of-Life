import numpy

class Grid:
    def __init__(self, rows, columns):
        self.rows = clamp(rows, 10, 100)
        self.columns = clamp(columns, 10, 100)
        
        self.grid = numpy.random.randint(2, size = (self.rows, self.columns))
        self.prev_grid = numpy.zeros_like(self.grid)
        
        print("A " + str(self.rows) + " x " + str(self.columns) + " grid has been created.")
    
    def get_rows(self):
        return self.rows
    
    def get_columns(self):
        return self.columns
    
    def get_num_alives(self):
        return numpy.count_nonzero(self.grid == 1)
    
    def is_equal(self):
        return numpy.array_equal(self.grid, self.prev_grid)
    
    def is_alive(self, i, j):
        return (self.grid[i, j] == 1)
    
    def square_sum(self, i, j):
        return ((self.prev_grid[lclamp(i - 1, 0) : uclamp(i + 2, self.rows), lclamp(j - 1, 0) : uclamp(j + 2, self.columns)].sum()) - self.prev_grid[i, j])
    
    def new_state(self, i, j):
        block_sum = self.square_sum(i, j)
        return 0 if ((block_sum < 2) or (block_sum > 3)) else (1 if (block_sum == 3) else self.prev_grid[i, j])
    
    def update(self):
        self.prev_grid = numpy.copy(self.grid)
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid[i, j] = self.new_state(i, j)

def clamp(num, lower, upper):
    return min(max(num, lower), upper)

def lclamp(num, lower):
    return max(num, lower)

def uclamp(num, upper):
    return min(num, upper)