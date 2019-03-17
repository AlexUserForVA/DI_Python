class IGuiProvider(object):

    def getCurrentSpectrogram(self): raise NotImplementedError

    def getCurrentPrediction(self, dt): raise NotImplementedError