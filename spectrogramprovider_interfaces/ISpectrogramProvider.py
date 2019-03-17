class ISpectrogramProvider(object):

    def getCurrentSpectrogramImage(self):
        """
        Retrieve the most current spectrogram image.

        Parameters
        ----------

        Returns
        -------
        PIL.JpegImagePlugin.JpegImageFile
            the current spectrogram as jpeg.
        """
        raise NotImplementedError

    def isSpectrogramImageQueueEmpty(self):
        """
        Check if the spectrogram queue is empty.

        Parameters
        ----------

        Returns
        -------
        Boolean
            queue is empty (true) or not (false)
        """
        raise NotImplementedError