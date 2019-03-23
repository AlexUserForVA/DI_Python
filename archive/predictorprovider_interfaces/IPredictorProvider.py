class IPredictorProvider(object):

    def predict(self, input):
        """
        Sends an input array to a trained predictor
        and outputs the class probability as a json
        string.

        Parameters
        ----------
        arg1 : input
            the input features as numpy array

        Returns
        -------
        string
            the class probabilities for each class
            in json format.
        """
        raise NotImplementedError