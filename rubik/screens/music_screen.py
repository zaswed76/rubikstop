from kivy.uix.screenmanager import Screen


class MusicScreen(Screen):
    def __init__(self, stored_data, audio, **kwargs):
        super().__init__(**kwargs)
        self.audio = audio
        print(self.audio)
        self.stored_data = stored_data