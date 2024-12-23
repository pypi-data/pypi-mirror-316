from typing import Optional

import torch
from torch import nn
from torch.ao import quantization as quant


__all__ = ['Quantized']


class Quantized(nn.Module):
    def __init__(
        self,
        in_size: int = 28,
        num_classes: int = 10,
        weights: Optional[str] = None,
        qconfig: Optional[quant.qconfig.QConfig] = None,
    ) -> None:
        try:
            # Initialize with full-precision weights or generate an empty model
            super().__init__(in_size, num_classes, weights)
            self.quant = quant.QuantStub()
            self.dequant = quant.DeQuantStub()
        except:
            # Initialize with quantized weights
            super().__init__(in_size, num_classes)
            self.quant = quant.QuantStub()
            self.dequant = quant.DeQuantStub()
            self.qconfig = qconfig
            quant.prepare(self, inplace=True)
            quant.convert(self, inplace=True)
            self.load_weights(weights)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.quant(x)
        x = self._forward_impl(x)
        x = self.dequant(x)
        return x
