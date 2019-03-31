import threading
import json
import urllib2
import numpy as np
import cv2
import time

import requests
from array import array
from flask import Flask, request, Response

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
from server.IModel import IModel
from controller.IController import IController

class RootWidget(FloatLayout):
    prob_list = ListProperty([100, 100, 100, 100, 100])
    class_list = ListProperty(['-', '-', '-', '-', '-'])

    def setModel(self, model):
        self.model = model

    def start_Button_pressed(self):
        self.but_1.disabled = True
        self.but_2.disabled = False
        Clock.schedule_interval(App.get_running_app().getCurrentSpectrogram, 2)
        # Clock.schedule_interval(App.get_running_app().getCurrentPrediction, 2)

    @mainthread
    def update_Spectrogram_Image(self, image):
        image_texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='rgb')
        arr = array('B', image.flatten())
        image_texture.blit_buffer(arr, colorfmt='rgb', bufferfmt='ubyte')
        self.img_texture.texture = image_texture
        print(time.time())

    @mainthread
    def update_Class_Prob_Bar(self, label, width, index):
        self.class_list[index] = label
        self.prob_list[index] = width

class MainApp(App, IViewer):

    kv_directory = 'viewer/kv'

    screen_width, screen_heigth = getScreenResolution()
    window_width, window_heigth = screen_width / 1.5, screen_heigth / 1.4
    Window.size = (window_width, window_heigth)

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)

        self.predList = self.loadConfig()
        x = 2

    def getPredList(self):
        return self.predList

    def build(self):
        self.window = RootWidget()
        return self.window

    def loadConfig(self):
        response = urllib2.urlopen("http://127.0.0.1:5000/pred_list")
        return json.loads(response.read())

    def getCurrentSpectrogram(self, dt):
        response = urllib2.urlopen("http://127.0.0.1:5000/live_spec")
        image = np.fromstring(response.read(), np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # cv2.imshow("AudioTagger", image)
        # cv2.waitKey(1)
        # image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # print(image)
        # spectrogram = np.fromstring(test[1:-1], dtype=np.int, sep=' ')
        # print(spectrogram)
        self.window.update_Spectrogram_Image(image)

    def getCurrentPrediction(self, dt):
        response = urllib2.urlopen("http://127.0.0.1:5000/live_pred")
        prob_dict = json.loads(response.read())
        sorted_values = np.argsort(prob_dict.values())
        for i in range(5):
            class_label = prob_dict.keys()[sorted_values[40 - i]]
            class_width = prob_dict.values()[sorted_values[40 - i]] * 350
            self.window.update_Class_Prob_Bar(class_label, class_width, i)

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
