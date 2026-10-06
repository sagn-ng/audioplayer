import Player
from Player import MusicPlayer
import pygame, keyboard, time

class CL_Interface:
    def __loadKeys(self)->None:
        keyboard.add_hotkey('shift+esc', self.myPlayer.quit)

        keyboard.add_hotkey('space', self.myPlayer.PauseOrUnpause)
        keyboard.add_hotkey('ctrl+l', self.myPlayer.toggleLoop)


        keyboard.add_hotkey('shift+right', self.myPlayer.playNext)
        keyboard.add_hotkey('shift+left', self.myPlayer.playPrevious)

        keyboard.add_hotkey('right', self.myPlayer.forward5s)
        keyboard.add_hotkey('left', self.myPlayer.rewind5s)



    def __init__(self) -> None:
        self.myPlayer=MusicPlayer()

        self.__loadKeys()

        self.printMenu()

    

    def printMenu(self)->None:
        print("\n" + "="*30)
        print("       MUSIC PLAYER MENU")
        print("="*30)
        print("1. Play a song (Search)")
        print("2. Pause/Unpause") #easy
        print("3. Next / Prev")  #easy
        print("4. Queue management")
        print("5. Playlist management")
        print("6. Thoát (Quit)") #easy



A=CL_Interface()
A.myPlayer.loopPlaylist("sample playlist")