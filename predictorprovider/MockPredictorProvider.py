from predictorprovider_interfaces.IPredictorProvider import IPredictorProvider

class MockPredictorProvider(IPredictorProvider):

    def predict(self, input):
        return input * 2;