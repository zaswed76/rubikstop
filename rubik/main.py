import os

__version__ = "0.1.85"
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivymd.app import MDApp
# import kivy


from screens.settings_screen import SettingsScreen
from screens.start_screen import StartScreen
from screens.music_screen import MusicScreen
from kivy.utils import platform

Window.allow_screensaver = False

if platform == 'android':
    try:
        from android.permissions import request_permissions, Permission
        from core.android_audioplayer import Sound

        request_permissions([Permission.WRITE_EXTERNAL_STORAGE])

    except:
        Sound = None
else:
    from core.audioplayer import Sound

    Window.size = (700, 400)

Builder.load_file("kv/start_screen.kv")
stored_data = JsonStore('data.json')


class MScreenManager(ScreenManager):
    def __init__(self, stored_data, **kwargs):
        super().__init__(**kwargs)
        self.stored_data = stored_data

        self._init_start_screen()
        self._init_settings_screen()
        self._init_music_screen()

    def _init_music_screen(self):
        play_list = [x for x in self.stored_data.get("playlist").get("playlist", []) if os.path.isfile(x)]
        if play_list:
            track = play_list[0]
        else:
            track = None
        self.audio = Sound(start_track=track)

        self.music_screen = MusicScreen(self.stored_data, self.audio, play_list, name="music_screen")

        self.add_widget(self.music_screen)

    def _init_start_screen(self):
        self.start_screen = StartScreen(self.stored_data, name="start_screen")
        self.add_widget(self.start_screen)

    def _init_settings_screen(self):
        self.settin_gsscreen = SettingsScreen(self.stored_data, name="settings_screen")
        self.settin_gsscreen.init_profiles()
        self.settin_gsscreen.init_stat()
        # self.settin_gsscreen.init_profiles()

        self.add_widget(self.settin_gsscreen)

    def set_screen(self, screen):

        self.current = screen
        self.music_screen.play_list_view.selectedItem = 0
        try:
            self.music_screen.play_list_view.select(0)
        except IndexError:
            pass


class RubikApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.screen_manager = MScreenManager(stored_data, transition=FadeTransition())

    def get_version(self):
        return __version__

    def build(self):

        profile = self.screen_manager.settin_gsscreen.current_profile
        if profile:
            self.screen_manager.start_screen.profile_label.text = profile
        else:
            self.screen_manager.start_screen.profile_label.text = "создай\nпрофиль"
        self.screen_manager.current = "start_screen"
        self.screen_manager.start_screen.update_stat(True)

        return self.screen_manager

    def on_start(self):
        self.set_indicator()
        Clock.schedule_interval(self.screen_manager.start_screen.update_time, 0)

    def set_indicator(self):
        self.screen_manager.start_screen.left_btn.init_indicator()
        # self.screen_manager.start_screen.right_btn.init_indicator()


if __name__ == '__main__':
    RubikApp().run()
