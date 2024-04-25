import pygame
import random
import sys
from song import Song
from audiobar import AudioBar
import numpy as np

class Game:
    def __init__(self, width, height, song):
        self.width = width
        self.height = height
        self.song = song
        self.bpm = self.song.get_tempo()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.next_color_change = pygame.time.get_ticks()

        self.bars = []
        self. frequencies = np.arange(100, 8000, 100)

        self.num_bars = len(self.frequencies)
        self.bar_width = self.width/self.num_bars
        self.bar_x = (self.width - self.bar_width*self.num_bars)/2

        for freq in self.frequencies:
            self.bars.append(AudioBar(self.bar_x, 300, freq, (255, 0, 0), max_height=400, width=self.bar_width))
            self.bar_x += self.bar_width

    def random_color(self, alpha=10):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), alpha)

    def calculate_beat_interval(self):
        return 60 * 1000 / self.bpm

    def run(self):
        current_time = pygame.time.get_ticks()
        last_time = current_time

        pygame.mixer.music.load("_assets/song.mp3")
        pygame.mixer.music.play(0)
        
        #color = self.random_color()

        running = True
        while running:
            current_time = pygame.time.get_ticks()
            change_time = (current_time - last_time) / 1000.0
            last_time = current_time
            beat_interval = self.calculate_beat_interval()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            
            if current_time >= self.next_color_change:
                self.song.draw_album(self.screen)
                color = self.random_color()
                self.screen.fill(color)
                self.next_color_change += beat_interval
            else:
                self.screen.fill(color)

            #self.screen.fill((255, 255, 255))

            for b in self.bars:
                b.update(change_time, self.song.get_decibel(pygame.mixer.music.get_pos()/1000.0, b.freq))
                b.render(self.screen)

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
