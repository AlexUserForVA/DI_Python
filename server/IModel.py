class IModel:

    def run(self):
        """
        Starts the IModel implementing instance.
        """

    def subscribe(self, viewer):
        """
        Model-Viewer communication is based on Publisher/Subscriber-Pattern.

        Call the server to subscribe a object of type IViewer.
        Every time the server changes the registered viewer gets
        notified.
        Parameters
        ----------
        arg1 : viewer
           the object of type IViewer to be registered.
        """
        raise NotImplementedError

    def publishSpectrogram(self, spectrogram):
        """
        Invokes the registered subscribers on change of spectrogram.
        """
        raise NotImplementedError

    def publishPrediction(self, probabilities):
        """
        Invokes the registered subscribers on change of class probabilities.
        """
        raise NotImplementedError