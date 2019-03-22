
from __future__ import print_function

import io
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from madmom.processors import IOProcessor, process_online

from prepare_spectrograms import processor_pipeline2, processor_version1
from spectrogramprovider_interfaces.ISpectrogramProvider import ISpectrogramProvider
#from lasagne_wrapper.network import Network
#from config.settings import EXP_ROOT
#from train import get_dump_file_paths, select_model
#from utils.data_tut18_task2 import ID_CLASS_MAPPING

# initialize sliding window
SLIDING_WINDOW = np.zeros((128, 256), dtype=np.float32)
FRAME_COUNT = 0
TEXT_BOX = None
PREDICT_EVERY_K = None

class SpectrogramProvider(ISpectrogramProvider):

    observers = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def publish(self, spectrogram_np):
        for o in self.observers:
            o.spectrogramHasChanged(spectrogram_np)

    def run(self):
        processor = IOProcessor(in_processor=processor_pipeline2, out_processor=self.output_processor)
        process_online(processor, infile=None, outfile=None, sample_rate=32000)

    def output_processor(self, data, output):
        """
        Output data processor
        """
        global FRAME_COUNT
        global TEXT_BOX
        global SLIDING_WINDOW
        global TAGGER
        global PREDICT_EVERY_K

        # check if there is audio content
        frame = data[0]
        if np.any(np.isnan(frame)):
            frame = np.zeros_like(frame, dtype=np.float32)

        PREDICT_EVERY_K = 50

        # increase frame count
        FRAME_COUNT += 1
        FRAME_COUNT = np.mod(FRAME_COUNT, PREDICT_EVERY_K)
        do_invoke = FRAME_COUNT == 0

        # update sliding window
        SLIDING_WINDOW[:, 0:-1] = SLIDING_WINDOW[:, 1::]
        SLIDING_WINDOW[:, -1] = frame

        # show current sliding window
        resz_spec = 2
        spec = SLIDING_WINDOW[::-1, :].copy() / 3.0
        spec = cv2.resize(spec, (spec.shape[1] * resz_spec, spec.shape[0] * resz_spec))
        spec = plt.cm.viridis(spec)[:, :, 0:3]
        spec = (spec * 255).astype(np.uint8)
        spec_rgb = cv2.cvtColor(spec, cv2.COLOR_RGB2BGR)
        if spec_rgb.shape[1] < 512:
            p = (512 - spec_rgb.shape[1]) // 2
            spec_rgb = np.pad(spec_rgb, ((0, 0), (p, p), (0, 0)), mode="constant")
        if do_invoke:
            self.publish(spec_rgb)
