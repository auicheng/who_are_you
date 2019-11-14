import torch
import torch.nn as nn
import torch.tensor as tensor
import torch.nn.functional as F
from torch.utils.data import Dataset
from torch.autograd import Variable

cuda_enabled = False

class BiRNN(nn.Module):

    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(BiRNN, self).__init__()
        self.is_training = False
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers,
                            batch_first=True, bidirectional=True)
        #self.fc = nn.Dropout(p=0.75, inplace=False)
        self.fc = nn.Dropout(p=0.5, inplace=False)
        self.linear = nn.Linear(self.hidden_size*2, self.num_classes)

        if cuda_enabled:
            self.lstm = self.lstm.cuda()
            self.fc = self.fc.cuda()
            self.linear = self.linear.cuda()

    def forward(self, x):
        # Set initial states
        h0 = Variable(torch.zeros(self.num_layers*2, x.size(0), self.hidden_size)) # 2 for bidirection
        c0 = Variable(torch.zeros(self.num_layers*2, x.size(0), self.hidden_size))
        
        if cuda_enabled:
            h0 = h0.cuda()  # 2 for bidirection
            c0 = c0.cuda()

        # Forward propagate RNN
        out, _ = self.lstm(x, (h0, c0))
        
        # Decode hidden state of last time step
        if self.is_training:
            out = self.fc(out[:, -1, :])
        else:
            out = out[:, -1, :]

        out = F.log_softmax(self.linear(out), dim=1)
        return out

class BiRNN3(nn.Module):

    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(BiRNN3, self).__init__()
        self.is_training = False
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes
        self.gru = nn.GRU(input_size, hidden_size, num_layers,
                            batch_first=True, bidirectional=True)
        #self.fc = nn.Dropout(p=0.75, inplace=False)
        self.fc = nn.Dropout(p=0.5, inplace=False)
        self.linear = nn.Linear(self.hidden_size*2, self.num_classes)

        if cuda_enabled:
            self.gru = self.gru.cuda()
            self.fc = self.fc.cuda()
            self.linear = self.linear.cuda()

    def forward(self, x):
        # Set initial states
        h0 = Variable(torch.zeros(self.num_layers*2, x.size(0), self.hidden_size)) # 2 for bidirection
        if cuda_enabled:
            h0 = h0.cuda()  # 2 for bidirection

        # Forward propagate RNN
        out, _ = self.gru(x, h0)
        
        # Decode hidden state of last time step
        if self.is_training:
            out = self.fc(out[:, -1, :])
        else:
            out = out[:, -1, :]

        out = F.log_softmax(self.linear(out), dim=1)
        return out