from model.audiotaggermodel import AudioTaggerModel
from viewer.mainApp import MainApp

if __name__ == '__main__':
    sp = AudioTaggerModel()
    MainApp(sp).run()