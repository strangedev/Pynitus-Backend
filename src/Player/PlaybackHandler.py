"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Noah Hummel

    This file is part of the Pynitus program, see <https://github.com/strangedev/Pynitus>.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
