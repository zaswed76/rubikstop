from jnius import autoclass

MediaPlayer = autoclass('android.media.MediaPlayer')


class Sound:
    def __init__(self):
        # self.sound = SoundLoader.load("resource/music/fifa-19-ost-jacob-banks.ogg")
        self.sound = MediaPlayer()
        self.sound.setDataSource("resource/music/aaa.mp3")
        self.sound.prepare()
        self.current_pos = 0

    def load(self, source):
        self.sound.setDataSource(source)
    #
    def play(self):
        if self.sound:
            self.sound.start()
    #
    def load_play(self, source):
        self.load(source)
        self.play()
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


