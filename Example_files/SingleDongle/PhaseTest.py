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
wavelength = 3e8 / center_freq  # Speed of light divided by center frequency


on_duration = int(0.03 * sample_rate)
off_duration_short = int(0.03 * sample_rate)
off_duration_long = int(0.91 * sample_rate)

# Make the reference signal
ref = np.concatenate([
    np.ones(on_duration),
    np.zeros(off_duration_short),
    np.ones(on_duration),
    np.zeros(off_duration_long)
])


def makeSignal(ref, sample_rate):
    # Define the carrier frequency
    carrier_frequency = 434  # 343 MHz

    # Generate the time vector for the base signal
    t = np.arange(len(ref)) / sample_rate

    # Generate the carrier signal
    carrier_signal = np.cos(2 * np.pi * carrier_frequency * t)

    # Modulate the base signal with the carrier
    modulated_signal = ref * carrier_signal

    return modulated_signal


def zero_pad_array(arr, desired_length):
    """
    Function that adds additional zeros to the array
    :param arr: Array to be altered
    :param desired_length: Length which the altered array needs to be
    :return: The altered array
    """
    current_length = len(arr)
    if current_length < desired_length:
        padding = desired_length - current_length
        arr = np.pad(arr, (0, padding), 'constant', constant_values=(0,))
    return arr


def makePeak(ref, samples1):
    """
    Function to calculate the time difference and phase difference between the received signal and the reference signal
    :param ref: Reference signal
    :param samples1: Received signal
    :return: The time delay and phase difference
    """
    begin_time = time.time()

    downsampling_factor = 1
    ref = ref[::downsampling_factor]
    samples1 = samples1[::downsampling_factor]

    length_ref = len(ref)
    length_samples = len(samples1)

    total_length = length_ref + length_samples - 1

    ref = zero_pad_array(ref, total_length)
    samples1 = zero_pad_array(samples1, total_length)

    mult1 = np.flip(scipy.fft.fft(np.conj(ref))) * scipy.fft.fft(samples1)
    ifft = np.abs(scipy.fft.ifft(mult1))

    td = np.linspace(0, total_length / sample_rate, total_length)
    # print(td)
    est_delay = (td[np.argmax(np.abs(ifft))] * downsampling_factor) % 1

    T = 1
    phase_delay = 2 * np.pi * 1 / T * est_delay
    phase_delay_degrees = np.rad2deg(phase_delay)

    time_delta = time.time() - begin_time
    print(F"Elapsed time  is {time_delta} seconds")

    return est_delay, phase_delay


modulated_ref = makeSignal(ref, sample_rate)

# Create a figure and axis for plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

x_data = np.linspace(-duration, 0, int(duration * sample_rate))
y_data1 = np.zeros(int(duration * sample_rate))
phase_data = []

line1, = ax1.plot(x_data, y_data1, lw=2, label='Receiver 1')
line2, = ax2.plot([], [], lw=2, label='Phase Difference')

ax1.set_ylim(0, 2)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax1.set_title('Received Signal - RTL-SDR 1')
ax1.legend(loc='upper right')

ax2.set_ylim(0, 360)
ax2.set_xlim(-duration, 0)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Phase Difference (degrees)')
ax2.set_title('Phase Difference')
ax2.legend(loc='upper right')


def init():
    """
    Initialize the plot
    :return:
    """
    line1.set_ydata(np.zeros_like(x_data))
    line2.set_data([], [])
    return line1, line2


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

        # Calculate phase difference
        time, phase_difference = makePeak(modulated_ref, samples1)
        print(F"The time difference between the reference and the shifted signal is: {time} seconds."
              F" The phase difference is: {np.rad2deg(phase_difference)} degrees.")
        phase_difference_degrees = np.degrees(phase_difference)  # Convert radians to degrees

        # Update the phase difference plot
        phase_data.append(phase_difference_degrees)
        if len(phase_data) > len(x_data):
            phase_data.pop(0)

        line2.set_data(np.linspace(-duration, 0, len(phase_data)), phase_data)

    return line1, line2


# Set up the animation
ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=50, cache_frame_data=False)

# Show the plot
plt.tight_layout()
plt.show()

receiver.stop_receiving()
