import threading

from array import array

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.texture import Texture

from spectrogramprovider.SpectrogramProvider import SpectrogramProvider


class RootWidget(FloatLayout):
    # stop = threading.Event()

    def start_second_thread(self):
        threading.Thread(target=self.second_thread).start()

    def second_thread(self):
        # Remove a widget, update a widget property, create a new widget,
        # add it and animate it in the main thread by scheduling a function
        # call with Clock.

        sp = SpectrogramProvider()
        sp.subscribe(App.get_running_app())
        sp.run()

    @mainthread
    def update_Spectrogram_Image(self, image):
        image_texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='rgb')
        arr = array('B', image.flatten())
        image_texture.blit_buffer(arr, colorfmt='rgb', bufferfmt='ubyte')

        self.spec_1.texture = image_texture

class MainApp(App):

    kv_directory = 'kv'

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)

    def build(self):
        self.window = RootWidget()
        return self.window

    def spectrogramHasChanged(self, spectrogram):
        self.window.update_Spectrogram_Image(spectrogram)


if __name__ == '__main__':
    MainApp().run()