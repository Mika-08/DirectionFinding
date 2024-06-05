import numpy as np


class ReferenceSignal:
    def __init__(self, sample_rate):
        """
        Constructor function for the reference signal class
        :param sample_rate: Sample rate with which the dongles sample
        """
        self.signal = None
        self.sample_rate = sample_rate
        self.gold_code = [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0]
        self.create_reference_signal_gold_code()

    def create_reference_signal_gold_code(self):
        signal = []
        bit_time = 0.01613

        bit_duration = int(bit_time * self.sample_rate)

        for value in self.gold_code:
            if value == 1:
                signal.append(np.ones(bit_duration))
            else:
                signal.append(np.zeros(bit_duration))

        # Concatenate the list of arrays into a single array
        self.signal = np.concatenate(signal)

    def create_reference_signal(self):
        """
        Function that creates a reference signal form the code
        :return: Nothing
        """
        on_duration = int(0.03 * self.sample_rate)
        off_duration_short = int(0.03 * self.sample_rate)
        off_duration_long = int(0.91 * self.sample_rate)

        reference_signal = np.concatenate([
            np.ones(on_duration),
            np.zeros(off_duration_short),
            np.ones(on_duration),
            np.zeros(off_duration_long)
        ])

        # Repeat the pattern to ensure it's long enough
        reference_signal = np.tile(reference_signal, 100)

        self.signal = reference_signal
