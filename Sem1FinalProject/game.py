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

    def check_collision(self, player_pos, food_pos, player_radius, food_size):
        distance = math.sqrt((player_pos[0] - food_pos[0])**2 + (player_pos[1] - food_pos[1])**2)
        return distance < player_radius + food_size

    def player_at_wall(self):
        # player_x = self.player.disp_x
        # player_y = self.player.disp_y
        if abs(self.background.bg_x) >= self.SCREEN_WIDTH + 350:
            #self.background.bg_x = 0
            print("x out of bounds")
        if abs(self.background.bg_y) >= self.SCREEN_HEIGHT + 250:
            #self.background.bg_y = 0
            print("y out of bounds")
        #print(self.background_grid[0])
        # Get location of the wall
        #wall_x = self.background_grid[0][0] - self.background.bg_x
        #wall_y = self.background_grid[0][1] - self.background.bg_y
        
        # if wall_x == self.player.position[0]:
        #     self.background.bg_x = 0
        # if wall_y == self.player.position[0]:
        #     self.background.bg_y = 0

        print(self.background.bg_x)
        print(self.background.bg_y)

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
            if abs(self.background.bg_x) >= self.SCREEN_WIDTH + 375:
                    direction_x = 0
            else:
                direction_x = mouse_pos[0] - self.player.position[0]
            if abs(self.background.bg_y) >= self.SCREEN_WIDTH + 75:
                    direction_y = 0
            else:
                direction_y = mouse_pos[1] - self.player.position[1]

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
            self.player_at_wall()
            # Draw background
            #self.background.draw(self.screen, self.background_grid)
            for cell in self.background_grid:
                cell_pos = (cell[0] - self.background.bg_x, cell[1] - self.background.bg_y)
                pygame.draw.rect(self.screen, (68, 86, 189), (cell_pos[0], cell_pos[1], self.cell_size, self.cell_size), 1)
                

            # Draw food and check collision with player
            for food_item in self.food.food_list[:]:
                food_pos = (food_item[0] - self.background.bg_x, food_item[1] - self.background.bg_y)
                # self.food.draw(self.screen, self.background.bg_x, self.background.bg_y)
                pygame.draw.circle(self.screen, self.food.color, food_pos, self.food.size)
                player_position = self.player.position
                if self.check_collision(player_position, food_pos, self.player.radius, self.food.size):
                    self.food.food_list.remove(food_item)

            # Draw player
            pygame.draw.circle(self.screen, self.player.color, (self.player.position[0], self.player.position[1]), self.player.radius)

            # Limit frames per second
            self.clock.tick(60)

            pygame.display.flip()

        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
