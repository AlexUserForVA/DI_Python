import cv2
import queue
import numpy as np
import matplotlib.pyplot as plt

from madmom.processors import IOProcessor, process_online
from prepare_spectrograms import processor_pipeline2

class MadmomSpectrogramProvider:

    def __init__(self):
        self.predict_every_k = 20
        self.frame_count = 0
        self.sliding_window = np.zeros((128, 256), dtype=np.float32)
        self.queue = queue.Queue()
        self.curImage = None

    def run(self):
        processor = IOProcessor(in_processor=processor_pipeline2, out_processor=self.output_processor)
        # process_online(processor, infile='server/2019-03-26-12:33:33.wav', outfile=None, sample_rate=32000)
        process_online(processor, infile=None, outfile=None, sample_rate=32000)

    def registerModel(self, model):
        self.model = model

    '''
    def getQueuedSpectrogram(self):
        if not self.queue.empty():
            return self.queue.get()

    def getLiveSpectrogram(self):
        return self.curImage
    '''

    def output_processor(self, data, output):
        """
        Output data processor
        """
        # SLIDING_WINDOW = np.zeros((128, 256), dtype=np.float32)
        # FRAME_COUNT = 0
        TEXT_BOX = None
        MAX_ELEMS = 256
        # global PREDICT_EVERY_K

        # check if there is audio content
        frame = data[0]
        if np.any(np.isnan(frame)):
            frame = np.zeros_like(frame, dtype=np.float32)

        # PREDICT_EVERY_K = 20

        # increase frame count
        self.frame_count += 1
        self.frame_count = np.mod(self.frame_count, self.predict_every_k)
        do_invoke = self.frame_count == 0

        # update sliding window
        self.sliding_window[:, 0:-1] = self.sliding_window[:, 1::]
        self.sliding_window[:, -1] = frame

        # show current sliding window
        resz_spec = 2
        spec = self.sliding_window[::-1, :].copy() / 3.0
        spec = cv2.resize(spec, (spec.shape[1] * resz_spec, spec.shape[0] * resz_spec))
        spec = plt.cm.viridis(spec)[:, :, 0:3]
        spec_bgr = (spec * 255).astype(np.uint8)
        if spec_bgr.shape[1] < 512:
            p = (512 - spec_bgr.shape[1]) // 2
            spec_bgr = np.pad(spec_bgr, ((0, 0), (p, p), (0, 0)), mode="constant")

        spec_bgr = cv2.flip(spec_bgr, 0)

        # _, jpegImage = cv2.imencode('.jpg', spec_bgr)
        # jpegImage = jpegImage.tobytes()
        # self.spectrogramQueue.append(jpegImage)
        '''
        if do_invoke:
            _, curImage = cv2.imencode('.jpg', spec_bgr)
            curImage = curImage.tobytes()
            self.curImage = curImage
            self.queue.put(curImage)
        '''
        if do_invoke:
            _, curImage = cv2.imencode('.jpg', spec_bgr)
            curImage = curImage.tobytes()
            self.model.onNewSpectrogramCalculated(curImage)
