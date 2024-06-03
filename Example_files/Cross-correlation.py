import numpy as np
import matplotlib.pyplot as plt

center_freq = 434e6
sample_rate = 2.048e6


def calculate_phase_cross_correlation(received_samples, reference_signal):
    """
    Funtion to calculate the phase difference using cross correlation
    :param received_samples: The measured signal
    :param reference_signal: The reference signal
    :return: Nothing
    """
    # Downsample the received samples and the reference signal by a factor
    downsample_factor = 100
    downsampled_samples = received_samples[::downsample_factor]
    downsampled_reference = reference_signal[:len(downsampled_samples)]

    # Cross-correlate the complex IQ data
    correlation = np.correlate(downsampled_samples, downsampled_reference, mode='full')
    max_index = np.argmax(np.abs(correlation))

    # Get the phase difference at the point of maximum correlation
    phase_difference = np.angle(correlation[max_index])

    return phase_difference


# Create a reference signal
duration = 5  # Duration in seconds
t = np.arange(int(sample_rate * duration)) / sample_rate
reference_signal = np.exp(1j * 2 * np.pi * center_freq * t)

# Create a phase-shifted signal (20 degrees phase shift)
phase_shift = np.deg2rad(20)  # Convert 20 degrees to radians
shifted_signal = reference_signal * np.exp(1j * phase_shift)

# Calculate phase difference
phase_difference = calculate_phase_cross_correlation(shifted_signal, reference_signal)
phase_difference_degrees = np.degrees(phase_difference)  # Convert radians to degrees

print(f"Calculated Phase Difference: {phase_difference_degrees:.2f} degrees")

# Plot the reference signal, phase-shifted signal, and the calculated phase shift
plt.figure(figsize=(12, 6))

# Plot reference signal
plt.plot(t[:1000], np.real(reference_signal[:1000]), label='Reference Signal (Real Part)', alpha=0.75)
# Plot phase-shifted signal
plt.plot(t[:1000], np.real(shifted_signal[:1000]), label='Phase-Shifted Signal (Real Part)', alpha=0.75)

plt.title('Reference Signal, Phase-Shifted Signal, and Calculated Phase Difference')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend(loc='upper right')
plt.grid()
plt.tight_layout()
plt.show()
