from Player import MusicPlayer
import pygame, time
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import radiolist_dialog, input_dialog
from prompt_toolkit.styles import Style #for styling dialogs

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

        @self.myKeys.add('escape','l')
        def _(e):
            self.myPlayer.toggleLoop()

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
        song=str(input_dialog(text="Search window",
                              title="Search for a song (cancel or leave blank to go back):", style=self.__style).run())
        return song

    def __run(self)->None:
        marker=0
        while True:
            try:
                if (marker%3==0): self.printMenu() #only print the menu every 3 times
                marker+=1
                choice=prompt("Enter choice:\n>> ", key_bindings=self.myKeys)

                if (choice=="1"):
                    song=self.__searchSong()
                    print()
                    if (song==""):
                        print("...Coming back to menu...")
                        continue

                    print(f"You searched for the song '{song}'.")
                    self.myPlayer.play(song)
#####

                elif (choice=="2"):
                    print("\nPress 'space' to pause/unpause and 'alt+L' to loop/unloop the current song.")
#####

                elif (choice=="3"):
                    print()
                    t=True
                    while (t):
                        print("Press 'n' or 'ctrl+left' to play the next.")
                        print("Press 'p' or 'ctrl+right' to play the previous song.")
                        print("Leave blank to go back.")
                        x=prompt(">> ", key_bindings=self.myKeys, style=self.__style)
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
                                print("Invalid choice or choice not included here!")
                                print("Choose again!")  
######

                elif (choice=="4"):
                    result = radiolist_dialog(
                        title="Choice dialog",
                        text="Which one do you choose?",
                        values=[
                            ("a", "Add a new song to queue"),
                            ("rm", "Remove a song from queue"),
                            ("p", "Show the queue"),
                            ("q", "Quit this dialog")
                        ],
                        style=self.__style
                    ).run()
                    print()
                    #if user chooses 'add' or 'remove'
                    if (result=="a" or result=="rm"):
                        song=self.__searchSong()
                        if (song==""):
                            print("...Coming back to menu...")
                            continue

                        print(f"You searched for the song '{song}'.")
                        if (result=="a"): self.myPlayer.addToQueue(song)
                        else: self.myPlayer.removeFromQueue(song)

                    #if user chooses 'print'
                    elif (result=="p"):
                        if (not self.myPlayer.myQueue):
                            print("The queue is empty! Nothing to show.")
                            continue

                        i=1
                        for x in self.myPlayer.myQueue:
                            print(f"{i}. {x}")
                            i+=1

                    #if user chooses 'quit'
                    else: print("...Coming back to menu...")
#####

                elif (choice=="6"):
                    self.myPlayer.quit()
                    break

#####
                else:
                    print("Invalid choice!")

            except (KeyboardInterrupt, EOFError):
                self.myPlayer.quit()
                break


    def __init__(self) -> None:
        self.myPlayer=MusicPlayer()
        self.hotkeys=dict({})

        self.__style=Style.from_dict({
            'dialog': 'bg:#0066ff',
            'dialog.body': 'bg:#000000 #ff0000'
        }) #self-created style for dialogs

        self.__loadKeys()

        self.__run()

    def printMenu(self)->None:
        print("\n" + "="*30)
        print("       MUSIC PLAYER MENU")
        print("="*30)
        print("1. Play a song (Search)") #done
        print("2. Pause/Unpause/Loop") #done
        print("3. Previous/Next")
        print("4. Queue management") #done
        print("5. Playlist management")
        print("6. Thoát (Quit)") #done
 
    #def searchToPlay(self)->None:
    # 
    #def QueueManagement(self)->None:
    #
    #def PlaylistManagement(self)->None:     

A=CL_Interface()