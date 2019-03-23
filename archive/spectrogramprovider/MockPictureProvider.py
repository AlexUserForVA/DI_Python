import io
import glob

from archive.spectrogramprovider_interfaces.ISpectrogramProvider import ISpectrogramProvider

class MockPictureProvider(ISpectrogramProvider):

    def __init__(self):
        self.spectrogramQueue = []
        self.fillQueue()

    def getCurrentSpectrogramImage(self):
        return self.spectrogramQueue.pop()

    def isSpectrogramImageQueueEmpty(self):
        return len(self.spectrogramQueue) == 0

    def fillQueue(self):
        data_paths = glob.glob('spectrogramprovider/mock_data/*.jpg')
        for elem in data_paths:
            data = io.BytesIO(open(elem, 'rb').read())
            self.spectrogramQueue.append(data)