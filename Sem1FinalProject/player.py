import pygame 

class Player:
    def __init__(self, screen_width, screen_height):
        self.color = (0, 0, 255)  # Blue color for the player
        self.radius = 20
        self.width = 80
        self.height = 60
        self.position = [screen_width // 2 - self.width / 2, screen_height // 2 - self.height / 2]
        self.disp_x = 0
        self.disp_y = 0
        self.health = 100

    def update_disp(self, dist_x, dist_y):
        self.disp_x += dist_x
        self.disp_y += dist_y
        #print(str(self.disp_x) + " " + str(self.disp_y))

    def update_health(self, health_change):
        # Dependent on assumption that health doesn't increase
        self.health = max(0, self.health + health_change)
    