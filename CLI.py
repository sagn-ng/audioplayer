from Player import MusicPlayer
import pygame, time, asyncio
from prompt_toolkit import prompt
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.key_binding import KeyBindings

class CL_Interface:
    def __loadKeys(self)->None:
        self.myKeys=KeyBindings()

        @self.myKeys.add('escape','q')
        def _(e):
            self.myPlayer.quit()
            e.app.exit(result="6")

        @self.myKeys.add('s')
        def _(e):
            e.app.exit(result="1")
            
        @self.myKeys.add('space')
        def _(e):
            self.myPlayer.PauseOrUnpause()

        @self.myKeys.add('c-left')
        def _(e):
            self.myPlayer.playPrevious()

        @self.myKeys.add('c-right')
        def _(e):
            self.myPlayer.playNext()

        @self.myKeys.add('left')
        def _(e):
            self.myPlayer.rewind5s()

        @self.myKeys.add('right')
        def _(e):
            self.myPlayer.forward5s()

    def __run(self)->None:
        while True:
            try:
                self.printMenu()
                choice=prompt("Enter choice: ", key_bindings=self.myKeys)

                if (choice=="1"):
                    print()
                    song=input("Search for a song (leave blank to go back): ")
                    if (song==""):
                        print("...Coming back to menu...")
                        continue

                    self.myPlayer.play(song)



                if (choice=="6"):
                    self.myPlayer.quit()
                    break

            except (KeyboardInterrupt, EOFError):
                self.myPlayer.quit()
                break


    def __init__(self) -> None:
        self.myPlayer=MusicPlayer()
        self.hotkeys=dict({})

        self.__loadKeys()

        self.__run()

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
 
    #def searchToPlay(self)->None:
    # 
    #def QueueManagement(self)->None:
    #
    #def PlaylistManagement(self)->None:     

A=CL_Interface()