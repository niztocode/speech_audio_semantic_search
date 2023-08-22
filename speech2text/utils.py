import IPython.display as ipd
import matplotlib.pyplot as plt


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
    plt.plot(x, color="gray")
    plt.xlim([0, x.shape[0]])
    plt.xlabel("Time (samples)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.show()
    ipd.display(ipd.Audio(data=x, rate=Fs))
