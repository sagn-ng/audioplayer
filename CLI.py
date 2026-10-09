from Player import MusicPlayer
import pygame, time
from prompt_toolkit import prompt, application
from prompt_toolkit.key_binding import KeyBindings

class CL_Interface:
    def __loadKeys(self)->None:
        self.myKeys=KeyBindings()

        @self.myKeys.add('s-escape')
        def _(e):
            self.myPlayer.quit()
            e.app.exit()

        @self.myKeys.add('s')
        def _(e):
            def ask_song():
                song=str(input("\nSearch for a song: "))
                self.myPlayer.play(song)
            application.run_in_terminal(ask_song)
            
        @self.myKeys.add('space')
        def _(e):
            self.myPlayer.PauseOrUnpause()

        @self.myKeys.add('s-left')
        def _(e):
            self.myPlayer.playPrevious()

        @self.myKeys.add('s-right')
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
                if (choice.strip()=="6"): break

            except (KeyboardInterrupt, EOFError):
                self.myPlayer.quit()
                break


    def __init__(self) -> None:
        self.myPlayer=MusicPlayer()
        self.hotkeys=dict({})

        self.__loadKeys()

        self.printMenu()

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