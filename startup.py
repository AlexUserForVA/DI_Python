from predictorprovider.MockPredictorProvider import MockPredictorProvider
from spectrogramprovider.MockSpectrogramProvider import MockSpectrogramProvider
from predictorprovider_interfaces.IPredictorProvider import IPredictorProvider
from spectrogramprovider_interfaces.ISpectrogramProvider import ISpectrogramProvider

class Client(object):
    def __init__(self, predictorProvider, spectorgramProvider):
        # type saftey
        if not isinstance(predictorProvider, IPredictorProvider):
            raise TypeError('predictorProvider must be an implementation of IPredictorProvider')
        if not isinstance(spectorgramProvider, ISpectrogramProvider):
            raise TypeError('spectrogramProvider must be an implementation of IPredictorProvider')

        self.predictorProvider = predictorProvider
        self.spectrogramProvider = spectorgramProvider

    def callTheStuff(self):
        print(self.predictorProvider.predict(4))
        print(self.spectrogramProvider.getSpectrogramData())


if __name__ == '__main__':
    predictorProvider = MockPredictorProvider()
    spectrogramProvider = MockSpectrogramProvider()
    client = Client(predictorProvider, spectrogramProvider)
    client.callTheStuff()