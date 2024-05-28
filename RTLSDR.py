# from rtlsdr import *
# import threading
# from matplotlib import pyplot
#
# class Receiver:
#     def __init__(self):
#         self.samples = None
#         self.sample_lock = threading.Lock()
#         self.sdr = RtlSdr()
#
#         # Configure SDR settings
#         self.sdr.sample_rate = 2.048e6  # Hz
#         self.sdr.center_freq = 433.96e6  # Hz
#         self.sdr.gain = 'auto'
#
#     def receive_samples(self):
#         while True:
#             samples = self.sdr.read_samples(256 * 1024)  # Read samples from the SDR
#             with self.sample_lock:
#                 self.samples = samples
#
#     def get_samples(self):
#         receive_thread = threading.Thread(target=self.receive_samples, args=(self.sdr,))
#         receive_thread.daemon = True  # Allows program to exit even if the thread is running
#         receive_thread.start()
#         #
#         # # Start the processing loop in the main thread
#         # try:
#         #     process_samples()
#         # except KeyboardInterrupt:
#         #     print("Terminating...")
#
#
# receiver = Receiver()
# receiver.get_samples()
# receiver.sdr.close()
#
# # use matplotlib to estimate and plot the PSD
# pyplot.psd(receiver.samples, NFFT=1024, Fs=receiver.sdr.sample_rate/1e6, Fc=receiver.sdr.center_freq/1e6)
# pyplot.xlabel('Frequency (MHz)')
# pyplot.ylabel('Relative power (dB)')
#
# pyplot.show()
#


# from rtlsdr import RtlSdr
# import threading
# import numpy as np
# from matplotlib import pyplot as plt
# from matplotlib.animation import FuncAnimation

# class Receiver:
#     def __init__(self):
#         self.samples = None
#         self.sample_lock = threading.Lock()
#         self.sdr = RtlSdr()

#         # Configure SDR settings
#         self.sdr.sample_rate = 2.048e6  # Hz
#         self.sdr.center_freq = 433.96e6  # Hz
#         self.sdr.gain = 'auto'

#         # Flag to stop the receiving thread
#         self.terminate_flag = threading.Event()

#     def receive_samples(self):
#         """
#         PYDOC HERE
#         """
#         while True:
#             while not self.terminate_flag.is_set():
#                 samples = self.sdr.read_samples(256 * 1024)  # Read samples from the SDR
#                 with self.sample_lock:
#                     self.samples = samples

#     def start_receiving(self):
#         self.receive_thread = threading.Thread(target=self.receive_samples)
#         self.receive_thread.daemon = True  # Allows program to exit even if the thread is running
#         self.receive_thread.start()

#     def stop_receiving(self):
#         self.terminate_flag.set()
#         self.receive_thread.join()
#         self.sdr.close()

#     def get_samples(self):
#         with self.sample_lock:
#             return self.samples

# # Initialize receiver and start receiving samples
# receiver = Receiver()
# receiver.start_receiving()

# # Create a figure and axis for plotting
# fig, ax = plt.subplots()
# line, = ax.plot([], [], lw=2)

# def init():
#     ax.set_xlim(433.96e6 - 1e6, 433.96e6 + 1e6)
#     ax.set_ylim(-100, 0)
#     return line,

# def update(frame):
#     samples = receiver.get_samples()
#     if samples is not None:
#         # Compute the PSD
#         freqs, psd = plt.psd(samples, NFFT=1024, Fs=receiver.sdr.sample_rate / 1e6, Fc=receiver.sdr.center_freq / 1e6)
#         line.set_data(freqs, 10 * np.log10(psd))
#     return line,

# # Set up the animation
# ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=1000)

# # Show the plot
# plt.show()

# # Stop receiving samples when closing the plot
# receiver.stop_receiving()


from pylab import *
from rtlsdr import *
from time import sleep    
import scipy.signal as sp
sdr = RtlSdr()    
sdr.sample_rate = 2.4e6
sdr.center_freq = 434e6
sdr.gain = 50    

on = [1] * 72000
off = [0] * 72000
#delay = [0] * 2184000
delay = [0] * 1092000

ref_signal = on + off + on + off + delay

# Initialize an empty list to accumulate samples
accumulated_samples = []

try:
    while True: # run until interrupted
        samples = sdr.read_samples(256*1024)
        # Append new samples to the accumulated list
        accumulated_samples.extend(samples)
        clf()
        # psd(samples.real, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
        # xlabel('Frequency (MHz)')
        # ylabel('Relative power (dB)')
        # show()
        output =  sp.correlate(ref_signal, accumulated_samples)     
        plt.plot(output)
        plt.xlabel('Sample')
        plt.ylabel('Value')
        plt.title('output cross correlation')
        plt.grid()
        plt.show()
        sleep(0.1) # sleep for 1s
except:
    pass
sdr.close()
#test 4 seconds
# t_end = time.time() + 4
# while time.time() < t_end:
#     samples = sdr.read_samples(256*1024)
#     accumulated_samples.extend(samples)
# sdr.close()
print(len(accumulated_samples))
output =  sp.correlate(ref_signal, accumulated_samples)     
plt.plot(output)
plt.xlabel('Sample')
plt.ylabel('Value')
plt.title('output cross correlation')
plt.grid()
plt.show()




# import numpy as np
# import threading
# from matplotlib import pyplot as plt
# from matplotlib.animation import FuncAnimation
# from rtlsdr import RtlSdr

# class Receiver:
#     def _init_(self):
#         self.samples = None
#         self.sample_lock = threading.Lock()
#         self.sdr = RtlSdr()

#         # Configure SDR settings
#         self.sdr.sample_rate = 2.048e6  # Hz
#         self.sdr.center_freq = 433e6  # Hz
#         self.sdr.gain = 'auto'

#         # Flag to stop the receiving thread
#         self.terminate_flag = threading.Event()

#     def receive_samples(self):
#         while not self.terminate_flag.is_set():
#             samples = self.sdr.read_samples(256 * 1024)  # Read samples from the SDR
#             with self.sample_lock:
#                 self.samples = samples

#     def start_receiving(self):
#         self.receive_thread = threading.Thread(target=self.receive_samples)
#         self.receive_thread.daemon = True  # Allows program to exit even if the thread is running
#         self.receive_thread.start()

#     def stop_receiving(self):
#         #self.terminate_flag.set()
#         self.receive_thread.join()
#         self.sdr.close()

#     def get_samples(self):
#         with self.sample_lock:
#             return self.samples

# # Initialize receiver and start receiving samples
# receiver = Receiver()
# receiver.start_receiving()

# # Create a figure and axis for plotting
# fig, ax = plt.subplots()
# line, = ax.plot([], [], lw=2)

# def init():
#     ax.set_xlim(0, 1)
#     ax.set_ylim(0, 1)
#     return line,

# def update(frame):
#     samples = receiver.get_samples()
#     if samples is not None:
#         # Compute the signal power
#         power = np.abs(samples)**2
#         power_mean = np.mean(power.reshape(-1, 1024), axis=1)  # Average power over blocks of samples

#         # Update the plot with the power data
#         x_data = np.linspace(0, len(power_mean) * 1024 / receiver.sdr.sample_rate, len(power_mean))
#         y_data = power_mean / np.max(power_mean)  # Normalize the power for plotting

#         line.set_data(x_data, y_data)
#         ax.set_xlim(0, x_data[-1])
#         ax.set_ylim(0, 1)
#     return line,

# # Set up the animation
# ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=1000)

# # Show the plot
# plt.show()

# # Stop receiving samples when closing the plot
# receiver.stop_receiving()