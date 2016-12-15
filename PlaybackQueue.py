import threading


class PlaybackQueue(object):

    def __init__(self, onFinishedCallback=None, onStoppedCallback=None):
        self.onFinishedCallback = onFinishedCallback
        self.onStoppedCallback = onStoppedCallback
        self.queue = []
        self.played = []
        self.playing = False
        self.currentTrack = None
        self.playbackSemaphore = threading.BoundedSemaphore(1)

    def startPlaying(self):
        print("Start! I am playing: ", self.playing)
        self.playNext()

    def stopPlaying(self, addToQueue=False):
        print("Stopping! I am playing: ", self.playing)
        if self.playing:
            try:
                if self.currentTrack.playbackHandlerInstance:
                    self.currentTrack.stop()
                self.playbackSemaphore.acquire()
                self.playing = False
                self.playbackSemaphore.release()
            except Exception as e:
                print(e)

            if addToQueue:
                self.playbackSemaphore.acquire()
                self.queue.insert(0, self.currentTrack)
                self.playbackSemaphore.release()

    def playNext(self):
        print("Next! I am playing: ", self.playing)
        if self.playing and self.currentTrack:
            self.stopPlaying()

        self.playbackSemaphore.acquire()
        if len(self.queue) == 0:
            self.playbackSemaphore.release()
            return
        self.played.append(self.currentTrack)
        self.currentTrack = self.queue.pop(0)
        self.currentTrack.play(self)
        self.playing = True
        self.playbackSemaphore.release()

    def playPrevious(self):
        if self.playing:
            self.stopPlaying()

        self.playbackSemaphore.acquire()
        self.queue.insert(0, self.currentTrack)
        self.currentTrack = self.played.pop(-1)
        self.currentTrack.play(self)
        self.playing = True
        self.playbackSemaphore.release()

    def addToQueue(self, track):
        self.playbackSemaphore.acquire()
        self.queue.append(track)
        self.playbackSemaphore.release()

    def getQueued(self):
        return self.queue

    def removeFromQueueByIndex(self, i):
        self.playbackSemaphore.acquire()
        del self.queue[i]
        self.playbackSemaphore.release()

    def removeFromQueueByTrack(self, track):
        self.playbackSemaphore.acquire()
        self.queue.remove(track)
        self.playbackSemaphore.release()

    def onFinished(self):
        if self.onFinishedCallback:
            self.onFinishedCallback()

        if self.playing:
            self.playNext()

    def onStopped(self):
        if self.onStoppedCallback:
            self.onStoppedCallback()
