This is my first personal project: a mini music player.🎵🔊<br>

I used Python for this project, with some extra installed modules that i found very useful:<br>
  <i>os, pygame, keyboard.</i>
Here are some reference materials i used (and also some help from AI for explaining and summarizing those:>🗿):<br>
https://www.pygame.org/docs/ref/mixer.html<br>
https://www.pygame.org/docs/ref/music.html#module-pygame.mixer.music<br>
https://pypi.org/project/keyboard/


The Player.py file contains many core functions that i created for a simple player. It initializes one extra thread to keep the player run and a smaller thread for the song timer.<br>
The CLI.py file includes some utilities for user interaction on a terminal window (i'm currently just working on those two).

I divided the project into 3 main parts:<br>
- Basic functions for song management, then playlist/queue.<br>
- Integrating into a CLI (with the help of the module "keyboard").<br>
- (Maybe in the future) Implementing a real GUI (with the module "Tkinter").
