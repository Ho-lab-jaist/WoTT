import torch.nn as nn


class TacNet(nn.Module):
  def __init__(self, in_nc=6, pad = 1, bias=False):
    super(TacNet, self).__init__()

    # convolutional block 1
    self.conv11 = nn.Conv2d(in_nc, 64, 3, stride=1, padding=pad, bias=bias)
    self.batch_norm64 = nn.BatchNorm2d(64)
    # convolutional block 2
    self.conv21 = nn.Conv2d(64, 128, 3, 1, padding=pad, bias=bias)
    self.batch_norm128 = nn.BatchNorm2d(128)    
    # convolutional block 3
    self.conv31 = nn.Conv2d(128, 256, 3, 1, padding=pad, bias=bias)
    self.conv32 = nn.Conv2d(256, 256, 3, 1, padding=pad, bias=bias)
    self.batch_norm256 = nn.BatchNorm2d(256)    
    # convolutional block 4
    self.conv41 = nn.Conv2d(256, 512, 3, 1, padding=pad, bias=bias)
    self.conv42 = nn.Conv2d(512, 512, 3, 1, padding=pad, bias=bias)
    # convolutional block 5
    self.conv51 = nn.Conv2d(512, 512, 3, 1, padding=pad, bias=bias)
    self.conv52 = nn.Conv2d(512, 512, 3, 1, padding=pad, bias=bias)
    self.batch_norm512 = nn.BatchNorm2d(512) 

    num_of_neurons = 128
    outputs = 1755 #585*3
    self.fc = nn.Linear(512*8*8, outputs, bias=True)
    self.fc1 = nn.Linear(512*8*8, num_of_neurons, bias=True)
    self.fc2 = nn.Linear(num_of_neurons, num_of_neurons, bias=True)
    self.fc3 = nn.Linear(num_of_neurons, outputs, bias=True)
    self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)
    self.max_pool = nn.MaxPool2d(2)
    self.drop = nn.Dropout(p=0.25)

  def forward(self, x): # input size : (6, 256, 256)
    # feed forward through the conv. block 1x1
    x = self.batch_norm64(self.conv11(x))
    x = self.lrelu(x)
    x = self.max_pool(x) # size out : (64, 128, 128)

    # feed forward through the conv. block 2x1
    x = self.batch_norm128(self.conv21(x))
    x = self.lrelu(x)
    x = self.max_pool(x) # size out : (128, 64, 64)

    # feed forward through the conv. block 3x2
    x = self.batch_norm256(self.conv31(x))
    x = self.lrelu(x)
    x = self.batch_norm256(self.conv32(x))
    x = self.lrelu(x)
    x = self.max_pool(x) # size out : (256, 32, 32)

    # feed forward through the conv. block 4x2
    x = self.batch_norm512(self.conv41(x))
    x = self.lrelu(x)
    # x = self.batch_norm512(self.conv42(x))
    # x = self.lrelu(x)
    x = self.max_pool(x) # size out : (512, 16, 16)

    # feed forward through the conv. block 5x2
    x = self.batch_norm512(self.conv51(x))
    x = self.lrelu(x)
    # x = self.batch_norm512(self.conv52(x))
    # x = self.lrelu(x)
    x = self.max_pool(x) # size out : (512, 8, 8)

    # feed forward fully connected layers
    x = x.view(-1, self.num_flat_features(x))
    # x = self.drop(x)
    x = self.lrelu(self.fc1(x))
    # x = self.drop(x)
    x = self.lrelu(self.fc2(x))
    # x = self.drop(x)
    x = self.fc3(x)
    # x = self.fc(x)
    return x

  def num_flat_features(self, x):
    size = x.size()[1:]  # all dimensions except the batch dimension
    num_features = 1
    for s in size:
        num_features *= s
    return num_features