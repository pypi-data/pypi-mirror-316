from typing import List, Optional

import torch
import torch.nn as nn


__all__ = ['Perceptron', 'MultiLayerPerceptron']


class Perceptron(nn.Module):
    def __init__(
        self,
        in_size: int = 32,
        num_classes: int = 10,
        weights: str = '',
    ) -> None:
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(in_size**2, num_classes),
            nn.ReLU(inplace=True)
        )
        self.load_weights(weights)

    def load_weights(self, weights: str = ''):
        self.weights = weights
        if weights:
            self.load_state_dict(torch.load(weights))

    def _forward_impl(self, x: torch.Tensor) -> torch.Tensor:
        x = torch.flatten(x, start_dim=1)
        return self.fc(x)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self._forward_impl(x)

class MultiLayerPerceptron(nn.Module):
    def __init__(
        self,
        in_size: List[int],
        num_classes: int = 10,
        weights: Optional[str] = None,
    ) -> None:
        super().__init__()
        in_size.append(num_classes)
        layers = [
            Perceptron(in_size[i], in_size[i + 1] ** 2)
            for i in range(len(in_size) - 1)
        ]
        self.layers = nn.Sequential(*layers)
        self.load_weights(weights)

    def load_weights(self, weights: str = ''):
        self.weights = weights
        if weights is not None:
            self.load_state_dict(torch.load(weights))

    def _forward_impl(self, x: torch.Tensor) -> torch.Tensor:
        x = torch.flatten(x, start_dim=-2)
        return self.layers(x)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self._forward_impl(x)