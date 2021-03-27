import datetime

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel


class DetailedStat:
    def __init__(self):
        self.stats = {}

    def top_places(self, _st=None, places=2):
        self.stats.clear()

        stats = sorted(_st, key=lambda i: i[0])
        _rec = sorted(stats, key=lambda i: i[0])
        rec = _rec[0]

        cur = _st[0]
        if rec == cur:
            try:
                new_rec = _rec[1][0] - cur[0]
            except IndexError:
                new_rec = cur[0] - 0
        else:
            new_rec = rec[0] - cur[0]
        # print(rec, cur, "rec, cur")

        self.stats["current"] = _st[0][-1].split(" ")[-1].replace('<','').replace('>','')

        st = [x[1].split(" ")[-1].replace('<','').replace('>','') for x in stats]
        self.stats["top"] = st[:places]
        self.stats["new_top"] = round(new_rec, 2)
        self.stats["pop"] = st[-1]
        self.stats["mean"] = round(sum([x[0] for x in stats]) / len(stats), 2)

        return self.stats



class SettingsScreen(Screen):

    def __init__(self, stored_data, **kwargs):
        super().__init__(**kwargs)
        self.detailed_stat = DetailedStat()
        self.stored_data = stored_data
        self.dialog = None
        self.del_dialog = None
        self.content = Content()
        self.profiles = self.stored_data.get("profiles")["profiles"]
        self.current_profile = self.stored_data.get("current_profile")["current_profile"]

        self.statistics = self.stored_data.get("statistics")
        self.current_statistics = self.stored_data.get("statistics").get(self.current_profile, [])
        # print(self.current_statistics, "11111")

        self.content.content_mdtext_field.text = ""
        self.dropdown = DropDown()
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.btn, 'text', x))
        self.stat_box = StatBox()
        self.app = MDApp.get_running_app()
        self.version_label.text = self.app.get_version()

    def get_current_statistic(self):
        return self.stored_data.get("statistics")[self.current_profile]

    def del_stat(self, stat):

        for n in self.current_statistics:
            print(n, "!!!!")
            if stat in n:
                self.current_statistics.remove(n)
        self.app.screen_manager.start_screen.reset()
        self.app.screen_manager.start_screen.update_stat(False)



    def add_to_stat(self, stat, *args):
        """

        :type args: tuple: args[0] = <float>время
        """
        if self.current_profile:
            today = datetime.datetime.today()
            t = today.strftime("%Y-%m-%d %H.%M.%S")
            format_res = "{}  <{}>".format(t, stat)
            res = [args[0], format_res]
            self.current_statistics.insert(0, res)
            self.statistics[self.current_profile] = self.current_statistics
            self.stored_data.put('statistics', **self.statistics)

            lb = StatLabel(text=format_res)

            self.stat_box.add_widget(lb, len(self.stat_box.children))
            self.app.screen_manager.start_screen.update_stat(False)




    def init_stat(self):
        self.stat_box.bind(minimum_height=self.stat_box.setter('height'))
        self.stat_scroll.add_widget(self.stat_box)
        self.set_stat()

    def set_stat(self):
        self.stat_box.clear_widgets()
        if self.current_profile:
            # print(self.current_statistics)
            for s in self.current_statistics:
                lb = StatLabel(text=s[1])
                self.stat_box.add_widget(lb)

    def init_profiles(self):
        self.profiles_btn = {}
        for p in self.profiles:
            self.add_profile(p)
        if self.current_profile:
            self.current_statistics = self.stored_data.get("statistics")[self.current_profile]
            self.dropdown.select(self.current_profile)
        else:
            self.btn.text = "создай\nпрофиль"

    def del_profile(self, *profile):
        self.del_dialog.dismiss(force=True)
        if self.current_profile:
            del (self.statistics[self.current_profile])
            # self.statistics[self.current_profile] = self.current_statistics
            self.stored_data.put('statistics', **self.statistics)

            self.profiles.remove(self.current_profile)
            self.dropdown.remove_widget(self.profiles_btn[self.current_profile])
            del (self.profiles_btn[self.current_profile])
            self.stored_data.put('profiles', profiles=self.profiles)
            try:

                self.select_profile(self.profiles[-1])

            except IndexError:
                self.current_profile = ""
                self.btn.text = "создай\nпрофиль"
                self.stored_data.put('current_profile', current_profile="")
                self.stat_box.clear_widgets()
                self.app.screen_manager.start_screen.profile_label.text = "создай\nпрофиль"
                self.app.screen_manager.start_screen.clear_stat()
                self.app.screen_manager.start_screen.clear_stopwatch_label()

    def set_profile(self, profile):
        self.current_profile = profile
        self.current_statistics = []
        self.statistics[self.current_profile] = self.current_statistics
        self.stored_data.put('statistics', **self.statistics)
        self.set_stat()
        self.add_profile(profile)
        self.app.screen_manager.start_screen.clear_stat()


    def add_profile(self, profile):
        self.profiles_btn[profile] = RectButton(text=profile)
        self.profiles_btn[profile].bind(on_release=lambda btn: self.select_profile(btn.text))
        self.stored_data.put('current_profile', current_profile=self.current_profile)
        self.dropdown.add_widget(self.profiles_btn[profile])
        self.btn.text = profile

        try:
            self.app.screen_manager.start_screen.profile_label.text = self.current_profile
        except AttributeError:
            pass

    def select_profile(self, text):
        self.current_profile = text
        self.stored_data.put('current_profile', current_profile=text)
        self.current_statistics = self.stored_data.get("statistics")[text]
        self.dropdown.select(text)
        self.set_stat()

        self.app.screen_manager.start_screen.reset()
        self.app.screen_manager.start_screen.profile_label.text = self.current_profile
        self.app.screen_manager.start_screen.update_stat(True)

    def open_list(self, btn):
        self.dropdown.open(btn)

    def show_confirmation_dialog(self):

        if not self.dialog:
            self.dialog = MDDialog(
                pos_hint={"center_x": 0.5, "center_y": 0.7},
                title="Новый профиль:",
                type="custom",
                content_cls=self.content,
                buttons=[
                    MDFlatButton(
                        text="ОТМЕНА", text_color=(0, 0, 0, 0), on_press=self.dialog_cancel
                    ),
                    MDFlatButton(
                        text="СОЗДАТЬ", text_color=(0, 0, 0, 0), on_press=self.dialog_ok
                    ),
                ],
            )
        self.dialog.open()

    def show_delit_dialog(self):

        if not self.del_dialog:
            self.del_dialog = MDDialog(
                pos_hint={"center_x": 0.5, "center_y": 0.7},
                title="Внимание",
                text="""Удаление профиля прведёт к удалению\nстатистики c ним связанной!""",
                buttons=[
                    MDFlatButton(
                        text="ОТМЕНА", text_color=(0, 0, 0, 1), on_press=self.dialog_del_cancel
                    ),
                    MDFlatButton(
                        text="УДАЛИТЬ", text_color=(0, 0, 0, 1), on_press=self.del_profile
                    ),
                ],
            )
        self.del_dialog.open()

    def dialog_ok(self, *args):
        profile = self.content.content_mdtext_field.text[:14]

        if profile:
            self.set_profile(profile)
            self.profiles.append(profile)
            self.stored_data.put('profiles', profiles=self.profiles)
        self.content.content_mdtext_field.text = ""
        self.dialog.dismiss(force=True)

    def dialog_cancel(self, *args):

        self.dialog.dismiss(force=True)

    def dialog_del_cancel(self, *args):
        self.del_dialog.dismiss(force=True)


class Content(BoxLayout):
    pass


class StatLabel(MDLabel, TouchBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            pass
            print(self.text)
            # for w in self.parent.children:
            #     if self.text == w.text:
            #         self.parent.remove_widget(w)
            #         return

    def on_triple_tap(self, touch, *args):
        super().on_double_tap(self, touch, *args)
        if self.collide_point(*touch.pos):
            for w in self.parent.children:
                if self.text == w.text:
                    self.parent.remove_widget(w)
                    self.app.screen_manager.start_screen.reset()
                    self.app.screen_manager.settin_gsscreen.del_stat(self.text)
                    return


class RectButton(MDRectangleFlatButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class StatBox(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
