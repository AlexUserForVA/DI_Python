import glob

from spectrogramprovider_interfaces.ISpectrogramProvider import ISpectrogramProvider

from PIL import Image

class MockSpectrogramProvider(ISpectrogramProvider):

    def __init__(self):
        self.spectrogramQueue = []
        self.fillQueue()

    def getCurrentSpectrogramImage(self):
        return self.spectrogramQueue.pop()

    def isSpectrogramImageQueueEmpty(self):
        return len(self.spectrogramQueue) == 0

    def fillQueue(self):
        data_paths = glob.glob('mock_data/*.jpg')
        for elem in data_paths:
            img = Image.open(elem)
            self.spectrogramQueue.append(img)


