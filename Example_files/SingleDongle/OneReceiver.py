import numpy as np
import scipy
import matplotlib.pyplot as plt
import Receiver
from matplotlib.animation import FuncAnimation
import time

center_freq = 434e6
sample_rate = 2.048e6
receiver = Receiver.Receiver(center_freq, sample_rate)
receiver.start_receiving()
duration = 5  # Duration in seconds


# Create a figure and axis for plotting
fig, (ax1) = plt.subplots(1, 1, figsize=(10, 8))

x_data = np.linspace(-duration, 0, int(duration * sample_rate))
y_data1 = np.zeros(int(duration * sample_rate))
phase_data = []

line1, = ax1.plot(x_data, y_data1, lw=2, label='Receiver 1')

ax1.set_ylim(0, 2)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax1.set_title('Received Signal - RTL-SDR 1')
ax1.legend(loc='upper right')


def init():
    """
    Initialize the plot
    :return:
    """
    line1.set_ydata(np.zeros_like(x_data))
    return line1,


def update(frame):
    """
    Function that updates the plot real-time
    :return: The lines to plot
    """
    samples1 = receiver.get_samples()

    if samples1 is not None:
        # Update the plot data for the received signal
        y_data1[:] = np.abs(samples1[:int(duration * sample_rate)])
        line1.set_ydata(y_data1)

    return line1,


# Set up the animation
ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=50, cache_frame_data=False)

# Show the plot
plt.tight_layout()
plt.show()

receiver.stop_receiving()
