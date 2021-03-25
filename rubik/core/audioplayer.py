from kivy.core.audio import SoundLoader, Sound


class MSound(Sound):
    def __init__(self):
        super().__init__()

    def play(self, name):
        print(name)

class Sound:
    def __init__(self):
        self.sound = SoundLoader.load("resource/music/aaa.mp3")

        self.current_pos = 0

    def load(self, source):
        self.sound = SoundLoader.load(source)

    def play(self, name=None):
        if self.sound:
            self.stop()
            if name is not None:
                self.load(name)

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

    def unload(self):
        self.sound.unload()

    def __repr__(self):
        return "SoundLoader Player"



# SoundLoader.register(MSound)