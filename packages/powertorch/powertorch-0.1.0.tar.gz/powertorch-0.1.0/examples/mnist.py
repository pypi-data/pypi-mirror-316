import sys

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision.datasets import MNIST as Dataset

from powertorch.models import Perceptron as DNN
from powertorch import helper


batch_size = 512
trainloader = helper.prepare_data(source=Dataset, train=True, batch_size=batch_size)
testloader = helper.prepare_data(source=Dataset, train=False, batch_size=batch_size)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
net = DNN(in_size=28, num_classes=10).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
max_epochs = 1 if len(sys.argv) == 1 else int(sys.argv[1])


losses = []
def train_step(batch, index, epoch):
    net.train()
    optimizer.zero_grad()
    inputs, labels = batch[0].to(device), batch[1].to(device)
    outputs = net(inputs)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()
    losses.append(loss.item())


def evaluate_model(dataloader):
    net.eval()
    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in dataloader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = net(images)
            _, predicted = torch.max(outputs.data, dim=1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        acc = correct / total
        print(f'[Epoch {trainer.state.epoch}/{max_epochs}] Accuracy: {acc * 100:.2f}%')


trainer = helper.Task(train_step)
trainer.add_event_handler(helper.Event.ITERATION_STARTED,
    lambda: print(f'Progress: {trainer.state.batch}/{len(trainloader)}', end='\r'))
trainer.add_event_handler(helper.Event.EPOCH_COMPLETED, evaluate_model, testloader)
trainer.run(trainloader, max_epochs=max_epochs)
