from archive.predictorprovider_interfaces import IPredictorProvider
from archive.spectrogramprovider_interfaces.ISpectrogramProvider import ISpectrogramProvider
from archive.audiotaggermodel_interfaces import IAudioTaggerModel

class AudioTaggerModel(IAudioTaggerModel):

    def __init__(self, spectrogramProvider, predictorProvider):

        # type saftey
        if not isinstance(spectrogramProvider, ISpectrogramProvider):
            raise TypeError('spectrogramProvider must be an implementation of ISpectrogramProvider')
        if not isinstance(predictorProvider, IPredictorProvider):
            raise TypeError('predictorProvider must be an implementation of IPredictorProvider')

        self.spectrogramProvider = spectrogramProvider
        self.predictorProvider = predictorProvider

        self.spectrogramProvider.setObserver(self)

    def registerViewer(self, viewer):
        self.viewer = viewer

    def start(self):
        self.spectrogramProvider.start()

    def onSpectrogramChanged(self, spectrogram):
        self.viewer.resetSpectrogram(spectrogram)