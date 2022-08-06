import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader


batch_size = 1
max_len = 512

class CreateDataset(Dataset):
  def __init__(self, X, tokenizer, max_len):
    self.X = X
    self.tokenizer = tokenizer
    self.max_len = max_len

  def __len__(self):
    return 1

  def encode(self, tokenizer, text):
      inputs = tokenizer.encode_plus(
          text,
          add_special_tokens=True,
          max_length=self.max_len,
          padding = 'max_length',
          truncation = True
      )
      return inputs

  def __getitem__(self, index):
    text = self.X[index]
    ids = []
    mask = []
    inputs = self.encode(tokenizer=self.tokenizer, text=text)
    ids.append(torch.LongTensor(inputs['input_ids']))
    mask.append(torch.LongTensor(inputs['attention_mask']))

    return {
      'ids': ids,
      'mask': mask,
      'text':text,
    }



def text_to_loader(text, tokenizer):
    """テキストデータをデータローダの形式に変換"""
    X = np.array([text])
    dataset = CreateDataset(X, tokenizer, max_len=max_len)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False, pin_memory=True)
    return dataloader