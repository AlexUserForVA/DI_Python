from model.audiotaggermodel import AudioTaggerModel
from viewer.mainApp import MainApp
from controller.controller import Controller

if __name__ == '__main__':
    m = AudioTaggerModel()
    v = MainApp(m)
    # c = Controller(m, v)

    v.run()