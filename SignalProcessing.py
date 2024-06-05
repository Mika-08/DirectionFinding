import Kalman
import numpy as np
import Receiver
import ReferenceSignal


def synchronize_signals(samples1, samples2):
    # Todo: synchronize the dongles

    return samples1, samples2


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

    def calculate_phase_cross_correlation(self, received_samples):
        """
        Function to calculate the phase of the received signal using cross-correlation with a reference signal
        :param received_samples: The samples from the antenna's
        :return: phase difference of the received signal
        """
        # Downsample the received samples and the reference signal by a factor
        downsample_factor = 150
        downsampled_samples = received_samples[::downsample_factor]
        downsampled_reference = self.reference_signal.signal[:len(downsampled_samples)]

        # Cross-correlate the complex IQ data
        correlation = np.correlate(downsampled_samples, downsampled_reference, mode='full')
        max_index = np.argmax(np.abs(correlation))

        # Get the phase difference at the point of maximum correlation
        phase_difference = np.angle(correlation[max_index])

        return phase_difference

    def calculate_delta_phi(self):
        """
        Function to calculate the phase difference between the two received signals
        :return: delta_phi, the phase difference
        """
        # Get samples
        samples1 = self.rx1.get_samples()
        samples2 = self.rx2.get_samples()

        # Synchronize antennas
        samples1, samples2 = synchronize_signals(samples1, samples2)

        # Calculate phase difference
        phase_difference1 = self.calculate_phase_cross_correlation(samples1)
        phase_difference_degrees1 = np.degrees(phase_difference1)  # Convert radians to degrees

        phase_difference2 = self.calculate_phase_cross_correlation(samples2)
        phase_difference_degrees2 = np.degrees(phase_difference2)  # Convert radians to degrees

        delta_phi = phase_difference_degrees1 - phase_difference_degrees2

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

        if angle_of_arrival_degrees < 0:
            angle_of_arrival_degrees += 360

        if len(self.past_data) > 0:
            angle_of_arrival_degrees = self.adjust_aoa(angle_of_arrival_degrees)

        print(angle_of_arrival_degrees)

        self.past_data.append(angle_of_arrival_degrees)
        return angle_of_arrival_degrees

    def adjust_aoa(self, aoa):
        """
        Function to account for 180 phase ambiguity
        :param aoa: calculated aoa
        :return: adjusted aoa
        """
        new_aoa = aoa

        # Does not work yet
        previous_aoa = self.past_data[-1]
        if (np.abs(aoa - previous_aoa)) > 30:
            if previous_aoa >= 45:
                new_aoa = aoa - 180
                print("decrease")

            elif 270 <= previous_aoa <= 315:
                new_aoa = aoa + 180
                print("add")

        return aoa

    def calculate_distance(self):
        """
        Function to calculate the distance to the receiver using the RSSI
        :return: Distance
        """
        distance = 250

        return distance
