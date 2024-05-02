import pygame

class AudioBar:
    def __init__(self, x, y, freq, color, width, max_height, min_decibel=-80, max_decibel=0):
        self.x, self.y, self.frequency, self.color = x, y, freq, color
        self.width, self.max_height = width, max_height
        self.height, self.min_decibel, self.max_decibel = 0, min_decibel, max_decibel
        self.decibel_height = (self.max_height)/(self.max_decibel - self.min_decibel)

    def update(self, change_time, decibel):
        desired_height = decibel * self.decibel_height + self.max_height
        self.height += ((desired_height - self.height)/0.1) * change_time
        self.height = max(min(self.max_height, self.height), 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y + self.max_height - self.height, self.width, self.height))