import random

class DcasePredictorProvider:

    classes = ["Acoustic_guitar", "Applause", "Bark", "Bass_drum", "Burping_or_eructation", "Bus", "Cello", "Chime",
               "Clarinet", "Computer_keyboard", "Cough", "Cowbell", "Double_bass", "Drawer_open_or_close",
               "Electric_piano",
               "Fart", "Finger_snapping", "Fireworks", "Flute", "Glockenspiel", "Gong", "Gunshot_or_gunfire",
               "Harmonica",
               "Hi-hat", "Keys_jangling", "Knock", "Laughter", "Meow", "Microwave_oven", "Oboe", "Saxophone",
               "Scissors",
               "Shatter", "Snare_drum", "Squeak", "Tambourine", "Tearing", "Telephone", "Trumpet",
               "Violin_or_fiddle",
               "Writing"]

    def registerModel(self, model):
        self.model = model

    def predict(self):
        # insert a real predictor
        probs = [{'label' : elem, 'prob' : random.uniform(0, 1), 'pos' : index} for index, elem in enumerate(self.classes)]
        #probs = dict([elem, random.uniform(0, 1)] for elem in self.classes)
        self.model.onNewPredictionCalculated(probs)