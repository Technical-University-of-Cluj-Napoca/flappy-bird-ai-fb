# ====================================================================
# 2. Autonomous Agent Class (FlappyBirdAgent)
# Represents an individual bird with its own perceptron brain.
# ====================================================================
from typing import Union

from GAME_CONSTANTS import SCREEN_HEIGHT, SCREEN_WIDTH, VELOCITY_AFTER_FLAP
import Perceptron
from Pipe import Pipe



class FlappyBirdAgent:
    def __init__(self, brain_weights=None):
        self.x:int = SCREEN_HEIGHT // 2
        self.y:int = SCREEN_WIDTH // 10
        self.velocity:int = 0
        self.is_alive:bool = True
        self.is_flapping:bool = False  # Boolean state describing whether the bird is in the middle of the jump [cite: 178]
        self.brain = Perceptron.Perceptron(brain_weights)
        self.distance_traveled: int = 0
        self.score:int = 0

        set_bird_def(self)

    def flap(self):
        if not self.is_flapping:
            self.velocity = VELOCITY_AFTER_FLAP  # Example jump velocity
            self.is_flapping = True

    def get_sensors(self, pipes: Union[tuple[Pipe, Pipe], tuple[None, Pipe]]) -> tuple[int,int,int]:
        """
        Get the input vector (i0, i1, i2, bias) for the perceptron.
        The bird will have 3 senses[cite: 145].
        """
        # Find the next pipe the bird has to pass through

        distance_nex_pipe = pipes[1].left_x - self.y

        pipe:Pipe = pipes[0]
        if pipe is None:
            pipe = pipes[1]

        up_distance = self.x - pipe.left_up
        down_distance = pipe.left_down - self.x

        return up_distance, distance_nex_pipe, down_distance

    def make_decision(self, sensors: tuple[int,int,int]):

        if not self.is_alive:
            raise NotImplementedError

        """
        Calculates the decision to flap or not using the perceptron.
        The bird only has to take one decision: Flap (1) or No Flap (0)[cite: 142].
        """
        output = self.brain.feed_forward(sensors)

        # Decision logic: jump only when falling AND output > threshold [cite: 177]
        threshold = 0.5  # Example threshold
        if output > threshold:
            self.flap()

def set_bird_def(bird: FlappyBirdAgent):
    bird.is_alive = True
    bird.is_flapping = False
    bird.x = SCREEN_HEIGHT // 2
    bird.y = SCREEN_WIDTH // 10
    bird.velocity = 0
    bird.distance_traveled = 0
    bird.score = 0