from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.filemanager import MDFileManager
  # SDcard Android



from screens.playlist import RV
from kivy.utils import platform
import os

class MusicScreen(Screen):
    def __init__(self, stored_data, audio, **kwargs):
        super().__init__(**kwargs)
        self.audio = audio

        self.file_manager = MDFileManager(
            exit_manager=self.not_choose_music,
            select_path=self.choose_music_folder,
            preview=False,
        )
        self.ext_list = [".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a"]
        self.stored_data = stored_data
        self.play_list = self.stored_data.get("playlist").get("playlist", [])


        self.set_view_data(self.play_list)


    def choose_folder_music(self):
        if platform == "android":
            p = '/sdcard'
        else:
            p = "/"
        self.file_manager.show(p)

    def choose_music_folder(self, path):
        self.file_manager.close()
        if path:
            self.play_list.clear()
            for root, dirs, files in os.walk(path):
                for f in files:
                    if os.path.splitext(f)[1] in self.ext_list:
                        mfile = os.path.abspath(os.path.join(root, f))
                        self.play_list.append(mfile)
        self.set_view_data(self.play_list)
        self.stored_data.put("playlist", playlist=self.play_list)

    def set_view_data(self, data):


        t = [{"text": os.path.basename(x), 'selected': False} for x in data]
        self.play_list_view.data = t
        self.stop()



    def not_choose_music(self, *args):
        self.file_manager.close()

    def load(self, p):
        self.audio.load(p)

    def play(self, name):
        p = self.load_name(name)
        if p and os.path.isfile(p):
            self.audio.play(p)

    def stop(self):
        self.audio.stop()

    def pause(self):
        pass

    def load_name(self, name):
        for p in self.play_list:
            if name in p:
                return p


