import numpy as np
import scipy
import matplotlib.pyplot as plt


center_freq = 434e6
sample_rate = 2.048e6
duration = 5  # Duration in seconds
wavelength = 3e8 / center_freq  # Speed of light divided by center frequency


def plot(signal1, signal2, signal3, phase):
    y1 = np.arange(0, len(signal1))/1000000
    y2 = np.arange(0, len(signal2))/1000000
    y3 = np.arange(0, len(signal3))/1000000

    plt.plot(y1, np.abs(signal1), label="Reference signal")
    plt.plot(y2, np.abs(signal2), label="Shifted signal 1, 0.05 s")
    plt.plot(y3, np.abs(signal3), label="Shifted signal 2, 0.08 s")
    plt.legend()
    plt.title(F"Reference signal and two shifted signals \n"
              F"Calculated phase difference between the two signals: {phase:.01f} degrees.")
    plt.ylabel("Amplitude")
    plt.xlabel("Time (s)")
    plt.show()


on_duration = int(0.03 * sample_rate)
off_duration_short = int(0.03 * sample_rate)
off_duration_long = int(0.91 * sample_rate)

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


def addTimeShift(s, t0, sample_rate):
    n = len(s)
    fft_signal = scipy.fft.fft(s)

    # Calculate the frequencies for each component
    freqs = np.fft.fftfreq(n, d=1 / sample_rate)

    # Create the phase shift array for the given time shift t0
    phase_shifts = np.exp(-1j * 2 * np.pi * freqs * t0)

    # Apply the phase shifts to the FFT signal
    shifted_fft_signal = fft_signal * phase_shifts

    # Compute the inverse FFT to get the time-shifted signal
    shifted_signal = scipy.fft.ifft(shifted_fft_signal)

    return shifted_signal


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
    est_delay = td[np.argmax(np.abs(ifft))] * downsampling_factor

    T = 1
    phase_delay = 2 * np.pi * 1/T * est_delay
    phase_delay_degrees = np.rad2deg(phase_delay)

    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
    #
    # ax.plot(td, np.abs(ifft))
    # ax.set_title('Reference and Delayed Signal Cross-Correlation')
    # ax.grid()
    # ax.set_xlabel('Delay [s]')
    # ax.set_ylabel('Magnitude')
    #
    # fig.tight_layout()
    # plt.show()

    return est_delay, phase_delay


def time_delay(ref, samples1, samples2):
    """
    Function to calculate the time difference and phase difference between two signal
    :param ref: Reference signal
    :param samples1: Received signal 1
    :param samples2: Received signal 2
    :return: The time difference and phase difference
    """
    downsampling_factor = 1
    ref = ref[::downsampling_factor]
    samples1 = samples1[::downsampling_factor]
    samples2 = samples2[::downsampling_factor]

    length_ref = len(ref)
    length_samples = len(samples1)

    total_length = length_ref + length_samples - 1

    ref = zero_pad_array(ref, total_length)
    samples1 = zero_pad_array(samples1, total_length)
    samples2 = zero_pad_array(samples2, total_length)

    mult1 = np.flip(scipy.fft.fft(np.conj(ref))) * scipy.fft.fft(samples1)
    mult2 = np.flip(scipy.fft.fft(np.conj(ref))) * scipy.fft.fft(samples2)

    near0 = 1.0e-16
    # mult1 = np.where(mult1 < near0, near0, mult1)
    # mult2 = np.where(mult2 < near0, near0, mult2)

    if np.argmax(np.abs(scipy.fft.ifft(mult2))) > np.argmax(np.abs(scipy.fft.ifft(mult1))):
        ifft = np.abs(scipy.fft.ifft(mult2 / mult1))

    else:
        ifft = np.abs(scipy.fft.ifft(mult1 / mult2))

    td = np.linspace(0, total_length / sample_rate, total_length)
    est_delay = td[np.argmax(np.abs(ifft))] * downsampling_factor

    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
    #
    # ax.plot(td, np.abs(ifft))
    # ax.set_title('Reference and Delayed Signal Cross-Correlation')
    # ax.grid()
    # ax.set_xlabel('Delay [s]')
    # ax.set_ylabel('Magnitude')
    #
    # fig.tight_layout()
    # plt.show()

    # plot(ref, samples1, mult1)

    T = 1
    phase_delay = 2 * np.pi * 1/T * est_delay
    phase_delay_degrees = np.rad2deg(phase_delay)

    return est_delay, phase_delay

def makeNoise(signal):
    target_snr_db = 20

    x_watts = signal ** 2
    # Calculate signal power and convert to dB
    sig_avg_watts = np.mean(x_watts)
    sig_avg_db = 10 * np.log10(sig_avg_watts)
    # Calculate noise according to [2] then convert to watts
    noise_avg_db = sig_avg_db - target_snr_db
    noise_avg_watts = 10 ** (noise_avg_db / 10)
    # Generate a sample of white noise
    mean_noise = 0
    noise_volts = np.random.normal(mean_noise, np.sqrt(noise_avg_watts), len(x_watts))

    # Add the noise to the data.
    return signal + noise_volts


modulated_ref = makeSignal(ref, sample_rate)

shifted = addTimeShift(modulated_ref, 0.05, sample_rate)
shifted2 = addTimeShift(modulated_ref, 0.08, sample_rate)

shifted = makeNoise(shifted)
shifted2 = makeNoise(shifted2)

# plot(ref, shifted, shifted2)

delay1, phase1 = makePeak(modulated_ref, shifted)
print(F"The time difference between the reference and the shifted signal is: {delay1} seconds."
      F" The phase difference is: {np.rad2deg(phase1)} degrees.")

delay2, phase2 = makePeak(modulated_ref, shifted2)
print(F"The time difference between the reference and the shifted signal is: {delay2} seconds."
      F" The phase difference is: {np.rad2deg(phase2)} degrees.")

delay3, phase3 = time_delay(modulated_ref, shifted, shifted2)
print(F"The time difference between the two shifted signals is: {delay3} seconds."
      F" The phase difference is: {np.rad2deg(phase3)} degrees.")

aoa = np.arcsin(phase3/np.pi)
print(F"The angle of arrival is {np.rad2deg(aoa)} degrees.")

plot(modulated_ref, shifted, shifted2, np.rad2deg(phase3))
