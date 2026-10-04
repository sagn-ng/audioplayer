import pygame
from pygame import mixer, event
import os, time, threading
import shutil #for copying files and deleting playlist
#We use 2 auxiliary threads running until the program is quit by us (see the quit() func.):
#- one as a timer for songs
#- the other one for switching songs and looping

pygame.init()
SONG_END=pygame.USEREVENT+1 #mark the moment that a song ends as an event

class MusicPlayer:
    #__task1 and __task2 run until the program gets manually quit
    def ___task1(self)->None:
        while self.__isRunning:
            time.sleep(0.1) #timer
            if (mixer.music.get_busy() and (not self.__isPaused) and self.__currSong):
            #only increase the song timer when there's a song
                self.__currPos+=0.1 #sync with time.sleep()


    def ___task2(self)->None:
        while self.__isRunning:
            time.sleep(0.1)
            for ev in event.get():
                if (ev.type==SONG_END): #we'll apply 'and self.__currSong' to define it not None (in fact that's true)
                    #single loop > playlist loop
                    if (self.__isLooped and self.__currSong):
                        self.play(self.__currSong)

                    #the single loop is Off
                    elif (self.__listLooped and self.__currSong): #playlist loop = On
                        if (len(self.myQueue)>0): #if there are at least 2 songs in the playlist
                            self.myQueue.append(self.__currSong)
                            nextSong=self.myQueue.pop(0)
                            self.play(nextSong)

                        elif (self.__currSong): #the playlist contains only 1 song
                            self.play(self.__currSong)

                    elif (len(self.myQueue)>0): #playlist loop = Off, i.e self.__listLooped=False
                        nextSong=self.myQueue.pop(0)
                        self.play(nextSong)

    #a func. that helps us load the music library
    def _load_library(self)->None:
        if (not os.path.exists(self.lib_folder)):
            os.makedirs(self.lib_folder) #allow sub-folders

        for file_dir in os.listdir(self.lib_folder):
            name, ext=os.path.splitext(file_dir)

            if (ext in self.__supportedFormats):
                if (name not in self.__store):
                    self.__store[name]=file_dir
            #there might be cases where we have 'm1.mp3', 'm1.m4a', we choose to
            #only take the first one found
    
    def __init__(self, lib_folder: str="musicLib", dir_for_pls: str="myPlaylists") -> None:
        mixer.init()
        time.sleep(0.1) #wait for "mixer" to start
        mixer.music.set_endevent(SONG_END) #register the event we've created
        mixer.music.set_volume(0.5)

        self.__supportedFormats=[".mp3", ".wav", ".ogg", ".m4a"]

        self.lib_folder=lib_folder
        self.__dir_for_pls=dir_for_pls
        self.__store=dict({}) #store[s] = path_of_s
        self._load_library()

        self.myQueue=[]
        
        self.__t=None #the thread that is used to track the timer

        self.__isRunning, self.__isPaused, self.__isLooped=True, False, False
        self.__listLooped=False

        self.__currSong, self.__prevSong=None, None #prevSong is used for the playPrevious() method
        self.__currPos=0 #timer for the music
    
        self.__check_Song_Status=threading.Thread(target=self.___task2)
        self.__check_Song_Status.start()

        self.__t=threading.Thread(target=self.___task1)
        self.__t.start()
    #we don't use "daemon=True" since we want to manually quit the program

    def quit(self)->None:
        self.__isRunning=False
        time.sleep(0.15) #must be large enough so that __task1() can instantly update the program state
        mixer.quit()


    def play(self, song: str, startTime: float = 0.0)->None:
        if (song not in self.__store):
            print("This song is not in your list!")
            
        else:
            self.__isPaused=False
            self.__currPos=startTime

            self.__prevSong=self.__currSong
            self.__currSong=song

            mixer.music.load(f"{self.lib_folder}/{self.__store[song]}")
            print(f"'{song}' is being played.")

            mixer.music.play(start=startTime)
            time.sleep(0.05) #wait for get_busy() to turn True


    def pause(self)->None:
        if (self.__isPaused==False):
            self.__isPaused=True
            mixer.music.pause()
            
        else:
            print("No song is being played or the current song is being paused!")


    def unpause(self)->None:
        if (self.__isPaused==False):
            print("No song is being paused!")

        else:
        #at this moment: get_busy()=False, isPaused=True
        #we need to set isPause=False and unpause() (i.e get_busy()=True), but:
        #if we set isPause=False first, the while loop in __task immediately stops
        #since it's updated continuously -> put unpause() first.
        #However, unpause() takes a couple of miliseconds to work, we need to stop
        #the time on the main thread to wait for it:
            mixer.music.unpause()
            time.sleep(0.05)
            self.__isPaused=False


    def restart(self)->None:
        mixer.music.rewind()
        self.__currPos=0
        if (self.__isPaused==True):
            time.sleep(0.05) #wait for get_busy() to turn True
            self.__isPaused=False


    def rewind5s(self)->None:
        self.__currPos=max(0.0, self.__currPos-6)
        mixer.music.play(start=self.__currPos)


    def forward5s(self)->None:
        self.__currPos+=4
        mixer.music.play(start=self.__currPos)

    #modifying the "loops" arugment in play() and queue() doesn't affect
    def toggleLoop(self)->None:
        self.__isLooped=not self.__isLooped
        if (self.__isLooped):
            self.__listLooped=False #if single loop is On, turn off playlist loop
        print(f"Loop mode has been turned {"On" if self.__isLooped else "Off"}.")


    def playPrevious(self)->None:
        if (self.__prevSong==None):
            print("There is no previous song to play!")
            return
        
        self.play(self.__prevSong, startTime=0.0)


    def playNext(self)->None:
        if (len(self.myQueue)==0):
            print("The queue is empty! No song to play next!")
            return

        x=self.myQueue.pop(0)
        self.play(x, startTime=0.0)


    def addToQueue(self, song: str)->None:
        if (song not in self.__store):
            print("This song doesn't exist in our library!")
            return

        if (song in self.myQueue):
            print("It's already in the queue!")
            return

        self.myQueue.append(song)


    def removeFromQueue(self, song: str)->None:
        #the current song that's being played is already not in the queue
        #so we don't have to worry
        if (song not in self.myQueue):
            print("This song might not exist in our library or not in the queue yet!")
            return

        self.myQueue.remove(song)


    def makeNewPlaylist(self, pList: str)->None:
        if (os.path.exists(f"{self.__dir_for_pls}/{pList}")):
            print("There's already a list with this name!")
            return

        os.makedirs(name=f"{self.__dir_for_pls}/{pList}")


    def addToPlaylist(self, pList: str, song: str)->None:
        if (not os.path.exists(f"{self.__dir_for_pls}/{pList}")):
            print(f"There is no playlist named '{pList}'!")
        
        elif (song not in self.__store):
            print(f"'{song}' doesn't exist in the default library!")

        else:
            temp=[(song+x) for x in self.__supportedFormats]
            for t in temp:
                if (os.path.exists(f"{self.__dir_for_pls}/{pList}/{t}")):
                    print(f"'{song}' already exists in this playlist!")
                    return #if a file with the same name but different extension already exist
                    
            source=f"{self.lib_folder}/{self.__store[song]}"
            destination=f"{self.__dir_for_pls}/{pList}/{self.__store[song]}"
            shutil.copyfile(source, destination)
            print(f"'{song}' has been added to '{pList}' successfully.")


    def removeFromPlaylist(self, pList: str, song: str)->None:
        if (not os.path.exists(f"{self.__dir_for_pls}/{pList}")):
            print(f"There is no playlist named '{pList}'!")

        elif (not os.path.exists(f"{self.__dir_for_pls}/{pList}/{self.__store[song]}")):
              print(f"'{song}' doesn't exist in this playlist!") #if the song doesn't exist in the playlist
        
        else:
            os.remove(f"{self.__dir_for_pls}/{pList}/{self.__store[song]}")
            print(f"'{song}' has been remove from '{pList}' successfully.")
            

    def addPlaylistToQueue(self, pList: str)->None:
        if (not os.path.exists(f"{self.__dir_for_pls}/{pList}")):
            print(f"There is no playlist named '{pList}'!")

        else:
            file_dir_list=os.listdir(f"{self.__dir_for_pls}/{pList}")
            if (len(file_dir_list)==0):
                print(f"'{pList}' is empty! Nothing to add.")
                return

            for file_dir in file_dir_list:
                song=(file_dir.split('.'))[0]
                self.myQueue.append(song)

            print("Added to queue successfully.")


    def loopPlaylist(self, pList: str)->None:
        if (not os.path.exists(f"{self.__dir_for_pls}/{pList}")):
            print(f"There is no playlist named '{pList}'!")
            return

        file_dir_list=os.listdir(f"{self.__dir_for_pls}/{pList}")

        if (len(file_dir_list)==0):
            print(f"'{pList}' is empty! Nothing to loop.")
            return

        self.__isLooped=False
        self.__listLooped=True #turn off single loop, activate playlist loop
        
        songs=[os.path.splitext(file_dir)[0] for file_dir in file_dir_list]
        self.play(songs[0])

        self.myQueue.clear()
        self.myQueue=songs[1:]

        print(f"Loop mode is now On for '{pList}'.")


    def deletePlaylist(self, pList: str)->None:
        if (not os.path.exists(f"{self.__dir_for_pls}/{pList}")):
            print(f"There is no playlist named '{pList}'!")
            return
        #os.remove only works for files, os.rmdir only works for empty directories,
        #os.removedirs even delete 'upwards'
        shutil.rmtree(f"{self.__dir_for_pls}/{pList}")
        print(f"'{pList}' has been deleted.")


S=MusicPlayer()
S.makeNewPlaylist("sample playlist")

S.addToPlaylist("sample playlist", "m4")

S.addToPlaylist("sample playlist", "m2")

S.addToPlaylist("sample playlist", "morning_flower")

S.removeFromPlaylist("sample playlist", "m2")

S.loopPlaylist("sample playlist")

print(S.__isRunning)

time.sleep(300)
S.deletePlaylist("sample playlist")
S.quit()