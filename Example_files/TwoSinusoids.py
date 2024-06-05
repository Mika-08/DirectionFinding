import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


# Plotting sinusoids with a phase difference in Python

# Define the parameters for the sinusoids
amplitude = 1
frequency = 1  # 1 Hz
phase_diff_degrees = 20
phase_diff_radians = np.deg2rad(phase_diff_degrees)
period = 1 / frequency  # Period of the sinusoid
num_periods = 1.5

# Create a time array for 1.5 periods
t = np.linspace(0, num_periods * period, 1000)

# Generate the two sinusoids
sinusoid1 = amplitude * np.sin(2 * np.pi * frequency * t)
sinusoid2 = amplitude * np.sin(2 * np.pi * frequency * t + phase_diff_radians)

# Plot the sinusoids
plt.figure(figsize=(10, 6))
plt.plot(t, sinusoid1, label='Sinusoid 1')
plt.plot(t, sinusoid2, label=f'Sinusoid 2 (Phase difference: {phase_diff_degrees}°)')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Two Sinusoids with a Phase Difference')
plt.legend()
plt.grid(True)
# plt.show()


def calculate_phase_cross_correlation(received_samples, reference_signal):
    """
    Function to calculate the phase of the received signal using cross-correlation with a reference signal
    :param received_samples: The samples from the antenna's
    :return: phase difference of the received signal
    """
    # Downsample the received samples and the reference signal by a factor
    downsample_factor = 150
    downsampled_samples = received_samples[::downsample_factor]
    downsampled_reference = reference_signal[:len(downsampled_samples)]

    downsampled_samples = received_samples
    downsampled_reference = reference_signal

    # Cross-correlate the complex IQ data
    correlation = np.correlate(downsampled_samples, downsampled_reference, mode='full')
    print(correlation)
    max_index = np.argmax(np.abs(correlation))

    # Get the phase difference at the point of maximum correlation
    phase_difference = np.angle(correlation[max_index])

    return phase_difference


# Calculate phase difference
phase_difference = calculate_phase_cross_correlation(sinusoid1, sinusoid2)
phase_difference_degrees = np.degrees(phase_difference)  # Convert radians to degrees

print(f"Calculated Phase Difference: {phase_difference_degrees:.2f} degrees")
