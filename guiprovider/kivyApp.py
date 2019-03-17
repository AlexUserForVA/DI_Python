import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App

from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.core.image import Image

from guiprovider.audioTaggerWindow import AudioTaggerWindow

from guiprovider_interfaces.IGuiProvider import IGuiProvider
from predictorprovider_interfaces.IPredictorProvider import IPredictorProvider
from spectrogramprovider_interfaces.ISpectrogramProvider import ISpectrogramProvider


class KivyApp(App, IGuiProvider):

    kv_directory = 'guiprovider/kv'

    img_texture = ObjectProperty(None)

    def __init__(self, spectrogramProvider, predictorProvider, **kwargs):
        super(KivyApp, self).__init__(**kwargs)

        # type saftey
        if not isinstance(spectrogramProvider, ISpectrogramProvider):
            raise TypeError('spectrogramProvider must be an implementation of IPredictorProvider')
        if not isinstance(predictorProvider, IPredictorProvider):
            raise TypeError('predictorProvider must be an implementation of IPredictorProvider')

        self.spectrogramProvider = spectrogramProvider
        self.predictorProvider = predictorProvider

        Clock.schedule_interval(self.getCurrentSpectrogram, 2)

    def build(self):
        return AudioTaggerWindow()

    def getCurrentSpectrogram(self, dt):
        binaryImg = self.spectrogramProvider.getCurrentSpectrogramImage()
        self.img_texture = Image(binaryImg, ext='jpg').texture


