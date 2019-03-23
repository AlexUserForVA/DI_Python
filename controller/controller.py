from viewer.IViewer import IViewer
from model.IModel import IModel

class Controller:

    def __init__(self, viewer, model):

        if not isinstance(viewer, IViewer):
            raise TypeError('viewer must be an implementation of IViewer')
        if not isinstance(model, IModel):
            raise TypeError('model must be an implementation of IModel')

        self.viewer = viewer
        self.model = model