"""
Controls the shark player
Keeps track of location on map and health

@author: Isabel Prado-Tucker
@version: 2023
"""
import pygame 

class Player:
    # Class constructor
    def __init__(self, screen_width, screen_height):
        # Initializing variables
        self.color = (0, 0, 255) 
        self.radius = 20
        self.width = 80
        self.height = 60
        # Player should always be centered in the screen
        self.position = [screen_width // 2 - self.width / 2, screen_height // 2 - self.height / 2]
        self.disp_x = 0
        self.disp_y = 0
        self.health = 100 # Starts at full health
        self.img = pygame.image.load("Sem1FinalProject/img/shark.png")
        self.img = pygame.transform.scale(self.img, (self.width, self.height))

    # Keep track of relative location on the map (center is 0, 0)
    def update_disp(self, dist_x, dist_y):
        self.disp_x += dist_x
        self.disp_y += dist_y

    # Updates health based on parameters, but keeps is within [0, 100]
    def update_health(self, health_change):
        self.health = min(100, max(0, self.health + health_change))

    # Draw player and health
    def draw(self, screen):
        screen.blit(self.img, (self.position[0], self.position[1]))
    
        # Display health
        font = pygame.font.Font('freesansbold.ttf', 25)
        text = font.render("Health: " + str(self.health), True, (255, 255, 255))
        screen.blit(text, (600, 10))
