# PowerTorch

A collection of PyTorch utilities designed to streamline the deep learning workflows

## Getting Started

### Installation

You can install the library directly from the repository:

```shell
pip install git+https://github.com/yutingshih/powertorch.git
```

Alternatively, clone the repository and manually install the dependencies:

```shell
git clone https://github.com/yutingshih/powertorch.git
cd nth
pip install -r requirements.txt
```

### Quick Test

To verify the installation, run the MNIST example:

```python
python3 -m examples.mnist
```

## Usage

### Import Package

```python
from powertorch import helper
from powertorch import models
```

### Prepare Data

```python
trainloader, validloader = helper.prepare_data(
    source=torchvision.datasets.MNIST,
    train=True,
    batch_size=256,
    transform=transforms.ToTensor(),
    splits=[0.8, 0.2],
)

testloader = helper.prepare_data(
    source=torchvision.datasets.MNIST,
    train=False,
    batch_size=256,
    transform=transforms.ToTensor(),
)
```

### Define a Training Task

```python
losses = []
def train_step(batch, index, epoch):
    net.train()
    optimizer.zero_grad()
    inputs, labels = [i.to(device) for i in batch]
    outputs = net(inputs)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()
    losses.append(loss.item())

trainer = helper.Task(train_step)
trainer.run(trainloader, max_epochs=max_epochs)
```

### Register Event Handlers

#### Show Progress

```python
trainer = helper.Task(train_step)
trainer.add_event_handler(helper.Event.ITERATION_STARTED,
    lambda: print(f'Progress: {trainer.state.batch}/{len(trainloader)}', end='\r'))
trainer.run(trainloader, max_epochs=max_epochs)
```

#### Evaluate Model

```python
def evaluate_model(dataloader):
    # (skip) ...

trainer = helper.Task(train_step)
trainer.add_event_handler(helper.Event.EPOCH_COMPLETED, evaluate_model, testloader)
trainer.run(trainloader, max_epochs=max_epochs)
```
