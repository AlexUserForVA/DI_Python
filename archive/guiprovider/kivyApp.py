import kivy
kivy.require('1.0.6') # replace with your current kivy version !

import threading

from kivy.app import App
from kivy.clock import mainthread
from kivy.properties import ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

# from audiotaggerwindow import AudioTaggerWindow
from archive.spectrogramprovider.SpectrogramProvider import SpectrogramProvider
from viewer.utils.utils import getScreenResolution

class AudioTaggerWindow(FloatLayout):


    def startButtonEvent(self, **kwargs):
        threading.Thread(target=self.startSpecCalc()).start()

    def startSpecCalc(self):
        sp = SpectrogramProvider()
        sp.subscribe(App.get_running_app())
        sp.run()

    @mainthread
    def updateSpectrogram(self, spectrogram):
        pass
        # texture = Texture.create(size=(256, 512))
        # arr = array('B', spectrogram)
        # texture.blit_buffer(arr, colorfmt='rgb', bufferfmt='ubyte')
        # self.img_texture = texture

class KivyApp(App):

    kv_directory = 'kv'

    # img_texture = ObjectProperty(None)
    rectangle_width = ListProperty([20, 100, 100, 100, 100])
    class_labels = ListProperty(['-', '-', '-', '-', '-'])

    screen_width, screen_heigth = getScreenResolution()
    window_width, window_heigth = screen_width / 1.5, screen_heigth / 1.5
    Window.size = (window_width, window_heigth)
    output_column = window_width / 2
    control_column = window_width / 2

    def __init__(self, **kwargs):
        super(KivyApp, self).__init__(**kwargs)

    def build(self):
        self.window = AudioTaggerWindow()
        return self.window

    '''
    def getCurrentSpectrogram(self, dt):
        # binaryImg = self.spectrogramProvider.getCurrentSpectrogramImage()
        data = io.BytesIO(open('spectrogramprovider/mock_data/mercedes.png', 'rb').read())
        self.img_texture = Image(data, ext='png').texture

    def getCurrentPrediction(self, dt):
        output_probabilities_json = self.predictorProvider.predict(2)
        prob_dict = json.loads(output_probabilities_json)
        sorted_values = np.argsort(prob_dict.values())
        for i in range(5):
            self.class_labels[i] = prob_dict.keys()[sorted_values[40 - i]]
            self.rectangle_width[i] = prob_dict.values()[sorted_values[40 - i]] * self.output_column
    '''

    def spectrogramHasChanged(self, spectrogram):
         self.window.updateSpectrogram(spectrogram)
if __name__ == '__main__':
    KivyApp().run()
