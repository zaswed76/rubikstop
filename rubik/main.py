__version__ = "0.1.07"

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, FadeTransition, SwapTransition, FallOutTransition
from kivymd.app import MDApp

from screens.settings_screen import SettingsScreen
from screens.start_screen import StartScreen
from kivy.core.window import Window
Window.clearcolor = 0, 25/255, 33/255, 1
Builder.load_file("kv/start_screen.kv")
stored_data = JsonStore('data.json')


class MScreenManager(ScreenManager):
    def __init__(self, stored_data, **kwargs):
        super().__init__(**kwargs)
        self.stored_data = stored_data
        self._init_start_screen()
        self._init_settings_screen()

    def _init_start_screen(self):
        self.start_screen = StartScreen(self.stored_data, name="start_screen")
        self.add_widget(self.start_screen)

    def _init_settings_screen(self):
        self.settin_gsscreen = SettingsScreen(self.stored_data, name="settings_screen")
        self.settin_gsscreen.init_profiles()
        self.settin_gsscreen.init_stat()
        # self.settin_gsscreen.init_profiles()

        self.add_widget(self.settin_gsscreen)


class RubikApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.screen_manager = MScreenManager(stored_data, transition=FadeTransition())
        # self.screen_manager = MScreenManager(stored_data, transition=FallOutTransition())
        return self.screen_manager

    def on_start(self):
        self.set_indicator()
        Clock.schedule_interval(self.screen_manager.start_screen.update_time, 0)

    def set_indicator(self):
        self.screen_manager.start_screen.left_btn.init_indicator()
        # self.screen_manager.start_screen.right_btn.init_indicator()


if __name__ == '__main__':
    RubikApp().run()
