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
