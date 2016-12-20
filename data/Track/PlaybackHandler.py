import os
import signal
import subprocess
import threading


class PlaybackHandler(object):
    """
    Superclass for PlaybackHandler classes

    PlaybackHandlers are used to play back audio
    from some kind of source.
    """

    def __init__(self):
        self.playing = False  # type: bool
        self.stopCalled = False  # type: bool
        self.playerProcess = None  # type: Any
        self.playerProcessMutex = threading.BoundedSemaphore(1)
        self.delegate = None  # type: object

    def play(self, command, delegate: object) -> None:
        self.delegate = delegate
        self.stopCalled = False
        self.playing = True
        self.runThreadedPlayback(self.callDelegate, command)

    def stop(self) -> None:
        if self.playing:
            self.stopCalled = True
            os.killpg(os.getpgid(self.playerProcess.pid), signal.SIGTERM)

    def isPlaying(self) -> bool:
        return self.playing

    def callDelegate(self):
        self.playing = False
        if not self.stopCalled:
            self.delegate.onFinished()
        else:
            self.delegate.onStopped()

    def runThreadedPlayback(
        self,
        onExit,
        command,
        stdout=None,
        shell=False,
        preexec_fn=os.setsid
    ):
        """
        Runs the given command in a subprocess.Popen, and then calls t
        he function onExit when the subprocess completes.
        """
        def runPlayerThread(
            caller,
            onExit,
            command,
            stdout,
            shell,
            preexec_fn
        ):

            try:
                proc = subprocess.Popen(
                    command,
                    stdout=stdout,
                    shell=shell,
                    preexec_fn=preexec_fn
                    )
            except Exception:
                pass

            caller.playerProcessMutex.acquire()
            caller.playerProcess = proc
            caller.playerProcessMutex.release()

            proc.wait()
            onExit()
            return

        stdout = stdout if stdout else open(os.devnull, 'wb')

        thread = threading.Thread(
            target=runPlayerThread,
            args=(self, onExit, command, stdout, shell, preexec_fn)
            )
        thread.start()
        # returns immediately after the thread starts
        return thread
