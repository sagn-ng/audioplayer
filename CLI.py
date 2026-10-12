from Player import MusicPlayer
import pygame, time, asyncio
from prompt_toolkit import prompt
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import radiolist_dialog

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
            e.app.exit(result="2")

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

    def __searchSong(self: CL_Interface)->str:
        print()
        song=input("Search for a song (leave blank to go back): ")
        return song

    def __run(self)->None:
        marker=0
        while True:
            try:
                if (marker%3==0): self.printMenu() #only print the menu every 3 times
                marker+=1
                choice=prompt("Enter choice: ", key_bindings=self.myKeys)

                if (choice=="1"):
                    song=self.__searchSong()
                    if (song==""): print("...Coming back to menu...")
                    else: self.myPlayer.play(song)

                if (choice=="2"):
                    self.myPlayer.PauseOrUnpause()
#####
                if (choice=="3"):
                    t=True
                    while (t):
                        print("Press 'n' or 'ctrl+left' to play the next.")
                        print("Press 'p' or 'ctrl+right' to play the previous song.")
                        print("Leave blank to go back.")
                        x=input("Your choice: ")
                        match (x):
                            case 'n':
                                self.myPlayer.playNext()
                                t=False
                            case 'p':
                                self.myPlayer.playPrevious()
                                t=False
                            case '':
                                print("...Coming back to menu...")
                                t=False
                            case _:
                                print("Invalid choice!")
                                print("Choose again!")                  
######

                if (choice=="4"):
                    result = radiolist_dialog(
                        title="Choice dialog",
                        text="Which one do you choose?",
                        values=[
                            ("a", "Add a new song to queue"),
                            ("rm", "Remove a song from queue"),
                        ]
                    ).run()

                    if (result=="a"):
                        song=self.__searchSong()
                        if (song==""): print("...Coming back to menu...")
                        else: self.myPlayer.addToQueue(song)

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
        print("1. Play a song (Search)") #done
        print("2. Pause/Unpause") #done
        print("3. Next / Prev")
        print("4. Queue management") #doing
        print("5. Playlist management")
        print("6. Thoát (Quit)") #done
 
    #def searchToPlay(self)->None:
    # 
    #def QueueManagement(self)->None:
    #
    #def PlaylistManagement(self)->None:     

A=CL_Interface()