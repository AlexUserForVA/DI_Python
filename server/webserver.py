import csv
import json
import threading

from flask import Flask, Response, request

from spectrogram.madmomSpectrogramProvider import MadmomSpectrogramProvider
from predictor.dcasePredictorProvider import DcasePredictorProvider
from audioTaggerModel import AudioTaggerModel

############### construct audio tagger model ####################
with open('config/predictors.csv') as file:
    csvReader = csv.reader(file, delimiter=';')
    next(csvReader, None)  # skip header
    predList = [{'id' : line[0], 'displayname': line[1], 'classes': line[2], 'description': line[3]} for line in csvReader]

with open('config/sources.csv') as file:
    csvReader = csv.reader(file, delimiter=';')
    next(csvReader, None)  # skip header
    sourceList = [{'id' : line[0],'displayname': line[1], 'path': line[2]} for line in csvReader]

specsProvider = MadmomSpectrogramProvider()
predProvider = DcasePredictorProvider()

model = AudioTaggerModel(specsProvider, predProvider)

thread = threading.Thread(target=model.specProvider.run).start()

def refreshAudioTagger(settings):
    print("We would like to stop the current thread now and start another one!")
    print(settings)


###### startup web server to provide audio tagger REST API ######
app = Flask(__name__)

@app.route('/live_spec', methods=['GET'])
def live_spec():
    content = model.getLiveSpectrogram()
    # content = (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + content + b'\r\n\r\n')
    return Response(content,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/live_spec_browser', methods=['GET'])
def live_spec_browser():
    content = model.getLiveSpectrogram()
    content = (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + content + b'\r\n\r\n')
    return Response(content,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/queued_spec', methods=['GET'])
def queued_spec():
    content = model.getQueuedSpectrogram()
    # content = (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + content + b'\r\n\r\n')
    return Response(content,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/live_pred', methods=['GET'])
def live_pred():
    content = model.getLivePrediction()
    response = app.response_class(
        response=json.dumps(content),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/queued_pred', methods=['GET'])
def queued_pred():
    content = model.getQueuedPrediction()
    response = app.response_class(
        response=json.dumps(content),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/pred_list', methods=['GET'])
def pred_list():
    content = predList
    response = app.response_class(
        response=json.dumps(content),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/source_list', methods=['GET'])
def source_list():
    content = [{'id' : elem['id'],'displayname': elem['displayname']} for elem in sourceList]
    response = app.response_class(
        response=json.dumps(content),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/settings', methods=['POST'])
def add_message():
    content = request.json
    refreshAudioTagger(content)
    return 'OK'

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False)
