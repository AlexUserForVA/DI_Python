import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label

from gui_interfaces.IGUIService import IGUIService


class KivyApp(App, IGUIService):

    def build(self):
        return Label(text='Hello world')

    def startGUI(self):
        KivyApp().run()
