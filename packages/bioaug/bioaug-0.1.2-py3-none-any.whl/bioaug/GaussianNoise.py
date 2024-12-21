import numpy as np
from src.tool import generate_seed

class GaussianNoise(object):
    """Jittering the input time-series data randomly with a given probability.

    Args:
        p       (float) : Probability of applying gaussian noise to the input signal.
        SNR     (float, tuple, list) : SNR can be a fixed value, a range (min_SNR, max_SNR), or a list of possible values.
        seed    (int)   : A seed value for the random number generator.
    """
    def __init__(self, p=0.5, SNR=20):
        self.p = p
        self.SNR = SNR

    def _select_value(self, param):
        """Helper function to select a value from param if it's a tuple or list."""
        if isinstance(param, (int, float)):
            return param
        elif isinstance(param, tuple) and len(param) == 2:
            return np.random.uniform(param[0], param[1])
        elif isinstance(param, list):
            return np.random.choice(param)
        else:
            raise ValueError("Parameter must be an int, float, tuple of length 2, or list.")

    def __call__(self, signal):
        """signal: [sequence_length, input_dim]"""
        if np.random.uniform(0, 1) < self.p:
            seed = generate_seed()
            signal_ = np.array(signal).copy()
            np.random.seed(seed)
            sequence_length = signal_.shape[0]
            input_dim = signal_.shape[1]

            selected_snr = int(self._select_value(self.SNR))
            for i in range(input_dim):
                noise = np.random.randn(sequence_length)
                noise = noise - np.mean(noise)
                signal_power = (1 / sequence_length) * np.sum(np.power(signal_[:, i], 2))
                noise_variance = signal_power / np.power(10, (selected_snr / 10))
                noise = (np.sqrt(noise_variance) / np.std(noise)) * noise
                signal_[:, i] = signal_[:, i] + noise
            return signal_
        return signal


if __name__ == '__main__':
    gn = GaussianNoise(p=1.0, SNR=(20, 30))
    data = np.random.random(size=(400, 1))
    for i in range(100):
        gn(data)