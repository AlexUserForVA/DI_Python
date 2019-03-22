from predictorprovider.MockPredictorProvider import MockPredictorProvider
from spectrogramprovider.MockPictureProvider import MockPictureProvider
from spectrogramprovider.SpectrogramProvider import SpectrogramProvider
#from spectrogramprovider.MockPictureProvider import MockPictureProvider
from audiotaggermodel.AudioTaggerModel import AudioTaggerModel
from guiprovider.kivyApp import KivyApp

from threading import Thread

if __name__ == '__main__':
    spectrogramProvider = SpectrogramProvider()
    gui = KivyApp(spectrogramProvider)
    gui.run()