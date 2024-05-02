import librosa
import pygame
import numpy as np
from PIL import Image, ImageOps, ImageDraw
import colorgram

class Song:
    def __init__(self, song_name, width, height):
        self.y, self.sr = librosa.load("_assets/good.mp3")
        self.album_cover = pygame.image.load("_assets/folklore.png")
        self.album_cover = pygame.transform.scale(self.album_cover, (width, height))

        self.stft = np.abs(librosa.stft(self.y, hop_length=512, n_fft=2048*4))
        self.spectrogram = librosa.amplitude_to_db(self.stft, ref=np.max)  # converting the matrix to decibel matrix
        self.frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies
        self.times = librosa.core.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=self.sr, hop_length=512, n_fft=2048*4)

        self.time_index_ratio = len(self.times)/self.times[len(self.times) - 1]
        self.frequencies_index_ratio = len(self.frequencies)/self.frequencies[len(self.frequencies)-1]

        self.top_colors = self.get_top_colors("_assets/folklore.png")
        self.record_img = self.create_record("_assets/folklore.png", "_assets/record_img.png")
        self.record = pygame.image.load("_assets/record_img.png")
        self.rot_images = []
        self.make_rotated_images(50)
        self.counter = 1

    
    def get_tempo(self):
        tempo, beat_frames = librosa.beat.beat_track(y=self.y, sr=self.sr)
        return tempo

    def play_song(self):
        self.pygame_song.play()
    
    def get_decibel(self, target_time, freq):
        return self.spectrogram[int(freq * self.frequencies_index_ratio)][int(target_time * self.time_index_ratio)]
    
    def get_top_colors(self, image_url):
        # Open the image
        image = Image.open(image_url)

        # Extract colors from the image
        colors = colorgram.extract(image, 5)

        # Get the RGB values of the top 5 colors
        top_colors = [(color.rgb.r, color.rgb.g, color.rgb.b) for color in colors]
        
        return top_colors

    def create_record_mask(self, size):
        # Create a new image with a white background
        mask = Image.new('L', (size, size), 255)

        # Create a circular mask with a transparent center
        draw = ImageDraw.Draw(mask)
        center = (size // 2, size // 2)
        radius = size // 2 - 5

        # Draw a filled circle at the center of the mask
        draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), fill=0)
        
        draw.ellipse((center[0] - 110, center[1] - 110, center[0] + 110, center[1] + 110), fill=255)
        mask = Image.eval(mask, lambda px: 255 - px)

        return mask

    def add_circle(self, record, position, radius, color):

        # Create a transparent overlay
        overlay = Image.new("RGBA", record.size, (0, 0, 0, 0))

        # Draw a blue circle on the overlay
        draw = ImageDraw.Draw(overlay)
        draw.ellipse((position[0] - radius, position[1] - radius, position[0] + radius, position[1] + radius), fill=color)
        draw.ellipse((position[0] - 15, position[1] - 15, position[0] + 15, position[1] + 15), fill=255)
        # Composite the overlay and the original image
        record = record.convert('RGBA')
        image_with_overlay = Image.alpha_composite(record, overlay)

        # Save the resulting image
        return image_with_overlay
        

    def create_record(self, album_cover_url, out_path):
        # Open the base and overlay images
        base_img = Image.open("_assets/folklore.png")
        overlay_img = Image.open('_assets/record.png')

        overlay_img = overlay_img.crop((25,25,487,487))

        overlay_img = overlay_img.convert('RGBA').resize(base_img.size)

        # Define the position where the overlay image will be pasted
        position = (0, 0)

        # Overlay the image over base image
        base_img.paste(overlay_img, position, overlay_img)

        mask_size = min(base_img.size)
        mask = self.create_record_mask(mask_size)
        base_img.putalpha(mask)

        base_img = self.add_circle(base_img, (base_img.width/2, base_img.width/2), 170, self.top_colors[0])
        # Save the resulting image
        base_img.save(out_path)

    def make_rotated_images(self, num):
        orig_img = Image.open("_assets/record_img.png")
        inc = 360/num
        for n in range(1, num):
            new_img = orig_img.rotate(n*inc)
            new_img.save("_assets/record" + str(n) + ".png")
            self.rot_images.append(pygame.image.load("_assets/record" + str(n) + ".png"))
    
    def draw(self, screen, radius, loc):
        if self.counter >= len(self.rot_images):
            self.counter = 1
        img = pygame.transform.scale(self.rot_images[self.counter], (2*radius, 2*radius))
        screen.blit(img, loc)
        self.counter += 1