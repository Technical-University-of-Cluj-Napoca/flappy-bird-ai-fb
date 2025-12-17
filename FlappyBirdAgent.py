# ====================================================================
# 2. Autonomous Agent Class (FlappyBirdAgent)
# Represents an individual bird with its own perceptron brain.
# ====================================================================
from typing import Union
import random

from GAME_CONSTANTS import SCREEN_HEIGHT, SCREEN_WIDTH, VELOCITY_AFTER_FLAP
from Perceptron import Perceptron
from Pipe import Pipe


class FlappyBirdAgent:
    def __init__(self, brain_weights=None):
        # Give each bird a DIFFERENT starting position for true diversity
        self.x: int = random.randint(SCREEN_HEIGHT // 4, SCREEN_HEIGHT // 2)
        self.y: int = random.randint(SCREEN_WIDTH // 20, SCREEN_WIDTH // 5)

        # Larger random initial velocity
        self.velocity: float = random.uniform(-2, 2)

        self.is_alive: bool = True
        self.is_flapping: bool = False
        self.brain = Perceptron(brain_weights)
        self.distance_traveled: int = 0
        self.score: int = 0

    def flap(self):
        self.velocity = VELOCITY_AFTER_FLAP

    def get_sensors(self, pipes: Union[tuple[Pipe, Pipe], tuple[None, Pipe], tuple[None, None]]) -> tuple[
        int, int, int, int]:
        """
        Get the input vector (i0, i1, i2, bias) for the perceptron.
        Returns: (up_distance, distance_to_next_pipe, down_distance, bias)
        """
        # Handle case where there are no pipes yet
        if pipes[0] is None and pipes[1] is None:
            return (SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2, 1)

        # Determine which pipe to use for measurements
        if pipes[1] is not None:
            target_pipe = pipes[1]
            distance_to_next_pipe = target_pipe.left_y - self.y
        else:
            target_pipe = pipes[0]
            distance_to_next_pipe = SCREEN_WIDTH

        # If we're between pipes, use the next pipe
        measuring_pipe = pipes[0] if pipes[0] is not None else pipes[1]

        # Calculate distances to pipe opening
        up_distance = self.x - measuring_pipe.left_up
        down_distance = measuring_pipe.left_down - self.x

        return (up_distance, distance_to_next_pipe, down_distance, 1)

    def make_decision(self, sensors: tuple[int, int, int, int]):
        if not self.is_alive:
            return

        """
        Calculates the decision to flap or not using the perceptron.
        The bird only has to take one decision: Flap (1) or No Flap (0)[cite: 142].
        """
        output = self.brain.feed_forward(sensors)

        # Decision logic: jump when output > threshold
        threshold = 0.5

        if output > threshold:
            self.flap()


def set_bird_def(bird: FlappyBirdAgent):
    """Reset bird but keep its brain (weights)"""
    bird.is_alive = True
    bird.is_flapping = False
    # Give random starting position each generation
    bird.x = random.randint(SCREEN_HEIGHT // 4, SCREEN_HEIGHT // 2)
    bird.y = random.randint(SCREEN_WIDTH // 20, SCREEN_WIDTH // 5)
    bird.velocity = random.uniform(-2, 2)
    bird.distance_traveled = 0
    bird.score = 0

    bird.flap()