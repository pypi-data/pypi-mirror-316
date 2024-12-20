# Power Spectral Density and Smoothing Analysis

This package provides tools for analyzing time series data using spectral methods, including Fourier and wavelet transforms. It includes functionality for smoothing data, estimating the power spectral density (PSD) using both FFT and wavelet methods, and other utility functions for handling spectral data.

## Features

- **Data Smoothing**:
  - `smooth`: Logarithmic smoothing of data, using indices generated based on the FFT frequency distribution.
  - `smoothing_function`: Core function for smoothing with a logarithmic window size.

- **Power Spectral Density Estimation**:
  - `TracePSD`: PSD estimation using the Fourier transform for a 3-component signal.
  - `trace_PSD_wavelet`: PSD estimation using the Continuous Wavelet Transform (CWT), with optional Cone of Influence (CoI) consideration.

## Installation

Clone this repository to your local machine and install the required dependencies:

```bash
git clone <repository_url>
cd <repository_name>
pip install -r requirements.txt
```

## Dependencies

- `numpy`: For numerical operations and FFT.
- `pycwt`: For wavelet analysis.
- `numba`: For JIT-compiled performance optimization of smoothing functions.

## Usage

### 1. Smoothing Data

```python
import numpy as np
from your_package_name import smooth

# Example data
x = np.fft.rfftfreq(1000, d=0.01)
y = np.random.random(len(x))

# Apply smoothing
xoutmean, yout = smooth(x, y, pad=10)
```

### 2. PSD Estimation with FFT

```python
from your_package_name import TracePSD

# Example data
x = np.sin(np.linspace(0, 10, 1000))
y = np.cos(np.linspace(0, 10, 1000))
z = np.sin(np.linspace(0, 10, 1000)) * 0.5

dt = 0.01  # Sampling time
freqs, B_pow = TracePSD(x, y, z, dt, norm='forward')
```

### 3. PSD Estimation with Wavelet Transform

```python
from your_package_name import trace_PSD_wavelet

# Example data
x = np.sin(np.linspace(0, 10, 1000))
y = np.cos(np.linspace(0, 10, 1000))
z = np.sin(np.linspace(0, 10, 1000)) * 0.5

dt = 0.01  # Sampling time
dj = 0.1   # Scale resolution

db_x, db_y, db_z, freqs, PSD, scales, coi = trace_PSD_wavelet(x, y, z, dt, dj, consider_coi=True)
```

## Function Descriptions

### `smooth(x, y, pad)`

**Description**: A wrapper for smoothing data based on logarithmic spacing of indices. Assumes `x` is the output of `numpy.fft.rfftfreq`.

**Parameters**:
- `x` (numpy.ndarray): FFT frequency array.
- `y` (numpy.ndarray): Data to smooth.
- `pad` (int): Controls the density of smoothing intervals.

**Returns**:
- `xoutmean` (numpy.ndarray): Smoothed x-values.
- `yout` (numpy.ndarray): Smoothed y-values.

---

### `TracePSD(x, y, z, dt, norm=None)`

**Description**: Estimate the PSD using the Fourier transform for a 3-component signal.

**Parameters**:
- `x, y, z` (numpy.ndarray): Time series data for each component.
- `dt` (float): Sampling time.
- `norm` (str, optional): Normalization method for FFT. Options are `{'forward', 'backward', 'ortho'}`.

**Returns**:
- `freqs` (numpy.ndarray): Frequencies of the PSD.
- `B_pow` (numpy.ndarray): Power spectral density.

---

### `trace_PSD_wavelet(x, y, z, dt, dj, consider_coi=True)`

**Description**: Estimate the PSD using wavelet transform for a 3-component signal.

**Parameters**:
- `x, y, z` (numpy.ndarray): Time series data for each component.
- `dt` (float): Sampling time.
- `dj` (float): Scale resolution.
- `consider_coi` (bool, optional): Whether to exclude regions in the Cone of Influence (CoI).

**Returns**:
- `db_x, db_y, db_z` (numpy.ndarray): Wavelet coefficients for each component.
- `freqs` (numpy.ndarray): Frequencies of the PSD.
- `PSD` (numpy.ndarray): Power spectral density.
- `scales` (numpy.ndarray): Scales used for the wavelet transform.
- `coi` (numpy.ndarray): Cone of Influence (CoI).

## Example Plots

You can visualize the smoothed data or PSD using libraries like `matplotlib`.

```python
import matplotlib.pyplot as plt

# Plot FFT-based PSD
plt.loglog(freqs, B_pow)
plt.title('Power Spectral Density (FFT)')
plt.xlabel('Frequency')
plt.ylabel('PSD')
plt.grid()
plt.show()

# Plot Wavelet-based PSD
plt.loglog(freqs, PSD)
plt.title('Power Spectral Density (Wavelet)')
plt.xlabel('Frequency')
plt.ylabel('PSD')
plt.grid()
plt.show()
```

## Contribution

Contributions are welcome! Please submit issues or pull requests to improve the code or documentation.

## License

This project is licensed under the [MIT License](LICENSE).

