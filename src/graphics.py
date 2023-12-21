import ctypes
import pygame

from logic import clamp, lclamp, uclamp

class Window:
    def __init__(self, width, height, rows, columns, background = 0, individual_color = (255, 255, 255), connection_color = (0, 0, 255)):
        width = clamp(width, 640, ctypes.windll.user32.GetSystemMetrics(0))
        height = clamp(height, 360, ctypes.windll.user32.GetSystemMetrics(1))
        self.cell_width = (width / columns)
        self.cell_cwidth = (self.cell_width / 2)
        self.cell_height = (height / rows)
        self.cell_cheight = (self.cell_height / 2)
        
        self.radius = (min(self.cell_width, self.cell_height) // 3)
        line_width = int(min(self.cell_width, self.cell_height) / 10)
        self.line_width = line_width if line_width >= 1 else 1
        
        self.background = background
        self.individual_color = individual_color
        self.connection_color = connection_color
        
        self.window = pygame.display.set_mode((width, height))
        self.window.fill(self.background)
        
        print("A " + str(width) + " x " + str(height) + " window has been created.")
    
    def get_position(self, i, j):
        return (((self.cell_width * j) + self.cell_cwidth), ((self.cell_height * i) + self.cell_cheight))
    
    def is_alive(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def draw_individuals(self, grid):
        for i in range(grid.get_rows()):
            for j in range(grid.get_columns()):
                if grid.is_alive(i, j):
                    pygame.draw.circle(self.window, self.individual_color, self.get_position(i, j), self.radius)
    
    def draw_connections(self, grid):
        for i in range(grid.get_rows()):
            for j in range(grid.get_columns()):
                if grid.is_alive(i, j):
                    for row in range(lclamp(i - 1, 0), uclamp(i + 2, grid.get_rows())):
                        for column in range(lclamp(j - 1, 0), uclamp(j + 2, grid.get_columns())):
                            if grid.is_alive(row, column) and ((i != row) or (j != column)):
                                pygame.draw.line(self.window, self.connection_color, self.get_position(i, j), self.get_position(row, column), self.line_width)
    
    def draw(self, grid, delay = 140):
        self.draw_connections(grid)
        self.draw_individuals(grid)
        
        pygame.display.update()
        pygame.time.wait(delay)
    
    def clear(self):
        self.window.fill(self.background)