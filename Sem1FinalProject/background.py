"""
Controls scrolling background
for shark game

@author: Isabel Prado-Tucker
@version: 2023
"""
import pygame

class Background:
    # Constructor
    def __init__(self, cell_size):
        self.color = (51, 84, 163)  
        self.bg_x, self.bg_y = 0, 0
        self.speed = 4  
        self.cell_size = cell_size
        self.color = (68, 86, 189)

    # Update position based on mouse direction
    def update_position(self, direction_x, direction_y):
        self.bg_x += direction_x * self.speed
        self.bg_y += direction_y * self.speed

    # ChatGPT generated method (prompted for moving background grid)
    # Draw each cell in the background grid
    def draw(self, screen, grid):
        for cell in grid:
                cell_pos = (cell[0] - self.bg_x, cell[1] - self.bg_y)
                pygame.draw.rect(screen, (68, 86, 189), (cell_pos[0], cell_pos[1], self.cell_size, self.cell_size), 1)