"""
Creates and controls every piece of food

@author: Isabel Prado-Tucker
@version: 2023
"""
import pygame
import random
from food_piece import Food_Piece

class Food:
    # Class constructor
    def __init__(self, screen_width, screen_height, num_food):
        # Initialize variables
        self.color = (70, 90, 125) 
        self.size = 20
        self.food_list = []
        self.reveal_dist = 80
        self.num_options = 4

        # Load possible images
        self.default_img = pygame.image.load("Sem1FinalProject/img/circle.png")
        self.default_img = pygame.transform.scale(self.default_img, (self.size * 2, self.size * 2))
        self.urchin_img = pygame.image.load("Sem1FinalProject/img/urchin.png")
        self.urchin_img = pygame.transform.scale(self.urchin_img, (self.size * 2, self.size * 2))
        self.fish_img = pygame.image.load("Sem1FinalProject/img/fish.png")
        self.fish_img = pygame.transform.scale(self.fish_img, (self.size * 2, self.size * 2))
        self.lionfish_img = pygame.image.load("Sem1FinalProject/img/lionfish.png")
        self.lionfish_img = pygame.transform.scale(self.lionfish_img, (self.size * 2, self.size * 2))
        self.plastic_img = pygame.image.load("Sem1FinalProject/img/plastic.png")
        self.plastic_img = pygame.transform.scale(self.plastic_img, (self.size * 2, self.size * 2))
        self.reveal_images = [self.urchin_img, self.fish_img, self.lionfish_img, self.plastic_img]
        self.generate_food(screen_width, screen_height, num_food)

    # Generate all food items and add to list
    def generate_food(self, screen_width, screen_height, num_food):
        for _ in range(num_food):
            which_option = random.randint(0, self.num_options - 1)
            new_food = Food_Piece(screen_width, screen_height, self.size, which_option, self.reveal_dist, self.default_img, self.reveal_images[which_option])
            self.food_list.append(new_food)
    
    # Change reveal distance
    def update_reveal_dist(self, change):
        self.reveal_dist = max(15, self.reveal_dist - change)