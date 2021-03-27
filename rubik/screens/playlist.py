from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivymd.app import MDApp


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            MDApp.get_running_app().screen_manager.music_screen.play(
                MDApp.get_running_app().screen_manager.music_screen.play_list_view.data[self.index]["text"])
            MDApp.get_running_app().screen_manager.music_screen.play_pause_btn.on_press("auto")
            # MDApp.get_running_app().screen_manager.start_screen.play_sound_btn.on_press("auto")
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        # if is_selected:
        #     # print(self.parent.get_selectable_nodes(), "5555")
        #     MDApp.get_running_app().screen_manager.music_screen.play(rv.data[index]["text"])



class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        self.selectedItem = 0

    def clearAll(self):
        for i in self.view_adapter.views:
            self.view_adapter.views[i].selected = 0



    def select(self, i):
        self.selectable_box.select_node(i)



