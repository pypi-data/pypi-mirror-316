import pygame
import sys
import time
import importlib.resources

def typing_effect(text, delay=0.05):
    # Dynamically load the sound file from the package
    with importlib.resources.path('typeFX.sounds', 'spacebar-click-keyboard-199448-[AudioTrimmer.com].mp3') as sound_path:
        pygame.mixer.init()  # Initialize the Pygame mixer
        sound = pygame.mixer.Sound(str(sound_path))  # Load the sound file
        
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            if char != ' ':
                sound.play()  # Play the sound when a character is typed
            time.sleep(delay)  # Delay between each character
        print()
