import datetime
import threading

from kivy.base import stopTouchApp
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.button import MDRectangleFlatButton, MDTextButton, MDIconButton
from kivymd.uix.label import MDLabel

TOP1_FORMAT = "рекорд         {}"
TOP2_FORMAT = "2-e место    {}"
CURRENT_FORMAT = "текущее      {}"
MEAN_FORMAT = "среднее       {}"
NEW_TOP_FORMAT = "НОВЫЙ РЕКОРД !!!\nбыстрее на {} сек."
STAT_COUNT_FORMAT = "СБОРОК         {}"


def float_to_time_str(fl):
    m, sm = str(datetime.timedelta(seconds=fl)).split(":")[1:]
    s, ml = sm.split(".")
    return ":".join([m, s, str(ml)[:2]])




class MDIconButtonExit(MDIconButton, TouchBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_double_tap(self, touch, *args):
        if self.collide_point(*touch.pos):
            stopTouchApp()


class PlaySoundBtn(MDIconButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._check = False

    @property
    def check(self):
        return self._check

    @check.setter
    def check(self, v):
        self._check = v
        if self._check:

            self.icon = "pause-circle-outline"
        else:
            self.icon = "play-outline"

    def on_press(self, *args):
        self.check = not self.check
        if self.check:
            self.icon = "pause"

            MDApp.get_running_app().screen_manager.music_screen.pause()
            if not args:
                MDApp.get_running_app().screen_manager.music_screen.play_pause_btn.on_press("auto")
        else:
            self.icon = "play-outline"
            MDApp.get_running_app().screen_manager.music_screen.pause()
            if not args:
                MDApp.get_running_app().screen_manager.music_screen.play_pause_btn.on_press("auto")


class StartButton(MDRectangleFlatButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ProfileLabel(MDLabel, TouchBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_double_tap(self, touch, *args):
        # print(touch.pos)
        if self.collide_point(*touch.pos):
            MDApp.get_running_app().screen_manager.current = "settings_screen"
            super().on_double_tap(touch, *args)


class SButton(MDTextButton, TouchBehavior):
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
                if self.start_screen.sw_seconds > 0.5:
                    self.start_screen.stop()
                    SButton.session = False
                    self.set_indicator("red")
                    self.app.screen_manager.settin_gsscreen.add_to_stat(self.start_screen.stopwatch.text,
                                                                        self.start_screen.sw_seconds)
                else:
                    self.app.screen_manager.start_screen.sw_seconds = 0
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
        self.app = MDApp.get_running_app()
        self.stored_data = stored_data
        self.left_down = False
        self.right_down = False
        self.session_count = 0
        self.session = False
        # self.webThread = threading.Thread(target=self.start)
        # self.webThread.daemon = True



    def clear_stopwatch_label(self):
        self.reset()
        # self.stopwatch.text = '00:00.00'


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

        else:
            self.right_down = False
        # print(self.session_count)


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


    def update_stat(self, start_flag):
        stat = self.app.screen_manager.settin_gsscreen.current_statistics
        if stat:

            stat_dict = self.app.screen_manager.settin_gsscreen.detailed_stat.top_places(stat)
            self.stat_top1_label.text = TOP1_FORMAT.format(stat_dict["top"][0])
            self.stat_current_label.text = CURRENT_FORMAT.format(stat_dict["current"])
            self.stat_count_label.text = STAT_COUNT_FORMAT.format(len(stat))
            if len(stat) > 1:
                self.stat_top2_label.text = TOP2_FORMAT.format(stat_dict["top"][1])
            self.stat_mean_label.text = MEAN_FORMAT.format(float_to_time_str(stat_dict["mean"]))
            new_rec = stat_dict["new_top"]
            # print(new_rec, "3333")
            if new_rec >= 0 and not start_flag:
                self.stat_new_top.text = NEW_TOP_FORMAT.format(new_rec)
            else:
                self.stat_new_top.text = ""
        else:
            self.stat_count_label.text = STAT_COUNT_FORMAT.format(len(stat))
            self.clear_stat()


    def clear_stat(self):
        self.stat_top1_label.text = TOP1_FORMAT.format("")
        self.stat_current_label.text = CURRENT_FORMAT.format("")
        self.stat_top2_label.text = TOP2_FORMAT.format("")
        self.stat_mean_label.text = MEAN_FORMAT.format("")
        self.stat_new_top.text = ""
        self.stat_count_label.text = STAT_COUNT_FORMAT.format("0")
