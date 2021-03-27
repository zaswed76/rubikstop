import os

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.filemanager import MDFileManager
# SDcard Android
from kivymd.uix.slider import MDSlider

from screens.playlist import RV
from kivy.utils import platform
import os


class MDIconButtonChecked(MDIconButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options = {"icon": self.change_icon, "color": self.change_color}
        self.change_options = {"text_color": {"checked": (1, 0, 0, 1), "unchecked": (0, 1, 0, 1)}}
        self._checked = False
        self._change_property_list = []

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, v):
        self._checked = v


    def set_change_property_list(self, prop=None, checked=None, unchecked=None):
        self._change_property_list.append([prop, checked, unchecked])

    @property
    def change_property_list(self):
        return self._change_property_list

    def on_pressed_change(self, opt):
        self.opt = opt

    def change_icon(self, checked, unchecked):
        self.icon = checked if self.checked else unchecked

    def change_color(self, checked, unchecked):
        self.text_color = checked if self.checked else unchecked

    def on_press(self, *args):
        self.checked = not self.checked
        for opt in self.change_property_list:
            self.options[opt[0]](opt[1], opt[2])
        print(args)
        if not args:
            if self._checked:

                MDApp.get_running_app().screen_manager.start_screen.play_sound_btn.on_press("auto")
            else:
                MDApp.get_running_app().screen_manager.start_screen.play_sound_btn.on_press("auto")

class MusicScreen(Screen):
    def __init__(self, stored_data, audio, play_list, **kwargs):
        super().__init__(**kwargs)

        self.audio = audio
        self.audio.parent = self
        self.is_play = False

        self.file_manager = MDFileManager(
            exit_manager=self.not_choose_music,
            select_path=self.choose_music_folder,
            preview=False,
        )
        self.ext_list = [".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a"]
        self.stored_data = stored_data

        if play_list is not None:
            self.play_list = play_list
        else:
            self.play_list = []

        self.set_view_data(self.play_list)
        self.stop()
        self._init_slider()

        self.current_index = 0
        self.player_start_flag = False
        # Clock.schedule_interval(self._on_position, 0.0)

    def choose_folder_music(self):
        print(App.get_running_app().user_data_dir)
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
        if self.play_list:
            if self.audio:
                # self.audio.unload()
                self.audio.stop()
                self.audio.load(self.play_list[0])

        else:
            if self.audio:
                self.audio.unload()
                self.audio.stop()

        self.set_view_data(self.play_list)
        self.stored_data.put("playlist", playlist=self.play_list)
        # self.audio.load("")
        # self.audio.stop()

    def set_view_data(self, data):
        t = [{"text": os.path.basename(x), 'selected': False} for x in data]
        self.play_list_view.data = t

    def get_next_source(self):
        self.current_index += 1
        return self.play_list[self.current_index]

    def not_choose_music(self, *args):
        self.file_manager.close()

    def load(self, p):
        self.audio.load(p)

    def play(self, name=None):
        if name is not None:
            p = self.load_name(name)
            if p and os.path.isfile(p):
                self.is_play = self.audio.play(p)
        else:
            print("111111")
            self.is_play = self.audio.play()
            self.audio.set_volume(self.pos_slider.value)
        if self.is_play:
            App.get_running_app().screen_manager.start_screen.play_sound_btn.check = True

    def stop(self):
        self.audio.stop()
        self.player_start_flag = False

    def pause(self):
        p = self.audio.pause()

    def load_name(self, name):
        for n, p in enumerate(self.play_list):
            self.current_index = n

            if name in p:
                return p

    def _init_slider(self):
        self.pos_slider = MDSlider()
        self.pos_slider.bind(value=self.on_slider_value_change)

        self.pos_slider.min = 0
        self.pos_slider.max = 1
        self.pos_slider.value = 0.3
        self.pos_slider.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.pos_slider.size_hint = 0.6, 1
        self.pos_slider.background_color = 1, 0, 0, 1

        self.pos_slider.hint = False
        self.pos_slider.step = 0.02
        self.pos_slider.orientation = 'horizontal'
        self.pos_slider.color = 0, 0.294, 0.352, 1
        self.play_tool_layout.add_widget(self.pos_slider)

    def set_value_slider(self, v):
        self.pos_slider.value = v

    def on_slider_value_change(self, instance, value):

        self.audio.set_volume(value)
        if value > 0:
            self.volume_high.text_color = 0, 75 / 255, 90 / 255, 1
            self.volume_mute.text_color = 0, 40 / 255, 50 / 255, 1
        else:
            self.volume_high.text_color = 0, 40 / 255, 50 / 255, 1
            self.volume_mute.text_color = 0, 75 / 255, 90 / 255, 1
