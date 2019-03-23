from archive.spectrogramprovider.SpectrogramProvider import SpectrogramProvider
#from spectrogramprovider.MockPictureProvider import MockPictureProvider
from archive.guiprovider import KivyApp

if __name__ == '__main__':
    spectrogramProvider = SpectrogramProvider()
    gui = KivyApp(spectrogramProvider)
    gui.run()