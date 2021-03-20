from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel


class SettingsScreen(Screen):

    def __init__(self, stored_data, **kwargs):
        super().__init__(**kwargs)
        self.stored_data = stored_data
        self.dialog = None
        self.content = Content()
        self.profiles = self.stored_data.get("profiles")["profiles"]
        self.current_profile = self.stored_data.get("current_profile")["current_profile"]

        self.statistics = self.stored_data.get("statistics")
        self.current_statistics = self.stored_data.get("statistics").get(self.current_profile, [])

        self.content.content_mdtext_field.text = ""
        self.dropdown = DropDown()
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.btn, 'text', x))
        self.stat_box = StatBox()

    def get_current_statistic(self):
        return self.stored_data.get("statistics")[self.current_profile]

    def add_to_stat(self, stat):
        if self.current_profile:
            self.current_statistics.append(stat)
            self.statistics[self.current_profile] = self.current_statistics
            self.stored_data.put('statistics', **self.statistics)


            lb = StatLabel(text=stat)
            self.stat_box.add_widget(lb)

    def init_stat(self):
        self.stat_box.bind(minimum_height=self.stat_box.setter('height'))
        self.stat_scroll.add_widget(self.stat_box)
        self.set_stat()

    def set_stat(self):
        self.stat_box.clear_widgets()
        if self.current_profile:
            for s in self.current_statistics:
                lb = StatLabel(text=s)
                self.stat_box.add_widget(lb)

    def init_profiles(self):
        self.profiles_btn = {}
        for p in self.profiles:
            self.add_profile(p)
        if self.current_profile:
            self.current_statistics = self.stored_data.get("statistics")[self.current_profile]
            self.dropdown.select(self.current_profile)
        else:
            self.btn.text = "создай профиль"

    def del_profile(self, *profile):

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
                self.btn.text = "создай профиль"
                self.stored_data.put('current_profile', current_profile="")
                self.stat_box.clear_widgets()

    def set_profile(self, profile):
        self.current_profile = profile
        self.current_statistics = []
        self.statistics[self.current_profile] = self.current_statistics
        self.stored_data.put('statistics', **self.statistics)
        self.set_stat()
        self.add_profile(profile)

    def add_profile(self, profile):
        self.profiles_btn[profile] = RectButton(text=profile)
        self.profiles_btn[profile].bind(on_release=lambda btn: self.select_profile(btn.text))
        self.stored_data.put('current_profile', current_profile=self.current_profile)
        self.dropdown.add_widget(self.profiles_btn[profile])
        self.btn.text = profile

    def select_profile(self, text):
        self.current_profile = text
        self.stored_data.put('current_profile', current_profile=text)
        self.current_statistics = self.stored_data.get("statistics")[text]
        self.dropdown.select(text)
        self.set_stat()
        print("!!!!!")
        MDApp.get_running_app().screen_manager.start_screen.reset()

    def open_list(self, btn):
        self.dropdown.open(btn)

    def show_confirmation_dialog(self):

        if not self.dialog:
            self.dialog = MDDialog(
                title="Новый профиль:",
                type="custom",
                content_cls=self.content,
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=(0, 0, 0, 0), on_press=self.dialog_cancel
                    ),
                    MDFlatButton(
                        text="OK", text_color=(0, 0, 0, 0), on_press=self.dialog_ok
                    ),
                ],
            )
        self.dialog.open()

    def dialog_ok(self, *args):
        profile = self.content.content_mdtext_field.text
        if profile:
            self.set_profile(profile)
            self.profiles.append(profile)
            self.stored_data.put('profiles', profiles=self.profiles)
        self.content.content_mdtext_field.text = ""
        self.dialog.dismiss(force=True)

    def dialog_cancel(self, *args):
        print("dialog_cancel")
        self.dialog.dismiss(force=True)


class Content(BoxLayout):
    pass


class StatLabel(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            print(self.text)


class RectButton(MDRectangleFlatButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class StatBox(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
