import librosa
import pygame

class Song:
    def __init__(self, song_name, width, height):
        self.y, self.sr = librosa.load("_assets/met.mp3")
        self.album_cover = pygame.image.load("_assets/folklore.jpg")
        self.album_cover = pygame.transform.scale(self.album_cover, (width, height))

        self.pygame_song = pygame.mixer.Sound('_assets/met.mp3')
    
    def get_tempo(self):
        tempo, beat_frames = librosa.beat.beat_track(y=self.y, sr=self.sr)
        print(tempo)
        return tempo

    def get_length(self):
        length = librosa.get_duration(y=self.y, sr=self.sr)
        print(length)

    def draw_album(self, screen):
        screen.blit(self.album_cover, (0, 0))

    def play_song(self):
        self.pygame_song.play()