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
        self.create_reference_signal()

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
        repeat_count = int(np.ceil(self.sample_rate / len(reference_signal)))
        reference_signal = np.tile(reference_signal, repeat_count)

        self.signal = reference_signal
