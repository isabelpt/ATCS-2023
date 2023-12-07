from PIL import Image, ImageOps, ImageDraw
import pygame
import math
from food import Food
from player import Player
from background import Background

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen dimensions
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Shark")
        self.clock = pygame.time.Clock()

        # Other variables
        self.cell_size = 50  # Size of grid cells
        self.num_food = 100

        # Create objects
        self.player = Player(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.food = Food(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.num_food)
        self.background_grid = [(x, y) for x in range(-self.SCREEN_WIDTH, 2 * self.SCREEN_WIDTH, self.cell_size)
                           for y in range(-self.SCREEN_HEIGHT, 2 * self.SCREEN_HEIGHT, self.cell_size)]
        self.background = Background(self.cell_size)

        # Images
        # self.player_img = Image.open("Sem1FinalProject/img/shark.png")
        # self.player_img = pygame.transform.scale(self.player_img, (75, 75))
        self.player_img = pygame.image.load("Sem1FinalProject/img/shark.png")
        self.player_img = pygame.transform.scale(self.player_img, (self.player.width, self.player.height))

        self.food_img_1 = pygame.image.load("Sem1FinalProject/img/urchin.png")
        self.food_img_1 = pygame.transform.scale(self.food_img_1, (self.food.size * 2, self.food.size * 2))

    def get_dist(self, food_pos, food_size):
        # distance = math.sqrt((player_pos[0] - food_pos[0])**2 + (player_pos[1] - food_pos[1])**2)
        # return distance < player_radius + food_size

        # Check collision between player and food
        # Need to pass in food_pos and food_size
        player_left = self.player.position[0]
        player_right = self.player.position[0] + self.player.width
        player_top = self.player.position[1]
        player_bottom = self.player.position[1] + self.player.height

        closest_x = max(player_left, min(food_pos[0], player_right))
        closest_y = max(player_top, min(food_pos[1], player_bottom))

        distance = math.sqrt((closest_x - food_pos[0])**2 + (closest_y - food_pos[1])**2)

        return distance 
    
    def check_collision(self, food_pos, food_size):
        return self.get_dist(food_pos, food_size) < food_size

    def run(self):
        running = True
        while running:
            self.screen.fill((120, 138, 204))  # Fill screen with white color

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()

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

            # Update background position based on the direction vector
            self.background.update_position(direction_x, direction_y)

            # Update player location on map
            speed = self.background.speed
            self.player.update_disp(direction_x * speed, direction_y * speed)
            # self.player_at_wall()
            # Draw background
            #self.background.draw(self.screen, self.background_grid)
            for cell in self.background_grid:
                cell_pos = (cell[0] - self.background.bg_x, cell[1] - self.background.bg_y)
                pygame.draw.rect(self.screen, (68, 86, 189), (cell_pos[0], cell_pos[1], self.cell_size, self.cell_size), 1)
                

            # Draw food and check collision with player
            for food_item in self.food.food_list[:]:
                food_pos = (food_item[0] - self.background.bg_x, food_item[1] - self.background.bg_y)
                # self.food.draw(self.screen, self.background.bg_x, self.background.bg_y)
                if self.get_dist(food_pos, self.food.size) < self.food.reveal_dist:
                    #color = (227, 32, 162)
                    self.screen.blit(self.food_img_1, food_pos)
                else:
                    #color = self.food.color
                    pygame.draw.circle(self.screen, self.food.color, (food_pos[0] + self.food.size, food_pos[1] + self.food.size), self.food.size)
                #pygame.draw.circle(self.screen, color, food_pos, self.food.size)
                #self.screen.blit(self.food_img_1, food_pos)
                player_position = self.player.position
                if self.check_collision(food_pos, self.food.size):
                    self.food.food_list.remove(food_item)
                    self.food.update_reveal_dist(5) # only do this when detracting from health

            # Draw player
            #pygame.draw.circle(self.screen, self.player.color, (self.player.position[0], self.player.position[1]), self.player.radius)
            self.screen.blit(self.player_img, (self.player.position[0], self.player.position[1]))
            # pygame.draw.rect(self.screen, self.player.color, (self.player.position[0], self.player.position[1], self.player.width, self.player.height), 1)

            # Limit frames per second
            self.clock.tick(60)

            pygame.display.flip()

        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
