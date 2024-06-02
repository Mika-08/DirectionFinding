import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import Receiver

center_freq = 434e6
sample_rate = 2.048e6
duration = 5  # Duration in seconds
wavelength = 3e8 / center_freq  # Speed of light divided by center frequency

receiver1 = Receiver.Receiver(center_freq, sample_rate, device_index=0)
receiver2 = Receiver.Receiver(center_freq, sample_rate, device_index=1)
receiver1.start_receiving()
receiver2.start_receiving()

def calculate_phase_cross_correlation(received_samples, reference_signal):
    # Ensure the reference signal length matches the received samples length
    if len(reference_signal) > len(received_samples):
        reference_signal = reference_signal[:len(received_samples)]
    else:
        reference_signal = np.tile(reference_signal, int(np.ceil(len(received_samples) / len(reference_signal))))[
                           :len(received_samples)]

    # Downsample the received samples by a factor
    downsample_factor = 100
    downsampled_samples = received_samples[::downsample_factor]
    downsampled_reference = reference_signal[:len(downsampled_samples)]

    # Cross-correlate the complex IQ data
    correlation = np.correlate(downsampled_samples, downsampled_reference, mode='full')
    max_index = np.argmax(np.abs(correlation))

    # Get the phase difference at the point of maximum correlation
    phase_difference = np.angle(correlation[max_index])

    return phase_difference

def calculate_angle_of_arrival(phase1, phase2):
    # Calculate the phase difference between the two signals
    phase_difference = phase1 - phase2
    # Ensure the phase difference is within the range [-pi, pi]
    phase_difference = np.arctan2(np.sin(phase_difference), np.cos(phase_difference))

    # Calculate the angle of arrival
    sin_theta = phase_difference / np.pi
    # Ensure sin_theta is in the valid range [-1, 1]
    sin_theta = np.clip(sin_theta, -1, 1)
    angle_of_arrival = np.arcsin(sin_theta)
    # Convert to degrees
    angle_of_arrival_degrees = np.rad2deg(angle_of_arrival) + 90
    return angle_of_arrival_degrees

# Create a reference signal
t = np.arange(int(sample_rate * duration)) / sample_rate
reference_signal = np.exp(1j * 2 * np.pi * center_freq * t)

# Create a figure and axis for plotting
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))

x_data = np.linspace(-duration, 0, int(duration * sample_rate))
y_data1 = np.zeros(int(duration * sample_rate))
phase_data = []
angle_data = []

line1, = ax1.plot(x_data, y_data1, lw=2, label='Receiver 1')
line2, = ax2.plot([], [], lw=2, label='Phase Difference')
line3, = ax3.plot([], [], lw=2, label='Angle of Arrival')

ax1.set_ylim(0, 2)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax1.set_title('Received Signal - RTL-SDR 1')
ax1.legend(loc='upper right')

ax2.set_ylim(-180, 180)
ax2.set_xlim(-duration, 0)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Phase Difference (degrees)')
ax2.set_title('Phase Difference')
ax2.legend(loc='upper right')

ax3.set_ylim(-0, 180)
ax3.set_xlim(-duration, 0)
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Angle of Arrival (degrees)')
ax3.set_title('Angle of Arrival')
ax3.legend(loc='upper right')

def init():
    """
    Initialize the plot
    :return:
    """
    line1.set_ydata(np.zeros_like(x_data))
    line2.set_data([], [])
    line3.set_data([], [])
    return line1, line2, line3

def update(frame):
    """
    Function that updates the plot real-time
    :return: The lines to plot
    """
    samples1 = receiver1.get_samples()
    samples2 = receiver2.get_samples()

    if samples1 is not None and samples2 is not None:
        # Update the plot data for the received signal
        y_data1[:] = np.abs(samples1[:int(duration * sample_rate)])
        line1.set_ydata(y_data1)

        # Calculate phase for each receiver
        phase1 = calculate_phase_cross_correlation(samples1, reference_signal)
        phase2 = calculate_phase_cross_correlation(samples2, reference_signal)
        phase_difference_degrees = np.degrees(phase1 - phase2)  # Convert radians to degrees

        # Update the phase difference plot
        phase_data.append(phase_difference_degrees)
        if len(phase_data) > len(x_data):
            phase_data.pop(0)
        line2.set_data(np.linspace(-duration, 0, len(phase_data)), phase_data)

        # Calculate angle of arrival
        angle_of_arrival_degrees = calculate_angle_of_arrival(phase1, phase2)
        print(angle_of_arrival_degrees)
        angle_data.append(angle_of_arrival_degrees)
        if len(angle_data) > len(x_data):
            angle_data.pop(0)
        line3.set_data(np.linspace(-duration, 0, len(angle_data)), angle_data)

    return line1, line2, line3

# Set up the animation
ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=50, cache_frame_data=False)

# Show the plot
plt.tight_layout()
plt.show()

# Stop receiving samples when closing the plot
receiver1.stop_receiving()
receiver2.stop_receiving()
