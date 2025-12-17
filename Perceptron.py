# ====================================================================
# 3. The Brain (Perceptron)
# A mathematical model for decision making.
# ====================================================================
import math
import random


class Perceptron:
    """
    A single layer perceptron, used by the autonomous birds[cite: 140].
    """

    def __init__(self, weights=None):
        # The perceptron has 4 inputs (i0, i1, i2, i3/bias) and one output [cite: 154]
        # It therefore needs 4 weights (w0, w1, w2, w3)
        if weights is None:
            # Initialize weights randomly between [-1, 1] [cite: 139]
            # Use smaller initial weights to avoid overflow
            self.weights = [random.uniform(-0.1, 0.1) for _ in range(4)]
        else:
            self.weights = weights

    def sigmoid(self, x):
        """
        The nonlinear/activation function is the sigmoid function[cite: 166].
        Output is between (0, 1), ideal for computing decisions with probability[cite: 168].
        Safe implementation that prevents overflow errors.
        """
        # Clamp x to prevent overflow
        # sigmoid(x) ≈ 1 for x > 20
        # sigmoid(x) ≈ 0 for x < -20
        x = max(-500, min(500, x))

        try:
            # \sigma(x) = 1 / (1 + e^{-x}) [cite: 167]
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            # Fallback for extreme values
            return 1.0 if x > 0 else 0.0

    def feed_forward(self, inputs):
        """
        Calculates the output of the perceptron: result = sigma(W^T * I) [cite: 170]
        Inputs should be normalized for better performance.
        """
        # Normalize inputs to prevent overflow
        # Scale large pixel values down to reasonable range
        normalized_inputs = [
            inputs[0] / 1000.0,  # up_distance (0-1080 range -> 0-1.08)
            inputs[1] / 2000.0,  # distance_to_next_pipe (0-1920 range -> 0-0.96)
            inputs[2] / 1000.0,  # down_distance (0-1080 range -> 0-1.08)
            inputs[3]  # bias (always 1)
        ]

        # Linear multiplication: f(I) = W^T * I = w0*i0 + w1*i1 + w2*i2 + w3*b [cite: 157, 162]
        linear_output = sum(w * i for w, i in zip(self.weights, normalized_inputs))

        # Pass the result to the activation function [cite: 163]
        result = self.sigmoid(linear_output)

        return result