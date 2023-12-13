"""
Shark Game

@author: Isabel Prado-Tucker
@version: 2023
"""
from time import sleep
import pygame
import math
from food import Food
from player import Player
from background import Background
from fsm import FSM

class Game:
    # Constants for types of food
    URCHIN, FISH, LIONFISH, PLASTIC = 0, 1, 2, 3

    # Class constrictor
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen dimensions
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Jaws vs. Junk")
        self.clock = pygame.time.Clock()

        # Other variables
        self.cell_size = 50  # Size of grid cells
        self.num_food = 100

        # Game states
        self.STARTUP, self.RUNNING, self.END = 0, 1, 2
        self.run_method = {self.STARTUP: self.startup, self.RUNNING: self.running, self.END: self.end_screen}

        # Create fsm
        self.fsm = FSM(self.STARTUP)
        self.init_fsm()

        # Create objects
        self.player = Player(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.food = Food(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.num_food)
        self.background_grid = [(x, y) for x in range(-self.SCREEN_WIDTH, 2 * self.SCREEN_WIDTH, self.cell_size)
                           for y in range(-self.SCREEN_HEIGHT, 2 * self.SCREEN_HEIGHT, self.cell_size)]
        self.background = Background(self.cell_size)
        self.button_rect = pygame.Rect(325, 320, 150, 60) # Startup button

        # Create and load sountrack
        pygame.mixer.init()
        pygame.mixer.music.load("Sem1FinalProject/media/song.mp3")
        pygame.mixer.music.set_volume(1)


    # Initialize fsm that controls screen graphics
    def init_fsm(self):
        self.fsm.add_transition(True, self.STARTUP, self.running, self.RUNNING) # Switch from startup to game
        self.fsm.add_transition(True, self.RUNNING, self.end_screen, self.END) # Switch from game to end screen
        self.fsm.add_transition(True, self.END, self.end_screen, self.END) # Switch from game to end screen

    # Returns the distance between a piece of food and the player
    # Used for collision detection and revealing the food item
    def get_dist(self, food_pos, food_size):
        # Get position values of the player
        player_left = self.player.position[0]
        player_right = self.player.position[0] + self.player.width
        player_top = self.player.position[1]
        player_bottom = self.player.position[1] + self.player.height

        # Get closest points of possible contact
        closest_x = max(player_left, min(food_pos[0], player_right))
        closest_y = max(player_top, min(food_pos[1], player_bottom))

        distance = math.sqrt((closest_x - food_pos[0])**2 + (closest_y - food_pos[1])**2)

        return distance # Returns the distance to the food
    
    # Returns true if the player is touching the food
    def check_collision(self, food_pos, food_size):
        return self.get_dist(food_pos, food_size) + 10 < food_size # +10 buffer to make it harder to eat the food

    # Startup screen
    # Displays name of the game, instructions, and the start button
    def startup(self):
        # Display game name
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render("Jaws vs. Junk", True, (255, 255, 255))
        self.screen.blit(text, (self.SCREEN_WIDTH / 2 - 175, 150))

        # Display instructions
        font = pygame.font.Font('freesansbold.ttf', 20)
        instructions = "Try to eat the fish and lionfish while avoiding the sea urchins and plastic!"
        text = font.render(instructions, True, (0, 0, 0))
        self.screen.blit(text, (45, 225))

        # Display button
        text = font.render('Get Started', True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 350))
        pygame.draw.rect(self.screen, (0, 0, 0), self.button_rect)
        self.screen.blit(text, text_rect)

    # Displays graphics for the game while it is running
    def running(self):
        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        """
        Start of ChatGPT 3.5 generated code
        Asked it to create an agar.io style pygame game where the background moves based on the direction of the mouse
        Edited by: Isabel Prado-Tucker
        """
        # Calculate the direction vector from player to mouse
        direction_x = mouse_pos[0] - self.player.position[0]
        direction_y = mouse_pos[1] - self.player.position[1]
        bound_x = self.SCREEN_WIDTH + 355
        bound_y = self.SCREEN_WIDTH + 70
        if self.background.bg_x >= bound_x and direction_x > 0:
            direction_x = 0
        elif self.background.bg_x <= (-1 * bound_x) and direction_x < 0:
            direction_x = 0
        if self.background.bg_y >= bound_y and direction_y > 0:
            direction_y = 0
        elif self.background.bg_y <= (-1 * bound_y) and direction_y < 0:
            direction_y = 0

        # Normalize the direction vector
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if magnitude != 0:
            direction_x /= magnitude
            direction_y /= magnitude

        """
        End of ChatGPT generated code
        """

        # Update background position based on the direction vector
        self.background.update_position(direction_x, direction_y)

        # Update player location on map
        speed = self.background.speed
        self.player.update_disp(direction_x * speed, direction_y * speed)

        # Draw the backfround
        self.background.draw(self.screen, self.background_grid)
            
        if len(self.food.food_list) == 0:
            self.fsm.process(True)

        # Draw food and check collision with player
        for item in self.food.food_list[:]:
            food_item = item.food_pos
            food_pos = (food_item[0] - self.background.bg_x, food_item[1] - self.background.bg_y)

            # Update to reveal food if necessary
            item.update(0 if self.get_dist(food_pos, self.food.size) < self.food.reveal_dist else 1)
            item.draw(self.screen, food_pos)

            # Change behavior based on type of food collided with
            if self.check_collision(food_pos, self.food.size):
                # Urchins are harmful
                if item.type == self.URCHIN:
                    self.player.update_health(-8)
                    self.food.update_reveal_dist(5)
                # Fish are benefitial
                elif item.type == self.FISH:
                    self.player.update_health(5)
                # Eating lionfish helps because they are invasive
                elif item.type == self.LIONFISH:
                    self.player.update_health(7)
                    self.food.update_reveal_dist(-5)
                # Eating plastic is very harmful
                elif item.type == self.PLASTIC:
                    self.background.speed = min(10, self.background.speed + 1)
                    self.player.update_health(-15)
                    self.food.update_reveal_dist(5)

                self.food.food_list.remove(item) # Remove if collision occurs
                
        # Draw player
        self.player.draw(self.screen)

    # Display end screen once the game ends
    def end_screen(self):
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render("Game Over", True, (255, 255, 255))
        self.screen.blit(text, (self.SCREEN_WIDTH / 2 - 150, 100))

    # Manages running the correct method based on the states
    def run(self):
        running = True
        while running:
            self.screen.fill((46, 87, 153))  # Fill screen with blue color
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                #####################################
                # Start of ChatGPT 3.5 Generated Code
                # Asked it for the simplest way in pygame to check if a button has been clicked
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If start button clicked, start the game
                    if self.fsm.current_state == self.STARTUP:
                        if self.button_rect.collidepoint(event.pos):
                            # End of ChatGPT Generated Code
                            ###############################
                            pygame.mixer.music.play() # Start the music
                            self.fsm.process(True)

            self.run_method[self.fsm.current_state]() # Run whichever method corresponds to the state

            # End game when the player runs out of health
            if self.player.health == 0:
                self.fsm.process(True)

            # Limit frames per second
            self.clock.tick(60)

            pygame.display.flip()

        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
