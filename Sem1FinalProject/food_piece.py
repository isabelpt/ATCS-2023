import pygame
import random
from fsm import FSM

class Food_Piece:
    def __init__(self, screen_width, screen_height, size, reveal_dist, default_img, reveal_img):
        self.DEFAULT, self.ACTUAL = 0, 1
        self.CLOSE, self.FAR = 0, 1
        self.color = (70, 90, 125)
        self.size = size
        self.reveal_dist = reveal_dist
        # self.default_img = 
        self.food_pos = (random.randint(-screen_width, 2 * screen_width),
                        random.randint(-screen_height, 2 * screen_height))
        self.default_img = default_img
        self.reveal_img = reveal_img
        self.img = self.default_img
       
        self.fsm = FSM(self.DEFAULT)
        self.init_fsm()
    
    def init_fsm(self):
        self.fsm.add_transition(self.CLOSE, self.DEFAULT, self.reveal, self.ACTUAL)
        self.fsm.add_transition(self.CLOSE, self.ACTUAL, self.reveal, self.ACTUAL)
        self.fsm.add_transition(self.FAR, self.ACTUAL, self.conceal, self.DEFAULT)
        self.fsm.add_transition(self.FAR, self.DEFAULT, self.conceal, self.DEFAULT)
        pass
    
    def reveal(self):
        self.img = self.reveal_img
        pass
    
    def conceal(self):
        self.img = self.default_img
        pass

    def get_state(self):
        return self.fsm.current_state

    def update_reveal_dist(self, change):
        self.reveal_dist = max(10, self.reveal_dist - change)
    
    def update(self, within_distance):
        self.fsm.process(within_distance)

    def draw(self, screen, food_pos):
        screen.blit(self.img, food_pos)