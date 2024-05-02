import pygame
import random
import sys
from song import Song
from audiobar import AudioBar
import numpy as np
import math

class Game:
    def __init__(self, width, height, song):
        self.width, self.height, self.song = width, height, song
        self.bpm = self.song.get_tempo()

        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.next_color_change = pygame.time.get_ticks()

        self.color_i = 0
        self.color = self.song.top_colors[self.color_i]

        self.audio_bars = []
        self.frequencies = np.arange(0, self.width, 15)

        self.num_bars = len(self.frequencies)
        self.bar_width = math.ceil(self.width/self.num_bars)
        self.bar_x = (self.width - self.bar_width*self.num_bars)/2

        for freq in self.frequencies:
            self.audio_bars.append(AudioBar(self.bar_x, 20, freq, self.song.top_colors[len(self.song.top_colors)-1], self.bar_width, self.height))
            self.bar_x += self.bar_width
        
        self.min_radius = 175
        self.radius = self.min_radius
        self.radius_vel = 1

        pygame.mixer.music.load("_assets/good.mp3")

    def random_color(self, alpha=10):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), alpha)

    def calculate_beat_interval(self):
        return 60 * 1000 / self.bpm

    def run(self):
        current_time = pygame.time.get_ticks()
        last_time = current_time
        pygame.mixer.music.play(0)

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
                if self.color_i >= len(self.song.top_colors) - 1:
                    self.color_i = 0
                self.color = self.song.top_colors[self.color_i]
                self.color_i += 1
                self.radius_vel *= -1
                self.next_color_change += beat_interval

            self.screen.fill(self.color)

            for bar in self.audio_bars:
                bar.update(change_time, self.song.get_decibel(pygame.mixer.music.get_pos()/1000.0, bar.frequency))
                bar.draw(self.screen)
            
            self.song.draw(self.screen, self.radius, (self.width/2-self.radius,self.height/2-self.radius))
            
            self.radius += self.radius_vel

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 500, 500
    song = Song("song", WIDTH, HEIGHT)
    game = Game(WIDTH, HEIGHT, song)
    game.run()
