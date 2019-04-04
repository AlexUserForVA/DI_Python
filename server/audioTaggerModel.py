import queue

class AudioTaggerModel:

    def __init__(self, specProvider, predProvider):
        self.specProvider = specProvider
        self.predProvider = predProvider

        self.spectrogramQueue = queue.Queue()
        self.predictionQueue = queue.Queue()

        self.liveSpec = None
        self.livePred = None

        specProvider.registerModel(self)
        predProvider.registerModel(self)


    '''
    def getQueuedSpectrogram(self):
        return self.specProvider.getQueuedSpectrogram()

    def getLiveSpectrogram(self):
        return self.specProvider.getLiveSpectrogram()

    def getQueuedPrediction(self):
        return self.predProvider.getQueuedPrediction()

    def getLivePrediction(self):
        return self.predProvider.getLivePrediction()
    '''

    def getQueuedSpectrogram(self):
        if not self.spectrogramQueue.empty():
            return self.spectrogramQueue.get()

    def getLiveSpectrogram(self):
        return self.liveSpec

    def getQueuedPrediction(self):
        if not self.spectrogramQueue.empty():
            return self.predictionQueue.get()

    def getLivePrediction(self):
        return self.livePred

    def onNewSpectrogramCalculated(self, image):
        self.liveSpec = image
        self.spectrogramQueue.put(image)
        self.predProvider.predict() # trigger predition when new spectrogram is available

    def onNewPredictionCalculated(self, prob_dict):
        self.livePred = prob_dict
        self.predictionQueue.put(prob_dict)

    #########################################################

