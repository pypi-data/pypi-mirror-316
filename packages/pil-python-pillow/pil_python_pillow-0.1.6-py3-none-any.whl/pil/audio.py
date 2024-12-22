# 1. Installing Pygame Library
# Command:
# pip install pygame

# 2. Loading and Playing Audio
import pygame
pygame.mixer.init()
pygame.mixer.music.load("example.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pass

# 3. Adding Pause, Resume, and Stop Controls
import pygame
pygame.mixer.init()
pygame.mixer.music.load("example.mp3")
pygame.mixer.music.play()
while True:
    command = input("Press 'p' to pause, 'r' to resume, 'q' to quit: ").lower()
    if command == 'p':
        pygame.mixer.music.pause()
    elif command == 'r':
        pygame.mixer.music.unpause()
    elif command == 'q':
        pygame.mixer.music.stop()
        break

# 4. Adjusting Volume
import pygame
pygame.mixer.init()
pygame.mixer.music.load("example.mp3")
pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pass

# 5. Playing Multiple Audio Tracks Simultaneously
import pygame
pygame.mixer.init()
sound1 = pygame.mixer.Sound("sound1.wav")
sound2 = pygame.mixer.Sound("sound2.wav")
sound1.play()
sound2.play()
while pygame.mixer.get_busy():
    pass

# 6. Audio Crossfading
import pygame
pygame.mixer.init()
pygame.mixer.music.load("audio1.mp3")
pygame.mixer.music.play(fade_ms=3000)
pygame.time.delay(5000)
pygame.mixer.music.load("audio2.mp3")
pygame.mixer.music.play(fade_ms=3000)
while pygame.mixer.music.get_busy():
    pass

# 7. Looping Audio
import pygame
pygame.mixer.init()
pygame.mixer.music.load("loop_audio.mp3")
pygame.mixer.music.play(loops=-1)  # Infinite loop
pygame.time.delay(10000)  # Play for 10 seconds
pygame.mixer.music.stop()

# 8. Adding Audio Effects
import pygame
pygame.mixer.init()
sound = pygame.mixer.Sound("effect.wav")
sound.play()
pygame.time.delay(2000)
sound.fadeout(2000)  # Fade out over 2 seconds

# 9. Audio Visualization
from scipy.io import wavfile
import matplotlib.pyplot as plt
rate, data = wavfile.read("example.wav")
plt.figure(figsize=(10, 4))
plt.plot(data)
plt.title("Waveform")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.show()

# 10. Playing Sound Effects Based on User Actions
import pygame
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("jump.wav")
collision_sound = pygame.mixer.Sound("collision.wav")
while True:
    action = input("Press 'j' for jump sound or 'c' for collision sound: ").lower()
    if action == 'j':
        jump_sound.play()
    elif action == 'c':
        collision_sound.play()
    elif action == 'q':
        break

# 11. Saving Audio Output
from pydub import AudioSegment
audio = AudioSegment.from_file("example.mp3")
audio.export("output.wav", format="wav")

# 12. Full Example: Creating an Interactive Audio Player
import pygame
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()
while True:
    command = input("Enter 'p' to pause, 'r' to resume, 'v' to adjust volume, 'q' to quit: ").lower()
    if command == 'p':
        pygame.mixer.music.pause()
    elif command == 'r':
        pygame.mixer.music.unpause()
    elif command == 'v':
        volume = float(input("Enter volume (0.0 to 1.0): "))
        pygame.mixer.music.set_volume(volume)
    elif command == 'q':
        pygame.mixer.music.stop()
        break
