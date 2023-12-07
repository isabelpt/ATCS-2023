import pygame
import random

class Food:
    def __init__(self, screen_width, screen_height, num_food):
        self.color = (70, 90, 125)  # Red color for food
        self.size = 15
        self.food_list = []
        self.reveal_dist = 70
        self.generate_food(screen_width, screen_height, num_food)

    def generate_food(self, screen_width, screen_height, num_food):
        for _ in range(num_food):
            food_pos = (random.randint(-screen_width, 2 * screen_width),
                        random.randint(-screen_height, 2 * screen_height))
            self.food_list.append(food_pos)
    
    def update_reveal_dist(self, change):
        self.reveal_dist = max(10, self.reveal_dist - change)