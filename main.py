from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDIcon
import thread6
import pyttsx3
from plyer import filechooser
engine=pyttsx3.init()
Window.size=(480,720)
class Dialog_Content(BoxLayout):
    pass
class Click_Icon(ButtonBehavior, MDIcon):
    pass
class Interface(FloatLayout):
    def exporting(self, location):
        print(location[0])
        objects = self.dialog.content_cls.children
        file_name=objects[0].text
        original_text=self.ids.input_text.text
        location_new=str(location[0])+"\\"+file_name+".mp3"
        voices = engine.getProperty('voices')
        if self.ids.female.active:
            engine.setProperty('voice', voices[0].id)
        elif self.ids.male.active:
            engine.setProperty('voice', voices[1].id)
        engine.save_to_file(text=original_text, filename=location_new)
        engine.runAndWait()
        self.dialog.dismiss()
    def selection(self, instances):
        filechooser.choose_dir(title="Select Folder For Output Audio", on_selection=self.exporting)
    def exporting_menu(self):
        self.dialog=MDDialog(
            size_hint=[.8, None],
            title="Filename Here",
            type="custom",
            content_cls= Dialog_Content(),
            buttons=[MDRaisedButton(text="Export", on_release=self.selection)]
        )
        self.dialog.open()

    def running(self):
        voices=engine.getProperty('voices')
        if self.ids.female.active:
            engine.setProperty('voice', voices[0].id)
        elif self.ids.male.active:
            engine.setProperty('voice', voices[1].id)
        engine.say(self.ids.input_text.text)
        engine.runAndWait()
        self.ids.icon_btn.icon = "play.png"
    def changing(self):
        if self.ids.icon_btn.icon=="play.png":
            #process=threading.Thread(target=self.running)
            #process.start()
            thread6.run_threaded(self.running)
            self.ids.icon_btn.icon="pause.png"
        else:
            self.ids.banner.show()
    def closing(self):
        self.ids.banner.hide()
class TtsApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette="Pink"
        self.theme_cls.theme_style="Light"

TtsApp().run()