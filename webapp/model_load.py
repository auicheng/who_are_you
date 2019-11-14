from BiRNN import BiRNN
from BiRNN import BiRNN3
import torch

input_size = 235
hidden_size = 128
num_layers = 2
num_classes = 2  # TODO: Determine this from the data

def create_model():
    rnn = BiRNN3(input_size, hidden_size, num_layers, num_classes)
    rnn.load_state_dict(torch.load('webapp/GRU.pkl', map_location='cpu'))
    rnn.eval()
    return rnn

def torch_max(model, mfcc):
    outputs = model(mfcc)
    _, predicted = torch.max(outputs.data, 1)
    return predicted   