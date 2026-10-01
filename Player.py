import pygame
from pygame import mixer, event
import os
import threading
import time

pygame.init()
SONG_END=pygame.USEREVENT+1

print(type(SONG_END)) #int

class MusicPlayer:

    def _task1(self)->None:
    #keep the program running even when the music is paused,
    #it only stops when reaching the end of the song or it's
    #shut down by mixer.music.stop()
        while (mixer.music.get_busy() or self.isPaused):
            if (not self.isPaused):
                self.currPos+=1 #sync with time.sleep()
            time.sleep(1) #make the main program work continuously and not get overloaded


    #we need a task on another thread to constantly check what to play next
    def _task2(self)->None:
        while True:
            time.sleep(0.1)
            for ev in pygame.event.get():
                if (ev.type==SONG_END): #if the player reaches the end of a song
                    if (self.isLooped and self.currSong): #assign "and self.currSong" make it valid for the play() line
                        self.play(self.currSong, startTime=0.0)

                    elif len(self.myQueue)>0: #play the next song from the queue
                        nextSong=self.myQueue.pop(0)
                        self.play(nextSong, startTime=0.0)

    
    def __init__(self) -> None:
        mixer.music.set_endevent(SONG_END)

        self._store=dict({}) #store[s] = path_of_s
        for file_dir in os.listdir("musicLib"):
            s=(file_dir.split('.'))[0]
            self._store[s]=file_dir #keys are the names

        self.myList=self._store.keys()
        self.myQueue=[]
        
        self.t=None #the thread that is used to play music

        self.isPaused, self.isLooped=False, False

        self.currSong=None
        self.currPos=0 #timer for the music

        mixer.init()
        mixer.music.set_volume(0.5)

        self._check_Song_Status=threading.Thread(target=self._task2, daemon=True)
        self._check_Song_Status.start() #it will work till the end of the program


    def play(self, song: str, startTime: float = 0.0)->None:
        if (song not in self._store):
            print("This song is not in your list!")
            

        else:
            self.isPaused=False
            self.currPos=startTime
            self.currSong=song

            mixer.music.load(f"musicLib/{self._store[song]}")
            print(f"'{song}' is being played.")

            mixer.music.play(start=startTime)
            time.sleep(0.05) #wait for get_busy() to turn True

            self.t=threading.Thread(target=self._task1)
            self.t.start()


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


S=MusicPlayer()
S.play("morning_flower")
S.toggleLoop()
time.sleep(36)
S.play("m1")