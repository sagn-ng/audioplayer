import pygame
import threading
from pygame import mixer
import time

mixer.init()
def task(song)->None:
    mixer.music.load(f"musicLib/{song}.mp3")
    mixer.music.play()

    while (mixer.music.get_busy()):
        time.sleep(0.1)


task("morning_flower")
x=mixer.music.get_busy()
print(x)