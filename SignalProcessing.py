import Kalman
import numpy as np
import Receiver
import ReferenceSignal
import scipy


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


def time_delay(ref, samples1, samples2, sample_rate):
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

    if np.argmax(np.abs(scipy.fft.ifft(mult2))) > np.argmax(np.abs(scipy.fft.ifft(mult1))):
        ifft = np.abs(scipy.fft.ifft(mult2 / mult1))

    else:
        ifft = np.abs(scipy.fft.ifft(mult1 / mult2))

    td = np.linspace(0, total_length / sample_rate, total_length)
    est_delay = (td[np.argmax(np.abs(ifft))] * downsampling_factor) % 1

    T = 1
    phase_delay = 2 * np.pi * 1 / T * est_delay
    phase_delay_degrees = np.rad2deg(phase_delay)

    return est_delay, phase_delay


class SignalProcessing:
    def __init__(self):
        """
        Constructor for the signal processing class
        """
        self.status = False
        self.kalman = Kalman.Kalman()
        self.center_freq = 434e6
        self.sample_rate = 2.048e6

        self.rx1 = Receiver.Receiver(self.center_freq, self.sample_rate, device_index=0)
        self.rx2 = Receiver.Receiver(self.center_freq, self.sample_rate, device_index=1)
        self.reference_signal = ReferenceSignal.ReferenceSignal(self.sample_rate)

        self.past_data = []

    def disable_receiving(self):
        """
        Function to let the sdr dongles receive
        :return: Nothing
        """
        self.rx1.stop_receiving()
        self.rx2.stop_receiving()

        self.save_data()
        self.past_data = []

    def enable_receiving(self):
        """
        Function to let the sdr dongles stop with receiving
        :return: Nothing
        """
        self.rx1.start_receiving()
        self.rx2.start_receiving()

    def save_data(self):
        """
        Function to save the last tracking to a file
        :return: Nothing
        """
        print(self.past_data)
        output_file = open("Output.txt", "w")
        for data in self.past_data:
            output_file.write(str(data))
            output_file.write("\n")

    def calculate_delta_phi(self):
        """
        Function to calculate the phase difference between the two received signals
        :return: delta_phi, the phase difference
        """
        # Get samples
        samples1 = self.rx1.get_samples()
        samples2 = self.rx2.get_samples()

        modulated_ref = self.reference_signal.signal

        delay, phase = time_delay(modulated_ref, samples1, samples2, self.sample_rate)
        delta_phi = phase

        return delta_phi

    def calculate_aoa(self):
        """
        Function to calculate the angle of arrival with the delta_phi
        :return: Angle of arrival
        """
        delta_phi = self.calculate_delta_phi()
        # Ensure the phase difference is within the range [-pi, pi]
        delta_phi = np.arctan2(np.sin(delta_phi), np.cos(delta_phi))

        # Calculate the angle of arrival
        sin_theta = delta_phi / np.pi
        # Ensure sin_theta is in the valid range [-1, 1]
        sin_theta = np.clip(sin_theta, -1, 1)
        angle_of_arrival = np.arcsin(sin_theta)
        # Convert to degrees
        angle_of_arrival_degrees = np.rad2deg(angle_of_arrival)

        # if angle_of_arrival_degrees < 0:
        #     angle_of_arrival_degrees += 360
        #
        # if len(self.past_data) > 0:
        #     angle_of_arrival_degrees = self.adjust_aoa(angle_of_arrival_degrees)

        print(angle_of_arrival_degrees)

        self.past_data.append(angle_of_arrival_degrees)
        return angle_of_arrival_degrees

    # def adjust_aoa(self, aoa):
    #     """
    #     Function to account for 180 phase ambiguity
    #     :param aoa: calculated aoa
    #     :return: adjusted aoa
    #     """
    #     new_aoa = aoa
    #
    #     # Does not work yet
    #     previous_aoa = self.past_data[-1]
    #     if (np.abs(aoa - previous_aoa)) > 30:
    #         if previous_aoa >= 45:
    #             new_aoa = aoa - 180
    #             print("decrease")
    #
    #         elif 270 <= previous_aoa <= 315:
    #             new_aoa = aoa + 180
    #             print("add")
    #
    #     return aoa

    def calculate_distance(self):
        """
        Function to calculate the distance to the receiver using the RSSI
        :return: Distance
        """
        distance = 250

        return distance
