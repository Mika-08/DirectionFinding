import numpy as np

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

        modulated_ref = makeSignal(reference_signal, self.sample_rate)

        self.signal = modulated_ref
