import threading
import json
import numpy as np

from array import array

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.texture import Texture
from kivy.garden.knob import Knob
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.properties import ListProperty, ObjectProperty
from utils.utils import getScreenResolution

from viewer.IViewer import IViewer
from model.IModel import IModel
from controller.IController import IController

class RootWidget(FloatLayout):
    prob_list = ListProperty([100, 100, 100, 100, 100])
    class_list = ListProperty(['-', '-', '-', '-', '-'])

    def setModel(self, model):
        self.model = model

    def start_second_thread(self):
        self.but_1.disabled = True
        self.but_2.disabled = False
        threading.Thread(target=self.second_thread).start()

    def second_thread(self):
        self.model.subscribe(App.get_running_app())
        self.model.run()

    @mainthread
    def update_Spectrogram_Image(self, image):
        image_texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='rgb')
        arr = array('B', image.flatten())
        image_texture.blit_buffer(arr, colorfmt='rgb', bufferfmt='ubyte')
        self.img_texture.texture = image_texture

    @mainthread
    def update_Class_Prob_Bar(self, label, width, index):
        self.class_list[index] = label
        self.prob_list[index] = width

class MainApp(App, IViewer):

    kv_directory = 'viewer/kv'

    screen_width, screen_heigth = getScreenResolution()
    window_width, window_heigth = screen_width / 1.5, screen_heigth / 1.4
    Window.size = (window_width, window_heigth)

    def __init__(self, model, **kwargs):
        super(MainApp, self).__init__(**kwargs)

        if not isinstance(model, IModel):
            raise TypeError('model must be an implementation of IModel')

        self.model = model

    def build(self):
        self.window = RootWidget()
        self.window.setModel(self.model)
        return self.window

    def registerController(self, controller):

        if not isinstance(controller, IController):
            raise TypeError('model must be an implementation of IModel')

        self.controller = controller

    ### IViewer method overrides ###

    def onSpectrogramChanged(self, spectrogram):
        self.window.update_Spectrogram_Image(spectrogram)

    def onPredictionChanged(self, json_class_probs):
        prob_dict = json.loads(json_class_probs)
        sorted_values = np.argsort(prob_dict.values())
        for i in range(5):
            class_label = prob_dict.keys()[sorted_values[40 - i]]
            class_width = prob_dict.values()[sorted_values[40 - i]] * 350
            self.window.update_Class_Prob_Bar(class_label, class_width, i)

    ### On controller widget changed - functions ###
    def speedSliderEvent(self, value):
        value = int(value)
        if value < 100 and value > 90:
            self.window.speedKnobLabel.text = 'Realtime'
            self.window.speedKnobLabel.color = 0.96, 0.76, 0.28, 1
        else:
            self.window.speedKnobLabel.text = str(value)
            self.window.speedKnobLabel.color = 0.7, 0.7, 0.7, 1

        self.controller.onSpeedChanged(100 - value)

