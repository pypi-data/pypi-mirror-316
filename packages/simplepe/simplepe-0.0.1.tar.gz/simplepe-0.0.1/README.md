# SimplePE

Simple implementation of some Positional Encoding methods in PyTorch.

- [x] Sinusoidal Positional Encoding
- [x] Rotary Positional Encoding

## Installation

```bash
git clone https://github.com/donglinkang2021/simplepe.git
cd simplepe
pip install .
```

## Usage

```python
python example.py # Run the example
```

You can see the following results:

| Method | Sinusoidal | Rotary |
| ------------ | ---------- | ------ |
| Dimension-Time_Step Heatmap | ![Sinusoidal](./images/Sinusoidal_Positional_Encoding_Heatmap.png) | ![Rotary](./images/Rotary_Positional_Encoding_Heatmap.png) |
| Value-Time_Step Line_Plot | ![Sinusoidal](./images/Sinusoidal_Positional_Encoding_LinePlot.png) | ![Rotary](./images/Rotary_Positional_Encoding_LinePlot.png) |
| Multi-Head Dimension-Time_Step Heatmap | ![Sinusoidal](./images/Multi-Head_Sinusoidal_Positional_Encoding_Heatmap.png) | ![Rotary](./images/Multi-Head_Rotary_Positional_Encoding_Heatmap.png) |
| Multi-Head Value-Time_Step Line_Plot | ![Sinusoidal](./images/Multi-Head_Sinusoidal_Positional_Encoding_LinePlot.png) | ![Rotary](./images/Multi-Head_Rotary_Positional_Encoding_LinePlot.png) |
