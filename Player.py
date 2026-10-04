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
    #_task1 and _task2 run until the program gets manually quit
    def _task1(self)->None:
        while self._isRunning:
            time.sleep(0.1) #timer
            if (mixer.music.get_busy() and (not self._isPaused) and self._currSong):
            #only increase the song timer when there's a song
                self._currPos+=0.1 #sync with time.sleep()


    def _task2(self)->None:
        while self._isRunning:
            time.sleep(0.1)
            for ev in event.get():
                if (ev.type==SONG_END): #we'll apply 'and self._currSong' to define it not None (in fact that's true)
                    #single loop > playlist loop
                    if (self._isLooped and self._currSong):
                        self.play(self._currSong)

                    #the single loop is Off
                    elif (self._listLooped and self._currSong): #playlist loop = On
                        if (len(self.myQueue)>0): #if there are at least 2 songs in the playlist
                            self.myQueue.append(self._currSong)
                            nextSong=self.myQueue.pop(0)
                            self.play(nextSong)

                        elif (self._currSong): #the playlist contains only 1 song
                            self.play(self._currSong)

                    elif (len(self.myQueue)>0): #playlist loop = Off, i.e self._listLooped=False
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
        
        self._t=None #the thread that is used to track the timer

        self._isRunning, self._isPaused, self._isLooped=True, False, False
        self._listLooped=False

        self._currSong, self._prevSong=None, None #prevSong is used for the playPrevious() method
        self._currPos=0 #timer for the music
    
        self._check_Song_Status=threading.Thread(target=self._task2)
        self._check_Song_Status.start()

        self._t=threading.Thread(target=self._task1)
        self._t.start()
    #we don't use "daemon=True" since we want to manually quit the program

    def quit(self)->None:
        self._isRunning=False
        time.sleep(0.15) #must be large enough so that _task1() can instantly update the program state
        mixer.quit()


    def play(self, song: str, startTime: float = 0.0)->None:
        if (song not in self._store):
            print("This song is not in your list!")
            
        else:
            self._isPaused=False
            self._currPos=startTime

            self._prevSong=self._currSong
            self._currSong=song

            mixer.music.load(f"{self.lib_folder}/{self._store[song]}")
            print(f"'{song}' is being played.")

            mixer.music.play(start=startTime)
            time.sleep(0.05) #wait for get_busy() to turn True


    def pause(self)->None:
        if (self._isPaused==False):
            self._isPaused=True
            mixer.music.pause()
            
        else:
            print("No song is being played or the current song is being paused!")


    def unpause(self)->None:
        if (self._isPaused==False):
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
            self._isPaused=False


    def restart(self)->None:
        mixer.music.rewind()
        self._currPos=0
        if (self._isPaused==True):
            time.sleep(0.05) #wait for get_busy() to turn True
            self._isPaused=False


    def rewind5s(self)->None:
        self._currPos=max(0.0, self._currPos-6)
        mixer.music.play(start=self._currPos)


    def forward5s(self)->None:
        self._currPos+=4
        mixer.music.play(start=self._currPos)

    #modifying the "loops" arugment in play() and queue() doesn't affect
    def toggleLoop(self)->None:
        self._isLooped=not self._isLooped
        if (self._isLooped):
            self._listLooped=False #if single loop is On, turn off playlist loop
        print(f"Loop mode has been turned {"On" if self._isLooped else "Off"}.")


    def playPrevious(self)->None:
        if (self._prevSong==None):
            print("There is no previous song to play!")
            return
        
        self.play(self._prevSong, startTime=0.0)


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


    def loopPlaylist(self, pList: str)->None:
        if (not os.path.exists(f"{self._dir_for_pls}/{pList}")):
            print(f"There is no playlist named '{pList}'!")
            return

        file_dir_list=os.listdir(f"{self._dir_for_pls}/{pList}")

        if (len(file_dir_list)==0):
            print(f"'{pList}' is empty! Nothing to loop.")
            return

        self._isLooped=False
        self._listLooped=True #turn off single loop, activate playlist loop
        
        songs=[os.path.splitext(file_dir)[0] for file_dir in file_dir_list]
        self.play(songs[0])

        self.myQueue.clear()
        self.myQueue=songs[1:]

        print(f"Loop mode is now On for '{pList}'.")


    def deletePlaylist(self, pList: str)->None:
        if (not os.path.exists(f"{self._dir_for_pls}/{pList}")):
            print(f"There is no playlist named '{pList}'!")
            return
        #os.remove only works for files, os.rmdir only works for empty directories,
        #os.removedirs even delete 'upwards'
        shutil.rmtree(f"{self._dir_for_pls}/{pList}")
        print(f"'{pList}' has been deleted.")


S=MusicPlayer()
S.makeNewPlaylist("sample playlist")

S.addToPlaylist("sample playlist", "m4")

S.addToPlaylist("sample playlist", "m2")

S.addToPlaylist("sample playlist", "morning_flower")

S.removeFromPlaylist("sample playlist", "m2")

S.loopPlaylist("sample playlist")



time.sleep(300)
S.deletePlaylist("sample playlist")
S.quit()