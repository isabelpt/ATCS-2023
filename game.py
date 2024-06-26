import pygame
import random
import sys
from song import Song

class Game:
    def __init__(self, width, height, song):
        self.width = width
        self.height = height
        self.song = song
        self.bpm = self.song.get_tempo()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.next_color_change = pygame.time.get_ticks()

    def random_color(self, alpha=10):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), alpha)

    def calculate_beat_interval(self):
        return 60 * 1000 / self.bpm

    def run(self):
        running = True
        self.song.play_song()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_time = pygame.time.get_ticks()
            beat_interval = self.calculate_beat_interval()

            if current_time >= self.next_color_change:
                self.song.draw_album(self.screen)
                self.screen.fill(self.random_color())
                self.next_color_change += beat_interval

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# Example usage:
if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 500, 500
    song = Song("song", WIDTH, HEIGHT)
    color_changing_screen = Game(WIDTH, HEIGHT, song)
    color_changing_screen.run()
