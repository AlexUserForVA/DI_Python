from kivy.uix.floatlayout import FloatLayout
from utils.utils import getScreenResolution
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

class AudioTaggerWindow(FloatLayout):
    screen_width, screen_heigth = getScreenResolution()
    window_width, window_heigth = screen_width / 1.5, screen_heigth / 1.5
    Window.size = (window_width, window_heigth)
    output_column = window_width * 0.66
    control_column = window_width * 0.33

class SpectrogramPanel(BoxLayout):
    image_path = 'gui/images/mercedes.png'