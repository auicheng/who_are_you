import os
import librosa
from pydub import AudioSegment
import torch.tensor as tensor
from torch.autograd import Variable

# files                                                                         
input_size = 235
sequence_length = 40
hidden_size = 128
num_layers = 2
num_classes = 2  # TODO: Determine this from the data
learning_rate = 0.0001
num_epochs = 20000

# convert wav to mp3                                                            
def convert_m4a(src):
    filename = os.path.splitext(os.path.basename(src))[0]

    sound = AudioSegment.from_file(src)
    dst = 'webapp/wavs' + '/' + filename + '.wav'
    
    sound.export(dst, format="wav")
    return dst
    

def get_unpadded(path):
    instance_list = []
    wav, sr = librosa.load(path, sr=None, mono=True)
    unpadded = librosa.feature.mfcc(wav, sr, n_mfcc=40)
    instance_list.append(unpadded)
    return instance_list

def pad_data(series):
    import numpy as np

    padded = []
    for i in range(len(series)):
        row = np.zeros((sequence_length, input_size), dtype=np.float32)
        for j in range(sequence_length):
            for k in range(len(series[i][j])):
                row[j][k] = series[i][j][k]
        padded.append(row)
    return padded

def tensor_pad(padded):
    mfcc = tensor(padded)
    mfcc = Variable(mfcc.view(-1, sequence_length, input_size))
    return mfcc

def get_predict(predict):
    return predict.item() 
