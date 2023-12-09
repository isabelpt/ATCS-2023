import pygame
import random
from fsm import FSM

class Food:
    def __init__(self, screen_width, screen_height, num_food):
        self.color = (70, 90, 125)  # Red color for food
        self.size = 15
        self.food_list = []
        self.reveal_dist = 70
        self.generate_food(screen_width, screen_height, num_food)

        self.fsm = FSM(0)
        self.init_fsm()

        self.states = {0, 1}

    def generate_food(self, screen_width, screen_height, num_food):
        for _ in range(num_food):
            food_pos = (random.randint(-screen_width, 2 * screen_width),
                        random.randint(-screen_height, 2 * screen_height))
            self.food_list.append(food_pos)
    
    def init_fsm(self):
        # self.fsm.add_transition(" ", 0, self., "S")
        pass
    
    def update_reveal_dist(self, change):
        self.reveal_dist = max(10, self.reveal_dist - change)