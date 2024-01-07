import numpy

def clamp(num, lower, upper):
    return min(max(num, lower), upper)

def lclamp(num, lower):
    return max(num, lower)

def uclamp(num, upper):
    return min(num, upper)

class Grid:
    nf_info = {"neighbors": ["square", "utriangle", "dtriangle", "ltriangle", "rtriangle", "lparallelogram", "rparallelogram",
               "plus", "hminus", "vminus", "tree"],
               "formulas": ["conway"]}
    
    rlower, rupper = 10, 200
    clower, cupper = 10, 200
    
    def __init__(self, rows, columns, neighbors = "square", breadth = 1, formula = "conway"):
        self.grid = numpy.random.randint(2, size = (clamp(rows, self.rlower, self.rupper), clamp(columns, self.clower, self.cupper)))
        self.prev_grid = numpy.zeros_like(self.grid)
        
        self.neighbors = "self." + neighbors
        self.breadth = breadth
        self.formula = "self." + formula
        
        print("A " + str(self.grid.shape[0]) + " x " + str(self.grid.shape[1]) + " grid has been created.")
    
    def info(self, what = "all"):
        if (what == "all"):
            print("The neighbors of each individual can be taken as:\n" + str(self.nf_info["neighbors"]))
            print("The formulas to determine the survival of each individual are:\n" + str(self.nf_info["formulas"]))
        elif (what == "neighbors"):
            print("The neighbors of each individual can be taken as:\n" + str(self.nf_info["neighbors"]))
        elif (what == "formulas"):
            print("The formulas to determine the survival of each individual are:\n" + str(self.nf_info["formulas"]))
    
    def get_rows(self):
        return self.grid.shape[0]
    
    def get_columns(self):
        return self.grid.shape[1]
    
    def get_num_alives(self):
        return numpy.count_nonzero(self.grid == 1)
    
    def is_equal(self):
        return numpy.array_equal(self.grid, self.prev_grid)
    
    def is_alive(self, i, j):
        return (self.grid[i, j] == 1)
    
    def square(self, i, j):
        return numpy.concatenate((self.prev_grid[lclamp(i - self.breadth, 0) : i, lclamp(j - self.breadth, 0) : uclamp((j + self.breadth) + 1, self.get_columns())].flatten(), self.prev_grid[i, lclamp(j - self.breadth, 0) : j], self.prev_grid[i, (j + 1) : uclamp((j + self.breadth) + 1, self.get_columns())], self.prev_grid[(i + 1) : uclamp((i + self.breadth) + 1, self.get_rows()), lclamp(j - self.breadth, 0) : uclamp((j + self.breadth) + 1, self.get_columns())].flatten()))
    
    def utriangle(self, i, j):
        slices, n = [], (self.breadth - (i - lclamp(i - self.breadth, 0)))
        for r in range(lclamp(i - self.breadth, 0), i):
            slices.append(self.prev_grid[r, lclamp(j - n, 0) : uclamp((j + n) + 1, self.get_columns())])
            n += 1
        slices.append(self.prev_grid[i, lclamp(j - self.breadth, 0) : j])
        slices.append(self.prev_grid[i, (j + 1) : uclamp((j + self.breadth) + 1, self.get_columns())])
        
        return numpy.concatenate(slices)
    
    def dtriangle(self, i, j):
        slices = [self.prev_grid[i, lclamp(j - self.breadth, 0) : j]]
        slices.append(self.prev_grid[i, (j + 1) : uclamp((j + self.breadth) + 1, self.get_columns())])
        n = (self.breadth - 1)
        for r in range((i + 1), uclamp((i + self.breadth) + 1, self.get_rows())):
            slices.append(self.prev_grid[r, lclamp(j - n, 0) : uclamp((j + n) + 1, self.get_columns())])
            n -= 1
        
        return numpy.concatenate(slices)
    
    def ltriangle(self, i, j):
        slices, n = [], (self.breadth - (j - lclamp(j - self.breadth, 0)))
        for c in range(lclamp(j - self.breadth, 0), j):
            slices.append(self.prev_grid[lclamp(i - n, 0) : uclamp((i + n) + 1, self.get_rows()), c])
            n += 1
        slices.append(self.prev_grid[lclamp(i - self.breadth, 0) : i, j])
        slices.append(self.prev_grid[(i + 1) : uclamp((i + self.breadth) + 1, self.get_rows()), j])
        
        return numpy.concatenate(slices)
    
    def rtriangle(self, i, j):
        slices = [self.prev_grid[lclamp(i - self.breadth, 0) : i, j]]
        slices.append(self.prev_grid[(i + 1) : uclamp((i + self.breadth) + 1, self.get_rows()), j])
        n = (self.breadth - 1)
        for c in range((j + 1), uclamp((j + self.breadth) + 1, self.get_columns())):
            slices.append(self.prev_grid[lclamp(i - n, 0) : uclamp((i + n) + 1, self.get_rows()), c])
            n -= 1
        
        return numpy.concatenate(slices)
    
    def lparallelogram(self, i, j):
        slices, n = [], (i - lclamp(i - self.breadth, 0))
        for r in range(lclamp(i - self.breadth, 0), i):
            slices.append(self.prev_grid[r, lclamp(j - self.breadth - n, 0) : uclamp((j + self.breadth - n) + 1, self.get_columns())])
            n -= 1
        slices.append(self.prev_grid[i, lclamp(j - self.breadth, 0) : j])
        slices.append(self.prev_grid[i, (j + 1) : uclamp((j + self.breadth) + 1, self.get_columns())])
        n -= 1
        for r in range((i + 1), uclamp((i + self.breadth) + 1, self.get_rows())):
            slices.append(self.prev_grid[r, lclamp(j - self.breadth - n, 0) : uclamp((j + self.breadth - n) + 1, self.get_columns())])
            n -= 1
        
        return numpy.concatenate(slices)
    
    def rparallelogram(self, i, j):
        slices, n = [], (i - lclamp(i - self.breadth, 0))
        for r in range(lclamp(i - self.breadth, 0), i):
            slices.append(self.prev_grid[r, lclamp(j - self.breadth + n, 0) : uclamp((j + self.breadth + n) + 1, self.get_columns())])
            n -= 1
        slices.append(self.prev_grid[i, lclamp(j - self.breadth, 0) : j])
        slices.append(self.prev_grid[i, (j + 1) : uclamp((j + self.breadth) + 1, self.get_columns())])
        n -= 1
        for r in range((i + 1), uclamp((i + self.breadth) + 1, self.get_rows())):
            slices.append(self.prev_grid[r, lclamp(j - self.breadth + n, 0) : uclamp((j + self.breadth + n) + 1, self.get_columns())])
            n -= 1
        
        return numpy.concatenate(slices)
    
    def plus(self, i, j):
        return numpy.concatenate((self.prev_grid[lclamp(i - self.breadth, 0) : i, j], self.prev_grid[i, lclamp(j - self.breadth, 0) : j], self.prev_grid[i, (j + 1) : uclamp((j + self.breadth) + 1, self.get_columns())], self.prev_grid[(i + 1) : uclamp((i + self.breadth) + 1, self.get_rows()), j]))
    
    def hminus(self, i, j):
        return numpy.concatenate((self.prev_grid[i, lclamp(j - self.breadth, 0) : j], self.prev_grid[i, (j + 1) : uclamp((j + self.breadth) + 1, self.get_columns())]))
    
    def vminus(self, i, j):
        return numpy.concatenate((self.prev_grid[lclamp(i - self.breadth, 0) : i, j], self.prev_grid[(i + 1) : uclamp((i + self.breadth) + 1, self.get_rows()), j]))
    
    def tree(self, i, j):
        slices, n = [], (self.breadth - (i - lclamp(i - self.breadth, 0)))
        for r in range(lclamp(i - self.breadth, 0), i):
            slices.append(self.prev_grid[r, lclamp(j - n, 0) : uclamp((j + n) + 1, self.get_columns())])
            n += 1
        slices.append(self.prev_grid[i, lclamp(j - self.breadth, 0) : j])
        slices.append(self.prev_grid[i, (j + 1) : uclamp((j + self.breadth) + 1, self.get_columns())])
        slices.append(self.prev_grid[(i + 1) : uclamp((i + self.breadth) + 1, self.get_rows()), j])
        
        return numpy.concatenate(slices)
    
    def conway(self, neighbors, i, j):
        neighbors_sum = neighbors.sum()
        return 0 if ((neighbors_sum < 2) or (neighbors_sum > 3)) else (1 if (neighbors_sum == 3) else self.prev_grid[i, j])
    
    def update(self):
        self.prev_grid = numpy.copy(self.grid)
        for i in range(self.get_rows()):
            for j in range(self.get_columns()):
                self.grid[i, j] = eval(self.formula)(eval(self.neighbors)(i, j), i, j)