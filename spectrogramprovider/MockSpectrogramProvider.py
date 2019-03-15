from spectrogramprovider_interfaces.ISpectrogramProvider import ISpectrogramProvider

class MockSpectrogramProvider(ISpectrogramProvider):

    def getSpectrogramData(self):
        return 'You got the spectrogram data.'