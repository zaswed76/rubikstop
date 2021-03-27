
from jnius import PythonJavaClass, autoclass, java_method, cast
MediaPlayer = autoclass('android.media.MediaPlayer')


class SoundCompletionCallback(PythonJavaClass):
    # http://developer.android.com/reference/android/media/MediaPlayer.OnCompletionListener.html
    __javainterfaces__ = ('android.media.MediaPlayer$OnCompletionListener', )

    def __init__(self, callback):
        super(SoundCompletionCallback, self).__init__()
        self.callback = callback

    @java_method('(Landroid/media/MediaPlayer;)V')
    def onCompletion(self, mp):
        self.callback(mp)

class Sound:
    def __init__(self, start_track=None):
        self.sound = MediaPlayer()
        self.current_pos = 0
        self._complete_callback = SoundCompletionCallback(self.on_completion)
        self.sound.setOnCompletionListener(self._complete_callback)
        self.parent = None

    def on_completion(self, *mp):
        self.parent.play(self.parent.get_next_source())

    def load(self, source):
        self.sound.setDataSource(source)
        self.sound.prepare()
    #
    def play(self, name=None):
        self.sound.reset()
        if name is not None:
            self.load(name)
        if self.sound:
            self.sound.start()
    #
    def load_play(self, source):
        self.load(source)
        # self.play()
    #
    def stop(self):
        if self.sound:
            self.sound.stop()

    def pause(self):
        if self.sound:
            if self.sound.isPlaying():
                self.sound.pause()
            else:
                self.play()

    def set_volume(self, volume):
        self.sound.setVolume(volume)

    def unload(self):
        self.sound.reset()


