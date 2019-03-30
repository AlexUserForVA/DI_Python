from viewer.IViewer import IViewer
from server.IModel import IModel
from IController import IController

class Controller(IController):

    def __init__(self, model, viewer):

        if not isinstance(model, IModel):
            raise TypeError('server must be an implementation of IModel')
        if not isinstance(viewer, IViewer):
            raise TypeError('viewer must be an implementation of IViewer')

        self.viewer = viewer
        self.model = model

    def onSpeedChanged(self, value):
        self.model.setSpeed(value)