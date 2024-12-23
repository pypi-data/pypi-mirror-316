from typing import Any, List, Optional

from torch import utils
from torchvision.transforms import transforms


__all__ = ['prepare_data']


def prepare_data(
    source: utils.data.Dataset,
    train: bool = True,
    batch_size: int = 1,
    transform: Any = transforms.ToTensor(),
    splits: Optional[List[float]] = None,
    shuffle: Optional[bool] = None,
    root: str = 'data',
) -> List[utils.data.DataLoader]:

    datasets = [source(root=root, train=train, download=True, transform=transform)]
    if splits is not None:
        datasets = utils.data.random_split(datasets[0], splits)

    if shuffle is None:
        shuffle = train
    dataloaders = [
        utils.data.DataLoader(i, batch_size=batch_size, shuffle=shuffle)
        for i in datasets
    ]
    return dataloaders if splits else dataloaders[0]
