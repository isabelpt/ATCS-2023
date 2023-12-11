import pygame

class Background:
    def __init__(self, cell_size):
        self.color = (120, 138, 204)  # White color for the background
        self.bg_x, self.bg_y = 0, 0
        self.speed = 4  # Constant background speed
        self.cell_size = cell_size
        self.color = (68, 86, 189)

    def update_position(self, direction_x, direction_y):
        self.bg_x += direction_x * self.speed
        self.bg_y += direction_y * self.speed

    def draw(self, screen, grid):
        for cell in grid:
                cell_pos = (cell[0] - self.bg_x, cell[1] - self.bg_y)
                pygame.draw.rect(screen, (68, 86, 189), (cell_pos[0], cell_pos[1], self.cell_size, self.cell_size), 1)