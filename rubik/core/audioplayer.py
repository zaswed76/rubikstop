from kivy.core.audio import SoundLoader


class Sound:
    def __init__(self):
        self.sound = SoundLoader.load("resource/music/aaa.mp3")
        self.current_pos = 0

    def load(self, source):
        self.sound = SoundLoader.load(source)

    def play(self):
        if self.sound:
            self.sound.play()

    def load_play(self, source):
        self.sound = SoundLoader.load(source)
        if self.sound:
            self.sound.play()

    def stop(self):
        if self.sound:
            self.sound.stop()

    def pause(self):
        if self.sound:
            if self.sound.state == "play":
                self.current_pos = self.sound.get_pos()
                # print(self.current_pos)
                self.sound.stop()
            else:
                # print(self.current_pos, "dddd")
                self.sound.play()
                self.sound.seek (self.current_pos)

    def __repr__(self):
        return "SoundLoader Player"
