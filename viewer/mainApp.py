import threading
import json
import numpy as np

from array import array

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.texture import Texture
from kivy.properties import ListProperty, ObjectProperty

from viewer.IViewer import IViewer
from model.IModel import IModel
from model.audiotaggermodel import AudioTaggerModel

class RootWidget(FloatLayout):

    image_texture = ObjectProperty()
    prob_list = ListProperty([100, 100, 100, 100, 100])
    class_list = ListProperty(['-', '-', '-', '-', '-'])

    def setModel(self, model):
        self.model = model

    def start_second_thread(self):
        threading.Thread(target=self.second_thread).start()

    def second_thread(self):
        self.model.subscribe(App.get_running_app())
        self.model.run()

    @mainthread
    def update_Spectrogram_Image(self, image):
        image_texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='rgb')
        arr = array('B', image.flatten())
        image_texture.blit_buffer(arr, colorfmt='rgb', bufferfmt='ubyte')
        self.image_texture = image_texture

    def update_Class_Prob_Bar(self, label, width, index):
        self.class_list[index] = label
        self.prob_list[index] = width

class MainApp(App, IViewer):

    kv_directory = 'viewer/kv'

    def __init__(self, model, **kwargs):
        super(MainApp, self).__init__(**kwargs)

        if not isinstance(model, IModel):
            raise TypeError('model must be an implementation of IModel')

        self.model = model

    def build(self):
        self.window = RootWidget()
        self.window.setModel(self.model)
        return self.window

    ### IViewer method overrides ###

    def onSpectrogramChanged(self, spectrogram):
        self.window.update_Spectrogram_Image(spectrogram)

    def onPredictionChanged(self, json_class_probs):
        prob_dict = json.loads(json_class_probs)
        sorted_values = np.argsort(prob_dict.values())
        for i in range(5):
            class_label = prob_dict.keys()[sorted_values[40 - i]]
            class_width = prob_dict.values()[sorted_values[40 - i]] * 500
            self.window.update_Class_Prob_Bar(class_label, class_width, i)