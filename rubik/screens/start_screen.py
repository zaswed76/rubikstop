from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel


class StartButton(MDRectangleFlatButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # def on_press(self):
    #     self.checked = not self.checked


class SButton(Button, TouchBehavior):
    left_down = False
    right_down = False
    session = False


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.checked = False
        self.duration_long_touch = 1.0
        self.on_touch_up_count = 0

        self.indicators_values = dict(red='resource/sharred.png', green='resource/shar.png',
                                      y='resource/yellow.png')

    def init_indicator(self):
        self.start_screen = self.app.screen_manager.start_screen
        # self.indicators = dict(left=MDApp.get_running_app().screen_manager.start_screen.left_indicator,
        #                        right=MDApp.get_running_app().screen_manager.start_screen.right_indicator)

    def on_touch_down(self, touch):

        self.on_touch_up_count = 0
        if self.collide_point(*touch.pos):
            if SButton.session:
                self.start_screen.stop()
                SButton.session = False
                self.set_indicator("red")
                self.app.screen_manager.settin_gsscreen.add_to_stat(self.start_screen.stopwatch.text)
            super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if not self.on_touch_up_count:
            self.on_touch_up_count += 1
            if self.collide_point(*touch.pos):
                if SButton.session and self.start_screen.stopwatch.text == '00:00.00':
                    self.start_screen.start()
        super().on_touch_up(touch)

    def on_long_touch(self, *args):
        if self.collide_point(*args[0].pos):
            if self.start_screen.stopwatch.text == '00:00.00':
                SButton.session = True
                self.set_indicator("green")
                super().on_long_touch(*args)


    def set_indicator(self, value):
        self.start_screen.left_indicator.source = self.indicators_values[value]


class StopwatchLabel(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_list = []

    def on_touch_move(self, touch):

        if self.collide_point(*touch.pos):
            self.move_list.append(touch.x)
            if self.move_list[0] - self.move_list[-1] > 70:
                MDApp.get_running_app().screen_manager.start_screen.reset()

            super().on_touch_move(touch)

    def on_touch_up(self, touch):
        self.move_list.clear()


class StartScreen(Screen):
    sw_started = False
    sw_seconds = 0

    def __init__(self, stored_data, **kwargs):
        super().__init__(**kwargs)
        self.stored_data = stored_data
        self.left_down = False
        self.right_down = False
        self.session_count = 0
        self.session = False

    def press(self, v):
        if v == "left":
            self.left_down = True
            if self.right_down:
                self.session_count += 1

        if v == "right":
            self.right_down = True

            if self.left_down:
                self.session_count += 1

    def release(self, v):

        if v == "left":
            if not self.right_down and self.session_count % 2:
                self.start()
            self.left_down = False
        #     if not self.right_down and not self.session_count%2:
        #         self.start()
        # if self.right_btn.checked and self.left_btn.checked:
        #     if not self.right_down and not self.session:
        #         self.start()
        #         self.session = True
        #     else:
        #         self.session = False
        # self.left_down = False
        # self.left_btn.checked = False
        # self.right_btn.checked = False
        else:
            self.right_down = False
        print(self.session_count)
        #     # if self.left_btn.checked and self.right_btn.checked:
        #     #     if not self.left_down and not self.session:
        #     #         self.start()
        #     #         self.session = True
        #     #     else:
        #     #         self.session = False
        #     self.right_down = False
        # print("release")

        # print(v, self.left_btn)
        # if v == "left":
        #     self.left_down = False
        # if v == "right" and self.left_down and not self.sw_started:
        #     self.start()

        # print("press", self.left_btn.checked, self.right_btn.checked)
        # if not self.left_btn.checked and not self.right_btn.checked:
        #     self.stop()

    def start(self):
        self.sw_started = True

    def stop(self):
        self.sw_started = False

    def on_start(self):
        Clock.schedule_interval(self.update_time, 0)

    def update_time(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
        minutes, seconds = divmod(self.sw_seconds, 60)
        self.stopwatch.text = (
                '%02d:%02d.%02d' %
                (int(minutes), int(seconds), int(seconds * 100 % 100)))

    def reset(self):
        if self.sw_started:
            self.sw_started = False
        self.sw_seconds = 0
        self.text = '00:00.00'

