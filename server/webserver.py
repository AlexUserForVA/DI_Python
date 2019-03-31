import csv
import json
import threading

from flask import Flask, Response

from server.spectrogram.madmomSpectrogramProvider import MadmomSpectrogramProvider
from server.predictor.dcasePredictorProvider import DcasePredictorProvider
from server.audioTaggerModel import AudioTaggerModel

############### construct audio tagger model ####################
with open('config/predictors.csv') as file:
    csvReader = csv.reader(file, delimiter=';')
    next(csvReader, None)  # skip header
    predList = [{'displayname': line[0], 'classes': line[1], 'description': line[2]} for line in csvReader]

with open('config/sources.csv') as file:
    csvReader = csv.reader(file, delimiter=';')
    next(csvReader, None)  # skip header
    sourceList = [{'displayname': line[0], 'path': line[1]} for line in csvReader]

specsProvider = MadmomSpectrogramProvider()
predProvider = DcasePredictorProvider()

model = AudioTaggerModel(specsProvider, predProvider)

threading.Thread(target=model.specProvider.run).start()


###### startup web server to provide audio tagger REST API ######
app = Flask(__name__)

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

@app.route('/pred_list')
def pred_list():
    content = predList
    response = app.response_class(
        response=json.dumps(content),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/source_list')
def source_list():
    content = [elem['displayname'] for elem in sourceList]
    response = app.response_class(
        response=json.dumps(content),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False)
