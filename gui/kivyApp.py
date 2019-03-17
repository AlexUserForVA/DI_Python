import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App

from gui.audioTaggerWindow import AudioTaggerWindow

from predictorprovider_interfaces.IPredictorProvider import IPredictorProvider
from spectrogramprovider_interfaces.ISpectrogramProvider import ISpectrogramProvider


class KivyApp(App):

    kv_directory = 'gui/kv'

    def __init__(self, spectrogramProvider, predictorProvider, **kwargs):
        super(KivyApp, self).__init__(**kwargs)

        # type saftey
        if not isinstance(spectrogramProvider, ISpectrogramProvider):
            raise TypeError('spectrogramProvider must be an implementation of IPredictorProvider')
        if not isinstance(predictorProvider, IPredictorProvider):
            raise TypeError('predictorProvider must be an implementation of IPredictorProvider')

        self.spectrogramProvider = spectrogramProvider
        self.predictorProvider = predictorProvider

    def build(self):
        return AudioTaggerWindow()

