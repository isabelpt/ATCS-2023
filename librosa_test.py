import librosa

# https://librosa.org/doc/latest/tutorial.html 
# 1. Get the file path to an included audio example


# 2. Load the audio as a waveform `y`
#    Store the sampling rate as `sr`
y, sr = librosa.load("_assets/song.mp3")

# 3. Run the default beat tracker
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

length = librosa.get_duration(y=y, sr=sr)

print(length)

print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

# 4. Convert the frame indices of beat events into timestamps
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# y_harmonic, y_percussive = librosa.effects.hpss(y)