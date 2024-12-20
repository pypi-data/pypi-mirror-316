import numpy as np
import pycwt as wavelet
from numba import prange, jit

def smooth(x, y, pad):
    """
    Wrapper function for smoothing data based on a logarithmic spacing of indices.

    This function generates a set of indices logarithmically spaced based on the length of `x` and the `pad` parameter.
    It then calls `smoothing_function` to compute the smoothed `y` values over windows of size 2 in log space.

    Assumptions:
    ------------
    - `x` is assumed to be the output from `numpy.fft.rfftfreq`, which generates an array of frequencies 
      that are monotonically increasing and equally distributed in logarithmic space.

    Parameters:
    ----------
    x : numpy.ndarray
        Array of x-values, typically the output from `numpy.fft.rfftfreq`.
    y : numpy.ndarray
        Array of y-values corresponding to `x`.
    pad : int
        Factor to control the density of smoothing intervals. Larger values result in fewer intervals.

    Returns:
    -------
    xoutmean : numpy.ndarray
        Array of mean x-values for each smoothing window.
    yout : numpy.ndarray
        Array of smoothed y-values for each interval.
    """

    # Generate logarithmically spaced indices
    loop = np.logspace(0, np.log10(len(x)), int(len(x)/pad))
    loop = np.array(loop, dtype=np.int64)
    loop = np.unique(loop)

    # Call the smoothing function
    xoutmean, yout = smoothing_function(x, y, loop)

    return xoutmean, yout

@jit(nopython=True, parallel=True)
def smoothing_function(x, y, loop):
    """
    Perform smoothing of `y` values over a window size of 2 in logarithmic space.

    This function assumes that `x` is the output from `numpy.fft.rfftfreq`, which generates an array of 
    monotonically increasing frequencies equally distributed in logarithmic space.
    For each interval specified in `loop`, the mean of `x` and `y` within the interval is computed.

    Assumptions:
    ------------
    - `x` is the output from `numpy.fft.rfftfreq`.

    Parameters:
    ----------
    x : numpy.ndarray
        Array of x-values, typically the output from `numpy.fft.rfftfreq`.
    y : numpy.ndarray
        Array of y-values corresponding to `x`.
    loop : numpy.ndarray
        Array of indices specifying the start of each smoothing interval.

    Returns:
    -------
    xoutmean : numpy.ndarray
        Array of mean x-values for each smoothing window.
    yout : numpy.ndarray
        Array of smoothed y-values for each interval.
    """

    len_x = len(x)  # Total length of the x array
    max_x = np.max(x)  # Maximum value in x

    # Initialize output arrays with NaN values
    xoutmean = np.full(len(loop), np.nan)
    yout = np.full(len(loop), np.nan)

    # Iterate over the loop indices in parallel
    for i1 in prange(len(loop)):
        i = int(loop[i1])  # Current index
        x0 = x[i]          # Start of the current window
        xf = x[i * 2]      # End of the current window

        # Ensure the window is within bounds
        if xf < max_x:
            e = i * 2  # Compute the end index
            if e < len_x:
                # Compute the mean x and y values for the interval
                yout[i1] = np.nanmean(y[i:e])
                xoutmean[i1] = np.nanmean(x[i:e])

    return xoutmean, yout



def TracePSD(x,y,z,dt, norm = None):
    """ 
    Estimate Power spectral density:

    Inputs:

    u : timeseries, np.array
    dt: 1/sampling frequency

    norm = 'forward'
    can be {“backward”, “ortho”, “forward”}
    see https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.rfft.html

    'forward' method can keep the transformed spectrum comparable with different sampling frequency. 'ortho' will conserve energy between real space and fourier transformed space.

    """
    
    B_pow = np.abs(np.fft.rfft(x, norm=norm))**2 \
          + np.abs(np.fft.rfft(y, norm=norm))**2 \
          + np.abs(np.fft.rfft(z, norm=norm))**2

    freqs = np.fft.rfftfreq(len(x), dt)

    coeff = len(x)/(2*dt)
    
    return freqs, B_pow/coeff


def trace_PSD_wavelet(x, y, z, dt, dj, consider_coi=True):
    """
    Calculate the power spectral density (PSD) using wavelet transform.

    Parameters
    ----------
    x, y, z : array-like
        Components of the field to transform.
    dt : float
        Sampling time of the time series.
    dj : float
        Scale resolution; smaller values increase the number of scales.
    consider_coi : bool, optional (default=True)
        Whether to consider the Cone of Influence (CoI) in PSD estimation.

    Returns
    -------
    db_x, db_y, db_z : array-like
        Wavelet coefficients for the x, y, z components.
    freqs : array-like
        Frequencies corresponding to the PSD points.
    PSD : array-like
        Power spectral density of the signal.
    scales : array-like
        Wavelet scales used for the transform.
    coi : array-like
        Cone of Influence (CoI) indicating regions affected by edge effects.
    """
    mother = wavelet.Morlet()

    db_x, scales, freqs, coi, _, _ = wavelet.cwt(x, dt, dj, wavelet=mother)
    db_y, _, _, _, _, _ = wavelet.cwt(y, dt, dj, wavelet=mother)
    db_z, _, _, _, _, _ = wavelet.cwt(z, dt, dj, wavelet=mother)

    if consider_coi:
        PSD = np.zeros_like(freqs)
        for i, scale in enumerate(scales):
            valid = coi > scale

            if np.any(valid):
                PSD[i] = (
                    np.nanmean(np.abs(db_x[i, valid]) ** 2) +
                    np.nanmean(np.abs(db_y[i, valid]) ** 2) +
                    np.nanmean(np.abs(db_z[i, valid]) ** 2)
                ) * (2 * dt)
            else:
                PSD[i] = np.nan
    else:
        PSD = (
            np.nanmean(np.abs(db_x) ** 2, axis=1) +
            np.nanmean(np.abs(db_y) ** 2, axis=1) +
            np.nanmean(np.abs(db_z) ** 2, axis=1)
        ) * (2 * dt)

    return db_x, db_y, db_z, freqs, PSD, scales, coi