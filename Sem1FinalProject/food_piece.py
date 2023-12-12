"""
Class for each piece of 'food'
the shark can eat

@author: Isabel Prado-Tucker
@version: 2023
"""
import random
from fsm import FSM

class Food_Piece:
    # Constants for possible food type
    URCHIN, FISH, LIONFISH, PLASTIC = 0, 1, 2, 3

    # Constructor
    def __init__(self, screen_width, screen_height, size, which_option, reveal_dist, default_img, reveal_img):
        # Constants for if to reveal food or not
        self.DEFAULT, self.ACTUAL = 0, 1
        # Possible states
        self.CLOSE, self.FAR = 0, 1

        # Initialize variables
        self.color = (70, 90, 125)
        self.size = size
        self.reveal_dist = reveal_dist
        self.type = which_option
        self.food_pos = (random.randint(-screen_width, 2 * screen_width),
                        random.randint(-screen_height, 2 * screen_height))
        self.default_img = default_img
        self.reveal_img = reveal_img
        self.img = self.default_img
       
        self.fsm = FSM(self.DEFAULT)
        self.init_fsm()
    
    # Initialize fsm to control revealing the food
    def init_fsm(self):
        self.fsm.add_transition(self.CLOSE, self.DEFAULT, self.reveal, self.ACTUAL)
        self.fsm.add_transition(self.CLOSE, self.ACTUAL, self.reveal, self.ACTUAL)
        self.fsm.add_transition(self.FAR, self.ACTUAL, self.conceal, self.DEFAULT)
        self.fsm.add_transition(self.FAR, self.DEFAULT, self.conceal, self.DEFAULT)
        pass
    
    # Change image to be the actual food
    def reveal(self):
        self.img = self.reveal_img
        pass
    
    # Change image to hid the food type
    def conceal(self):
        self.img = self.default_img
        pass
    
    # Returns the state of the fsm
    def get_state(self):
        return self.fsm.current_state

    # Changes the reveal distance
    def update_reveal_dist(self, change):
        self.reveal_dist = max(10, self.reveal_dist - change)
    
    # Fsm processing to reveal or conceal food
    def update(self, within_distance):
        self.fsm.process(within_distance)

    # Draw food
    def draw(self, screen, food_pos):
        screen.blit(self.img, food_pos)