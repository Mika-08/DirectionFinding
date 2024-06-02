import numpy as np
import multiprocessing
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from rtlsdr import RtlSdr
import Receiver
import threading


def calculate_phase_cross_correlation(received_samples, reference_signal):
    # Downsample the received samples by a factor of 10
    downsampled_samples = received_samples[::10]

    correlation = np.correlate(downsampled_samples, reference_signal[:len(downsampled_samples)], mode='same')
    max_index = np.argmax(correlation)
    phase_difference = np.angle(downsampled_samples[max_index])
    phase_degrees = np.degrees(phase_difference)  # Convert radians to degrees
    return phase_degrees


def update(frame, queue, reference_signal):
    if not queue.empty():
        samples = queue.get()
        phase = calculate_phase_cross_correlation(samples, reference_signal)
        x_data.append(frame)
        y_data.append(phase)
        if len(x_data) > 100:
            x_data.pop(0)
            y_data.pop(0)
        line.set_data(x_data, y_data)
        ax.set_xlim(x_data[0], x_data[-1])
        ax.set_ylim(-180, 180)  # Phase range in degrees
    return line,


center_freq = 433e6
sample_rate = 2.048e6
receiver = Receiver.Receiver(center_freq, sample_rate)
queue = multiprocessing.Queue()
process = multiprocessing.Process(target=receiver.receive_samples, args=(queue,))
process.start()

reference_signal = np.concatenate([
    np.ones(int(0.03 * sample_rate)),
    np.zeros(int(0.03 * sample_rate)),
    np.ones(int(0.03 * sample_rate)),
    np.zeros(int(0.91 * sample_rate))
])

fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], lw=2)


def init():
    ax.set_xlim(0, 10)
    ax.set_ylim(-180, 180)  # Phase range in degrees
    return line,


ani = FuncAnimation(fig, update, fargs=(queue, reference_signal), init_func=init, blit=True, interval=100)
plt.show()

receiver.terminate_flag.set()
process.join()
