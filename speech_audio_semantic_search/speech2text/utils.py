from typing import List, TYPE_CHECKING
import IPython.display as ipd
import matplotlib.pyplot as plt
import numpy as np


def batch_data(data: np.array, batch_size):
    return [
        data[i : min(i + batch_size, len(data))]
        for i in range(0, len(data), batch_size)
    ]


def print_plot_play(x, Fs, text=""):
    """1. Prints information about an audio singal, 2. plots the waveform, and 3. Creates player

    Notebook: C1/B_PythonAudio.ipynb

    Args:
        x: Input signal
        Fs: Sampling rate of x
        text: Text to print
    """
    print(
        "%s Fs = %d, x.shape = %s, x.dtype = %s" % (text, Fs, x.shape, x.dtype)
    )
    plt.figure(figsize=(8, 2))
    time = np.arange(0, x.shape[0] / Fs, 1 / Fs)
    plt.plot(time, x, color="gray")
    # plt.xlim([0, x.shape[0]])
    plt.xlabel("Time (samples)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.show()
    ipd.display(ipd.Audio(data=x, rate=Fs))
