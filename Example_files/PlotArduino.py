import numpy as np
import matplotlib.pyplot as plt

sample_rate = 2.048e6

on_duration = int(0.03 * sample_rate)
off_duration_short = int(0.03 * sample_rate)
off_duration_long = int(0.91 * sample_rate)

reference_signal = np.concatenate([
    np.ones(on_duration),
    np.zeros(off_duration_short),
    np.ones(on_duration),
    np.zeros(off_duration_long)
])

# Repeat the pattern to ensure it's long enough
reference_signal = np.tile(reference_signal, 5)


# Plot the reference signal, phase-shifted signal, and the calculated phase shift
plt.figure(figsize=(12, 6))
t = np.arange(0, len(reference_signal))

# Plot reference signal
plt.plot(t, np.real(reference_signal), alpha=0.75)


plt.title('Ideal arduino signal')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()

