import ctypes
import pygame

import logic

class Window:
    def __init__(self, width, height, background = 0):
        pygame.init()
        
        self.width = logic.clamp(width, 640, ctypes.windll.user32.GetSystemMetrics(0))
        self.height = logic.clamp(height, 360, ctypes.windll.user32.GetSystemMetrics(1))
        self.background = background
        self.window = pygame.display.set_mode((self.width, self.height))
        
        self.window.fill(self.background)
        
        print("A " + str(self.width) + " x " + str(self.height) + " window has been created.")
    
    def is_alive(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def print_grid(self, grid):
        for i in range(grid.get_rows()):
            for j in range(grid.get_columns()):
                pygame.draw.circle(self.window, (200, 0, 0), (j * 40, i * 40), 10) if (grid.get_element(i, j) == 1) else pygame.draw.circle(self.window, (0, 200, 150), (j * 40, i * 40), 10)
                pygame.display.update()
    
    def clear(self, delay = 200):
        self.window.fill(self.background)
        pygame.time.delay(delay)