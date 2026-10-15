## This is my first personal project: a mini music player.🎵🔊<br>

### *Note: if you're not going to read the description below, you can jump straight into the note in the last part (*Note)<br>

I used Python for this project, with some extra installed modules that i found very useful:<br>
  <i>pygame, prompt_tookit.</i><br>
(I have tried the modules 'keyboard' and 'pynput' but they only work with global hotkeys, i.e also swallowing keys of other programs)<br><br>

Here are some reference materials i used (and also some help from AI for explaining and summarizing those:>🗿):<br>
https://www.pygame.org/docs/ref/mixer.html<br>
https://www.pygame.org/docs/ref/music.html#module-pygame.mixer.music<br>
https://python-prompt-toolkit.readthedocs.io/en/stable/pages/advanced_topics/key_bindings.html<br>
https://python-prompt-toolkit.readthedocs.io/en/stable/pages/dialogs.html<br><br>

The <i><b>Player.py</b></i> file contains many core functions that i created for a simple player. It initializes one extra thread to keep the player run and a smaller thread for the song timer.<br>
The <i><b>CLI.py</b></i> file includes some utilities for user interaction on a terminal window (i'm currently just working on those two).

I divided the project into 3 main parts:<br>
- Basic functions for song management, then playlist/queue.<br>
- Integrating into a CLI (with the help of the module <i>'prompt_tookit'</i>).<br>
- (Maybe in the future) Implementing a real GUI (with the module 'Tkinter').<br><br>

### <b>--- 15/10/2026: I have basically done all of the stuff for a program with CLI. ---</b><br>
I 'extracted' the Python program into an executable (<i>.exe</i>) file, in the folder <i>'result'</i> with the help of the module <i>'pyinstaller'</i>.<br>
Since i want the <i>.exe</i> file to work in a separate folder for convenience (maybe deleting in the future), i created <i>'result'</i>.<br>
#### *Note: as i said, you only need the folder <i>'result'</i>, so if you just want to use the music player program, after downloading and extracting (the .zip file), you can just copy the folder <i>'result'</i> into another place that you like!
