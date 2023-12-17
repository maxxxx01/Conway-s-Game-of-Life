import numpy

class Grid:
    def __init__(self, rows, columns):
        self.rows = clamp(rows, 1, 100)
        self.columns = clamp(columns, 1, 100)
        self.init_grid = numpy.random.randint(2, size = (self.rows, self.columns))
        self.grid = numpy.copy(self.init_grid)
        self.prev_grid = None
        
        print("A " + str(self.rows) + " x " + str(self.columns) + " grid has been created.")
    
    def get_rows(self):
        return self.rows
    
    def get_columns(self):
        return self.columns
    
    def get_element(self, i, j):
        return self.grid[i, j]
    
    def is_equal_to_prev(self):
        return numpy.array_equal(self.grid, self.prev_grid)
    
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

def clamp(num, lower_limit, upper_limit):
    return min(max(num, lower_limit), upper_limit)

def lclamp(num, lower_limit):
    return max(num, lower_limit)

def uclamp(num, upper_limit):
    return min(num, upper_limit)