import pygame
import random

class Food:
    def __init__(self, screen_width, screen_height, num_food):
        self.color = (255, 0, 0)  # Red color for food
        self.size = 8
        self.food_list = []
        self.generate_food(screen_width, screen_height, num_food)

    def generate_food(self, screen_width, screen_height, num_food):
        for _ in range(num_food):
            food_pos = (random.randint(-screen_width, 2 * screen_width),
                        random.randint(-screen_height, 2 * screen_height))
            self.food_list.append(food_pos)