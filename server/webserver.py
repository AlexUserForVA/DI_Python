import json
import threading

from flask import Flask, Response

from server.spectrogram.madmomSpectrogramProvider import MadmomSpectrogramProvider
from server.predictor.dcasePredictorProvider import DcasePredictorProvider
from server.audioTaggerModel import AudioTaggerModel

'''
class Spectrogram(Resource):

    def __init__(self, model):SpectrogramSpectrogram
        self.model = model

    def get(self):
        data = self.model.getCurrentSpectrogram().flatten()
        return json.dumps({'spec': data})


class Prediction(Resource):

    def __init__(self, model):
        self.model = model

    def get(self):
        return json.dumps(self.model.getCurrentPrediction())
'''
#############################################

specsProvider = MadmomSpectrogramProvider()
predProvider = DcasePredictorProvider()

model = AudioTaggerModel(specsProvider, predProvider)

threading.Thread(target=model.specProvider.run).start()

app = Flask(__name__)

'''
def gen(model):
    while True:
            frame = model.getCurrentLiveSpectrogram()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
'''

@app.route('/live_spec')
def live_spec():
    content = model.getLiveSpectrogram()
    # content = (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + content + b'\r\n\r\n')
    return Response(content,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/queued_spec')
def queued_spec():
    content = model.getQueuedSpectrogram()
    # content = (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + content + b'\r\n\r\n')
    return Response(content,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/live_pred')
def live_pred():
    content = model.getLivePrediction()
    response = app.response_class(
        response=json.dumps(content),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/queued_pred')
def queued_pred():
    content = model.getQueuedPrediction()
    response = app.response_class(
        response=json.dumps(content),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False)