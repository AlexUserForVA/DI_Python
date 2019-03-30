import os
import numpy as np
import argparse

import torch

from dcase_task2.pytorch.data_pool import EvalDataPool
from dcase_task2.pytorch.load_meta import get_files_and_labels_train, get_files_and_labels_test
from dcase_task2.pytorch.vars import DATA_ROOT as DATA_ROOT
from dcase_task2.pytorch.apk import mapk

BATCH_SIZE = 10

# add argument parser
parser = argparse.ArgumentParser(description='Train audio tagging network.')
parser.add_argument('--train_file', help='train data file.', type=str, default="train.csv")
parser.add_argument('--modelPath', type = str)
parser.add_argument('--validationFileNames', help='numpy dump of file names of the validation set', type = str, default = '')
args = parser.parse_args()

if args.validationFileNames != '':  # validation set
    fileNames, labels, isVerified = get_files_and_labels_train(os.path.join(DATA_ROOT, args.train_file), "specs_train_v1")
    evaluationFileNames = np.load(args.validationFileNames)
    evaluationIndices = [np.where(fileNames == sample)[0][0] for sample in evaluationFileNames]
    evaluationLabels = labels[evaluationIndices]
    n_eval = len(evaluationFileNames)
else: # test set
    evaluationFileNames, evaluationLabels = get_files_and_labels_test(os.path.join(DATA_ROOT, "test.csv"), "specs_test_v1")
    n_eval = len(evaluationFileNames)

no_of_batches_eval = int(np.ceil(n_eval * 1.0 / BATCH_SIZE))

pool = EvalDataPool(evaluationFileNames, evaluationLabels, spec_len= 2048)

eval_indices = range(0, n_eval)

model = torch.load(args.modelPath)
device = torch.device("cuda:0")
model.to(device)

model.eval()

all_eval_labels_actual = []
all_eval_labels_predicted = []

# validation section
for i in range(0, no_of_batches_eval):
    if len(eval_indices) < BATCH_SIZE:
        batch_eval_indices = eval_indices
    else:
        # pop first BATCH_SIZE elements of the indices array
        batch_eval_indices = eval_indices[0:BATCH_SIZE]
        eval_indices = eval_indices[BATCH_SIZE: len(evaluationFileNames) + 1]
    eval_features, eval_labels = pool[batch_eval_indices]

    torch_eval_features = torch.from_numpy(eval_features)
    cuda_torch_eval_features = torch_eval_features.to(device)

    # predict labels
    eval_out = model(cuda_torch_eval_features)
    # test_out = server(torch_test_features)   # test for cpu
    predicts = eval_out.cpu().detach().numpy()

    all_eval_labels_actual.extend(eval_labels)
    all_eval_labels_predicted.extend(predicts)

# compute map@3
predict_k = 3
actual = [[y] for y in all_eval_labels_actual]
predicted = []
for yp in all_eval_labels_predicted:
    predicted.append(list(np.argsort(yp)[::-1][0:predict_k]))
map3 = mapk(actual, predicted, predict_k)
map1 = mapk(actual, predicted, 1)
print("MAP@%d: %.3f" % (predict_k, map3))
print("Precision: %.3f" % (map1))

def predict(self, modelpath, inputSpectrogram):
    model = torch.load(args.modelPath)
    device = torch.device("cuda:0")
    model.to(device)

    model.eval()
    # returns a json ob class probabilities


