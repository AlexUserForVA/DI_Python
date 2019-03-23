class IViewer:

    def onSpectrogramChanged(self, spectrogram):
        """
        This function gets invoked when the model which
        the implemented viewer is subscribed to has calculated
        a new spectrogram.

        Parameters
        ----------
        arg1 : spectrogram
            the currently pushed spectrogram
            as numpy array in rgb format
        """
        raise NotImplementedError


    def onPredictionChanged(self, prob_dict):
        """
        This function gets invoked when the model which
        the implemented viewer is subscribed to has calculated
        a new class probabilities during prediction.

        Parameters
        ----------
        arg1 : prob_dict
            the currently pushed class probabilities
            in json format
        """
        raise NotImplementedError