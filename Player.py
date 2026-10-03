import pygame
from pygame import mixer, event
import os, time, threading
import shutil #for copying files
#We use 2 auxiliary threads running until the program is quit by us (see the quit() func.):
#- one as a timer for songs
#- the other one for switching songs and looping

pygame.init()
SONG_END=pygame.USEREVENT+1 #mark the moment that a song ends as an event

class MusicPlayer:
    def _task1(self)->None:
    #keep the program running even when the music is paused,
    #it only stops when the program
        while self._isRunning:
            time.sleep(0.1) #timer
            if (mixer.music.get_busy() and (not self.isPaused) and self.currSong):
            #only increase the song timer when there's a song
                self.currPos+=0.1 #sync with time.sleep()


    def _task2(self)->None:
    #this task also works only when the program is quit.
        while self._isRunning:
            time.sleep(0.1)
            for ev in event.get():
                if (ev.type==SONG_END):
                    if (self.isLooped and self.currSong): #assign "and self.currSong" make it valid for the play() line
                        self.play(self.currSong)

                    elif len(self.myQueue)>0:
                        nextSong=self.myQueue.pop(0)
                        self.play(nextSong)

    #a func. that helps us load the music library
    def _load_library(self)->None:
        if (not os.path.exists(self.lib_folder)):
            os.makedirs(self.lib_folder) #allow sub-folders

        for file_dir in os.listdir(self.lib_folder):
            name, ext=os.path.splitext(file_dir)

            if (ext in self._supportedFormats):
                if (name not in self._store):
                    self._store[name]=file_dir
            #there might be cases where we have 'm1.mp3', 'm1.m4a', we choose to
            #only take the first one found
    
    def __init__(self, lib_folder: str="musicLib", dir_for_pls: str="myPlaylists") -> None:
        mixer.init()
        time.sleep(0.1) #wait for "mixer" to start
        mixer.music.set_endevent(SONG_END) #register the event we've created
        mixer.music.set_volume(0.5)

        self._supportedFormats=[".mp3", ".wav", ".ogg", ".m4a"]

        self.lib_folder=lib_folder
        self._dir_for_pls=dir_for_pls
        self._store=dict({}) #store[s] = path_of_s
        self._load_library()

        self.myQueue=[]
        
        self.t=None #the thread that is used to track the timer

        self._isRunning, self.isPaused, self.isLooped=True, False, False

        self.currSong, self.prevSong=None, None #prevSong is used for the playPrevious() method
        self.currPos=0 #timer for the music
    
        self._check_Song_Status=threading.Thread(target=self._task2)
        self._check_Song_Status.start()

        self.t=threading.Thread(target=self._task1)
        self.t.start()
    #we don't use "daemon=True" since we want to manually quit the program

    def quit(self)->None:
        self._isRunning=False
        time.sleep(0.15) #must be large enough so that _task1() can instantly update the program state
        mixer.quit()


    def play(self, song: str, startTime: float = 0.0)->None:
        if (song not in self._store):
            print("This song is not in your list!")
            
        else:
            self.isPaused=False
            self.currPos=startTime

            self.prevSong=self.currSong
            self.currSong=song

            mixer.music.load(f"{self.lib_folder}/{self._store[song]}")
            print(f"'{song}' is being played.")

            mixer.music.play(start=startTime)
            time.sleep(0.05) #wait for get_busy() to turn True


    def pause(self)->None:
        if (self.isPaused==False):
            self.isPaused=True
            mixer.music.pause()
            
        else:
            print("No song is being played or the current song is being paused!")


    def unpause(self)->None:
        if (self.isPaused==False):
            print("No song is being paused!")

        else:
        #at this moment: get_busy()=False, isPaused=True
        #we need to set isPause=False and unpause() (i.e get_busy()=True), but:
        #if we set isPause=False first, the while loop in _task immediately stops
        #since it's updated continuously -> put unpause() first.
        #However, unpause() takes a couple of miliseconds to work, we need to stop
        #the time on the main thread to wait for it:
            mixer.music.unpause()
            time.sleep(0.05)
            self.isPaused=False


    def restart(self)->None:
        mixer.music.rewind()
        self.currPos=0
        if (self.isPaused==True):
            time.sleep(0.05) #wait for get_busy() to turn True
            self.isPaused=False


    def rewind5s(self)->None:
        self.currPos=max(0.0, self.currPos-6)
        mixer.music.play(start=self.currPos)


    def forward5s(self)->None:
        self.currPos+=4
        mixer.music.play(start=self.currPos)

    #modifying the "loops" arugment in play() and queue() doesn't affect
    def toggleLoop(self)->None:
        self.isLooped=not self.isLooped
        print(f"Loop mode has been turned {"On" if self.isLooped else "Off"}.")


    def playPrevious(self)->None:
        if (self.prevSong==None):
            print("There is no previous song to play!")
            return
        
        self.play(self.prevSong, startTime=0.0)


    def playNext(self)->None:
        if (len(self.myQueue)==0):
            print("The queue is empty! No song to play next!")
            return

        x=self.myQueue.pop(0)
        self.play(x, startTime=0.0)


    def addToQueue(self, song: str)->None:
        if (song not in self._store):
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
        if (os.path.exists(f"{self._dir_for_pls}/{pList}")):
            print("There's already a list with this name!")
            return

        os.makedirs(name=f"{self._dir_for_pls}/{pList}")


    def addToPlaylist(self, pList: str, song: str)->None:
        if (not os.path.exists(f"{self._dir_for_pls}/{pList}")):
            print(f"There is no playlist named '{pList}'!")
        
        elif (song not in self._store):
            print(f"'{song}' doesn't exist in the default library!")

        else:
            temp=[(song+x) for x in self._supportedFormats]
            for t in temp:
                if (os.path.exists(f"{self._dir_for_pls}/{pList}/{t}")):
                    print(f"'{song}' already exists in this playlist!")
                    return #if a file with the same name but different extension already exist
                    
            source=f"{self.lib_folder}/{self._store[song]}"
            destination=f"{self._dir_for_pls}/{pList}/{self._store[song]}"
            shutil.copyfile(source, destination)
            print(f"'{song}' has been added to '{pList}' successfully.")


    def removeFromPlaylist(self, pList: str, song: str)->None:
        if (not os.path.exists(f"{self._dir_for_pls}/{pList}")):
            print(f"There is no playlist named '{pList}'!")

        elif (not os.path.exists(f"{self._dir_for_pls}/{pList}/{self._store[song]}")):
              print(f"'{song}' doesn't exist in this playlist!") #if the song doesn't exist in the playlist
        
        else:
            os.remove(f"{self._dir_for_pls}/{pList}/{self._store[song]}")
            print(f"'{song}' has been remove from '{pList}' successfully.")
            

    def addPlaylistToQueue(self, pList: str)->None:
        if (not os.path.exists(f"{self._dir_for_pls}/{pList}")):
            print(f"There is no playlist named '{pList}'!")

        else:
            file_dir_list=os.listdir(f"{self._dir_for_pls}/{pList}")
            if (len(file_dir_list)==0):
                print(f"'{pList}' is empty! Nothing to add.")
                return

            for file_dir in file_dir_list:
                song=(file_dir.split('.'))[0]
                self.myQueue.append(song)

            print("Added to queue successfully.")


    def deletePlaylist(self, pList: str)->None:
        if (not os.path.exists(f"{self._dir_for_pls}/{pList}")):
            print(f"There is no playlist named '{pList}'!")
            return

        os.remove(f"{self._dir_for_pls}/{pList}")
        print(f"'{pList}' has been deleted.")


S=MusicPlayer()
S.play("m1")
time.sleep(25)
S.makeNewPlaylist("sample playlist")
S.makeNewPlaylist("sample playlist")
S.addToPlaylist("sampleplaylist", "m1")

S.addToPlaylist("sample playlist", "m1")

S.addToPlaylist("sample playlist", "m2")

S.addToPlaylist("sample playlist", "m3")

S.removeFromPlaylist("sampleplaylist", "m1")
S.removeFromPlaylist("sample playlist", "m2")

S.addPlaylistToQueue("sample playlist")

time.sleep(5)
S.quit()