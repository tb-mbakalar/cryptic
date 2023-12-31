import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data

translation_dict = {'A':0,'T':1,'C':2,'G':3,'N':4}

# One-hot encoding of sequences
class Dataset(torch.utils.data.Dataset):

  def __init__(self, sequences, labels, vocab_size, output_size=1, one_hot_label=False):
    self.sequences = sequences
    self.labels = labels
    self.vocab_size = vocab_size
    self.output_size = output_size
    self.one_hot_label = one_hot_label

  def __len__(self):
    return len(self.sequences)

  def __getitem__(self, idx):
    sequence = self.sequences[idx]
    if self.one_hot_label:
      label = F.one_hot(torch.tensor(self.labels[idx]), num_classes=self.output_size)
    else:
        label = self.labels[idx]
    encoding = torch.tensor([translation_dict[c] for c in sequence])
    x = F.one_hot(encoding, num_classes=self.vocab_size).to(torch.float32)
    return x, label