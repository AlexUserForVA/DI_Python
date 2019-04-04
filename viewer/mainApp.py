import json
# import urllib2
import numpy as np
import cv2
import time

import requests
from array import array
from urllib.request import urlopen

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.properties import ListProperty, StringProperty
from viewer.utils.utils import getScreenResolution

from viewer.IViewer import IViewer

class RootWidget(FloatLayout):
    prob_list = ListProperty([100, 100, 100, 100, 100])
    class_list = ListProperty(['-', '-', '-', '-', '-'])
    pred_list = ListProperty([])
    source_list = ListProperty([])
    sourceProperty = StringProperty()
    predictorProperty = StringProperty()

    def start_Button_pressed(self, label):
        self.but_1.disabled = True
        Clock.schedule_interval(App.get_running_app().getCurrentSpectrogram, 0.02)
        Clock.schedule_interval(App.get_running_app().getCurrentPrediction, 1)

    def liveOrFileSettingHasChanged(self, instance, value):
        App.get_running_app().setIsLive(value)

    def predSettingHasChanged(self, *args):
        App.get_running_app().setPredictor(args[0].selection[0].text)

    def sourceSettingHasChanged(self, *args):
        App.get_running_app().setFile(args[0].selection[0].text)

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

    def build(self):
        self.window = RootWidget()
        self.window.pred_list = self.loadPredictors()
        self.window.source_list = self.loadSources()

        self.isLive = True
        self.file = self.window.source_list[0]['displayname']
        self.predictor = self.window.pred_list[0]['displayname']

        self.setSummaryLabels()

        self.window.switch_1.bind(active=self.window.liveOrFileSettingHasChanged)
        self.window.predView.adapter.bind(on_selection_change=self.window.predSettingHasChanged) # doesn't work in .kv file
        self.window.sourceView.adapter.bind(on_selection_change=self.window.sourceSettingHasChanged)  # doesn't work in .kv file

        return self.window

    def setSummaryLabels(self):
        if self.isLive:
            self.window.sourceProperty = 'Microphone'
        else:
            self.window.sourceProperty = self.file
        self.window.predictorProperty = self.predictor

    def loadPredictors(self):
        response = urllib2.urlopen("http://127.0.0.1:5000/pred_list")
        return json.loads(response.read())

    def loadSources(self):
        response = urllib2.urlopen("http://127.0.0.1:5000/source_list")
        return json.loads(response.read())

    def setIsLive(self, value):
        self.isLive = value
        self.notifyBackendAboutSettingsChanged()

    def setFile(self, value):
        self.file = value
        self.notifyBackendAboutSettingsChanged()

    def setPredictor(self, value):
        self.predictor = value
        self.notifyBackendAboutSettingsChanged()

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
        if len(prob_dict) > 5:  # show the 5 most probable classes
            sorted_dict = sorted(prob_dict, key=lambda i: i['prob'], reverse=True)
        else:
            sorted_dict = sorted(prob_dict, key=lambda i: i['pos'])
        for i in range(5):
            # class_label = prob_dict.keys()[sorted_values[40 - i]]
            # class_width = prob_dict.values()[sorted_values[40 - i]] * 350
            class_label = sorted_dict[i]['label']
            class_width = sorted_dict[i]['prob'] * 350
            self.window.update_Class_Prob_Bar(class_label, class_width, i)

    def onPredictionChanged(self, json_class_probs):
        prob_dict = json.loads(json_class_probs)
        sorted_values = np.argsort(prob_dict.values())
        for i in range(5):
            class_label = prob_dict.keys()[sorted_values[40 - i]]
            class_width = prob_dict.values()[sorted_values[40 - i]] * 350
            self.window.update_Class_Prob_Bar(class_label, class_width, i)

    def notifyBackendAboutSettingsChanged(self):
        self.setSummaryLabels()
        settingsDict = {'isLive' : self.isLive, 'file' : self.file, 'predictor' : self.predictor}
        res = requests.post('http://localhost:5000/settings', json=settingsDict)


