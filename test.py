import pygame
import threading
from pygame import mixer
import time
from prompt_toolkit.shortcuts import input_dialog

result=input_dialog(text="search window", title="type something").run()
if (result=="Sang"): print(True)
else: print(False)