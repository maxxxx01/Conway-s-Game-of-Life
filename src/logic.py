import numpy

def clamp(num, lower, upper):
    return min(max(num, lower), upper)

def lclamp(num, lower):
    return max(num, lower)

def uclamp(num, upper):
    return min(num, upper)

class Grid:
    nf_info = {"neighbors": ["square", "plus", "hminus", "vminus", "tree"],
               "formulas": ["conway"]}
    
    def __init__(self, rows, columns, neighbors = "square", breadth = 1, formula = "conway"):
        self.rows = clamp(rows, 10, 200)
        self.columns = clamp(columns, 10, 200)
        
        self.grid = numpy.random.randint(2, size = (self.rows, self.columns))
        self.prev_grid = numpy.zeros_like(self.grid)
        
        self.neighbors_func = "self." + neighbors
        self.breadth = breadth
        self.formula = "self." + formula
        
        print("A " + str(self.rows) + " x " + str(self.columns) + " grid has been created.")
    
    def info(self, what = "all"):
        if ((what == "all") or (what == "neighbors")):
            print("The neighbors of each individual can be taken as:\n" + str(self.nf_info["neighbors"]))
        if ((what == "all") or (what == "formulas")):
            print("The formulas to determine the survival of each individual are:\n" + str(self.nf_info["formulas"]))
    
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
    
    def square(self, i, j):
        return numpy.concatenate((self.prev_grid[lclamp(i - self.breadth, 0) : i, lclamp(j - self.breadth, 0) : uclamp((j + self.breadth) + 1, self.columns)].flatten(), self.prev_grid[i, lclamp(j - self.breadth, 0) : j], self.prev_grid[i, (j + 1) : uclamp((j + self.breadth) + 1, self.columns)], self.prev_grid[(i + 1) : uclamp((i + self.breadth) + 1, self.rows), lclamp(j - self.breadth, 0) : uclamp((j + self.breadth) + 1, self.columns)].flatten()))
    
    def plus(self, i, j):
        return numpy.concatenate((self.prev_grid[lclamp(i - self.breadth, 0) : i, j], self.prev_grid[i, lclamp(j - self.breadth, 0) : j], self.prev_grid[i, (j + 1) : uclamp((j + self.breadth) + 1, self.columns)], self.prev_grid[(i + 1) : uclamp((i + self.breadth) + 1, self.rows), j]))
    
    def hminus(self, i, j):
        return numpy.concatenate((self.prev_grid[i, lclamp(j - self.breadth, 0) : j], self.prev_grid[i, (j + 1) : uclamp((j + self.breadth) + 1, self.columns)]))
    
    def vminus(self, i, j):
        return numpy.concatenate((self.prev_grid[lclamp(i - self.breadth, 0) : i, j], self.prev_grid[(i + 1) : uclamp((i + self.breadth) + 1, self.rows), j]))
    
    def tree(self, i, j):
        slices, n = [], 0
        for r_before in range(lclamp(i - self.breadth, 0), i):
            slices.append(self.grid[r_before, lclamp(j - n, 0) : uclamp((j + n) + 1, self.columns)])
            n += 1
        slices.append(self.grid[i, lclamp(j - self.breadth, 0) : j])
        slices.append(self.grid[i, (j + 1) : uclamp((j + self.breadth) + 1, self.columns)])
        slices.append(self.grid[(i + 1) : uclamp((i + self.breadth) + 1, self.rows), j])
        
        return numpy.concatenate(slices)
    
    def conway(self, neighbors, i, j):
        neighbors_sum = neighbors.sum()
        return 0 if ((neighbors_sum < 2) or (neighbors_sum > 3)) else (1 if (neighbors_sum == 3) else self.prev_grid[i, j])
    
    def update(self):
        self.prev_grid = numpy.copy(self.grid)
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid[i, j] = eval(self.formula)(eval(self.neighbors_func)(i, j), i, j)