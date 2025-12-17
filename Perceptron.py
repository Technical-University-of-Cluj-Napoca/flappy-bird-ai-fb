
import math
import random


class Perceptron:
    def __init__(self, weights=None):

        if weights is None:
            self.weights = [random.uniform(-0.1, 0.1) for _ in range(4)]
        else:
            self.weights = weights

    def sigmoid(self, x):

        x = max(-500, min(500, x))

        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            # Fallback for extreme values
            return 1.0 if x > 0 else 0.0
    def feed_forward(self, inputs):

        normalized_inputs = [
            inputs[0] / 1000.0,
            inputs[1] / 2000.0,
            inputs[2] / 1000.0,
            inputs[3]
        ]

        # Linear multiplication: f(I) = W^T * I = w0*i0 + w1*i1 + w2*i2 + w3*b
        linear_output = sum(w * i for w, i in zip(self.weights, normalized_inputs))

        result = self.sigmoid(linear_output)

        return result