import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import Receiver


def calculate_phase_cross_correlation(received_samples, reference_signal):
    # Downsample the received samples and the reference signal by a factor
    downsample_factor = 150
    downsampled_samples = received_samples[::downsample_factor]
    downsampled_reference = reference_signal[:len(downsampled_samples)]

    # Cross-correlate the complex IQ data
    correlation = np.correlate(downsampled_samples, downsampled_reference, mode='full')
    max_index = np.argmax(np.abs(correlation))

    # Get the phase difference at the point of maximum correlation
    phase_difference = np.angle(correlation[max_index])

    return phase_difference


center_freq = 434e6
sample_rate = 2.048e6
duration = 5  # Time interval in seconds

# Create a reference signal (repeating pattern)
reference_signal = np.exp(1j * 2 * np.pi * np.arange(int(sample_rate * 0.03)) / sample_rate)
reference_signal = np.concatenate(
    [reference_signal, np.zeros(int(sample_rate * 0.03)), reference_signal, np.zeros(int(sample_rate * 0.91))])
repeat_count = int(np.ceil(sample_rate * duration / len(reference_signal)))
reference_signal = np.tile(reference_signal, repeat_count)

# Initialize receivers
receiver1 = Receiver.Receiver(center_freq, sample_rate, device_index=0)
receiver2 = Receiver.Receiver(center_freq, sample_rate, device_index=1)

receiver1.start_receiving()
receiver2.start_receiving()

x_data = np.linspace(-duration, 0, int(duration * sample_rate))
y_data1 = np.zeros(int(duration * sample_rate))
# Create a figure and axis for plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

phase_data_1 = []
phase_data_2 = []

line1, = ax1.plot([], [], lw=2, label='Phase Difference 1')
line2, = ax2.plot([], [], lw=2, label='Phase Difference 2')

ax1.set_ylim(-180, 180)
ax1.set_xlim(-duration, 0)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Phase difference (degrees)')
ax1.set_title('Phase difference - RTL-SDR 1')
ax1.legend(loc='upper right')

ax2.set_ylim(-180, 180)
ax2.set_xlim(-duration, 0)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Phase Difference (degrees)')
ax2.set_title('Phase Difference - RTL-SDR 2')
ax2.legend(loc='upper right')

def init():
    """
    Initialize the plot
    :return:
    """
    return line1, line2


def update(frame):
    """
    Function that updates the plot real-time
    :return: The lines to plot
    """
    samples1 = receiver1.get_samples()
    samples2 = receiver2.get_samples()

    if samples1 is not None and samples2 is not None:
        # Calculate phase difference
        phase_difference_1 = calculate_phase_cross_correlation(samples1, reference_signal)
        phase_difference_degrees_1 = np.degrees(phase_difference_1)  # Convert radians to degrees

        # Update the phase difference plot
        phase_data_1.append(phase_difference_degrees_1)
        if len(phase_data_1) > len(x_data):
            phase_data_1.pop(0)

        line1.set_data(np.linspace(-duration, 0, len(phase_data_1)), phase_data_1)

        # Calculate phase difference
        phase_difference_2 = calculate_phase_cross_correlation(samples2, reference_signal)
        phase_difference_degrees_2 = np.degrees(phase_difference_2)  # Convert radians to degrees

        # Update the phase difference plot
        phase_data_2.append(phase_difference_degrees_2)
        if len(phase_data_2) > len(x_data):
            phase_data_2.pop(0)

        line2.set_data(np.linspace(-duration, 0, len(phase_data_2)), phase_data_2)




        print(phase_difference_degrees_1 - phase_difference_degrees_2)

    return line1, line2


# Set up the animation
ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=50, cache_frame_data=False)

plt.tight_layout()
plt.show()
receiver1.stop_receiving()
receiver2.stop_receiving()
