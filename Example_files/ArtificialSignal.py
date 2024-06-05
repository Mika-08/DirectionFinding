import numpy as np
import matplotlib.pyplot as plt

# Define the sample rate and durations
sample_rate = 2.048e6  # 1 GHz sample rate
on_duration = int(0.03 * sample_rate)
off_duration_short = int(0.03 * sample_rate)
off_duration_long = int(0.91 * sample_rate)

# Create the base signal pattern
ref = np.concatenate([
    np.ones(on_duration),
    np.zeros(off_duration_short),
    np.ones(on_duration),
    np.zeros(off_duration_long)
])

# Define the carrier frequency
carrier_frequency = 434  # 343 MHz

# Generate the time vector for the base signal
t = np.arange(len(ref)) / sample_rate

# Generate the carrier signal
carrier_signal = np.cos(2 * np.pi * carrier_frequency * t)

# Modulate the base signal with the carrier
modulated_signal = ref * carrier_signal


# Plot the base signal and the modulated signal
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t, ref)
plt.title('Base Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.subplot(2, 1, 2)
plt.plot(t, modulated_signal)
plt.title('Modulated Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()
