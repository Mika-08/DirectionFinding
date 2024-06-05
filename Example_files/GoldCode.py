import numpy as np
import matplotlib.pyplot as plt

center_freq = 434e6
sample_rate = 2.048e6
gold_code = [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0]

bit_time = 0.01613

on_duration = int(bit_time * sample_rate)
off_duration_short = int(bit_time * sample_rate)

# Initialize an empty list to store the signal
signal = []

for value in gold_code:
    if value == 1:
        signal.append(np.ones(on_duration))
    else:
        signal.append(np.zeros(off_duration_short))

# Concatenate the list of arrays into a single array
signal = np.concatenate(signal)


td = np.linspace(0, len(signal)/sample_rate, len(signal))

plt.plot(td, signal)
plt.title("Gold code")
plt.ylabel("Amplitude")
plt.xlabel("Time (s)")
plt.show()
