import librosa
import pygame
import numpy as np

class Song:
    def __init__(self, song_name, width, height):
        self.y, self.sr = librosa.load("_assets/song.mp3")
        self.album_cover = pygame.image.load("_assets/folklore.jpg")
        self.album_cover = pygame.transform.scale(self.album_cover, (width, height))

        self.pygame_song = pygame.mixer.Sound('_assets/song.mp3')

        self.stft = np.abs(librosa.stft(self.y, hop_length=512, n_fft=2048*4))

        self.spectrogram = librosa.amplitude_to_db(self.stft, ref=np.max)  # converting the matrix to decibel matrix

        self.frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies

        self.times = librosa.core.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=self.sr, hop_length=512, n_fft=2048*4)

        self.time_index_ratio = len(self.times)/self.times[len(self.times) - 1]

        self.frequencies_index_ratio = len(self.frequencies)/self.frequencies[len(self.frequencies)-1]
    
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
    
    def get_decibel(self, target_time, freq):
        return self.spectrogram[int(freq * self.frequencies_index_ratio)][int(target_time * self.time_index_ratio)]
