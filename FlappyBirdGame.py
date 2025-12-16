# ====================================================================
# 1. Game Environment Class (FlappyBirdGame)
# Handles all physics, rendering, and game-specific logic.
# ====================================================================
import sys
from typing import Union

import pygame
import random
import math

from FlappyBirdAgent import FlappyBirdAgent, set_bird_def
from GAME_CONSTANTS import SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_WIDTH, BIRD_DIMENSION, GRAVITY, PIPE_SPEED, PIPE_DISTANCE, \
    PIPE_GAP
from Pipe import Pipe

# Constants (Adjust as needed for screen size, bird size, etc.)



def image_color_transparent(path: str, size: float, color:tuple[int,int,int]) -> pygame.Surface:
    image_full = pygame.transform.scale(pygame.image.load(path),(size, size)).convert_alpha()
    image_full.set_colorkey(color)
    return image_full

class Images:
    def __init__(self):
        self.background = pygame.transform.scale(pygame.image.load("Background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pipe = pygame.transform.scale(pygame.image.load("Pipe.png"), (PIPE_WIDTH, SCREEN_HEIGHT))
        self.bird = image_color_transparent("Bird.png", BIRD_DIMENSION, (255, 0, 0))
        self.pipe_top = pygame.transform.scale(pygame.image.load("Pipe_TOP.png"), (PIPE_WIDTH * 1.1, SCREEN_HEIGHT * 0.1))


class FlappyBirdGame:
    def __init__(self, autonomous_mode=True):
        # Initialize Pygame and game assets (Skins, Sprites, Sounds)
        # ... (Setup screen, clock, load images for bird, pipes, background)
        self.autonomous_mode = autonomous_mode
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pipes:list[Pipe] = []
        self.score = 0
        self.game_over = False
        self.close_game = False
        self.curr_poz_left = 0
        self.images = Images()


    def update_pipes(self):
        update_done:bool = False
        l = len(self.pipes)
        if l == 0:
            self.pipes.append(self.new_pipe(int(SCREEN_WIDTH * 0.33), PIPE_WIDTH, PIPE_GAP))
        while not update_done:
            ref_poz = 0
            l = len(self.pipes)
            if l > 0:
                ref_poz = self.pipes[0].left_x
            if ref_poz < 0:
                self.pipes.remove(self.pipes[0])
            elif self.pipes[l-1].left_x + PIPE_DISTANCE <= SCREEN_WIDTH:
                self.pipes.append(self.new_pipe(self.pipes[l-1].left_x + PIPE_DISTANCE, PIPE_WIDTH, PIPE_GAP))
            else:
                update_done = True


    def new_pipe(self, y:int, pipe_width:int, pipe_gap:int) -> Pipe:
        down_pipe = random.randint( int(SCREEN_HEIGHT * 0.2), int(SCREEN_HEIGHT * 0.8))
        return Pipe(down_pipe + pipe_gap, down_pipe, pipe_width, y)


    def update_physics(self, bird: FlappyBirdAgent):
        # Apply gravity (Faby is affected by gravity [cite: 58])
        bird.velocity += GRAVITY
        bird.y += bird.velocity

        # Check for floor collision
        if bird.x > SCREEN_HEIGHT or bird.x < 0:  # Assuming 50 is ground level
            bird.is_alive = False

        # Move pipes
        # ... (Update pipe positions)

        for pipe in self.pipes:
            pipe.left_x -= PIPE_SPEED

    def check_collision(self, bird: FlappyBirdAgent) -> bool:
        for pipe in self.pipes:
            if pipe.left_down >= bird.x and pipe.left_up <= bird.x + BIRD_DIMENSION:
                continue
            if pipe.left_x >= bird.y and pipe.left_x + pipe.width <= bird.y + BIRD_DIMENSION:
                continue
            return True
        return False

    def update_game_state(self, birds: list[FlappyBirdAgent]):
        pygame.event.pump()
        self.update_pipes()
        for bird in birds:
            self.update_physics(bird)
            if self.check_collision(bird):
                bird.is_alive = False
        """Main loop for one step of the game."""
        # 1. Update pipe positions and generate new ones
        # 2. Update bird physics (gravity, position)
        # 3. Check collision
        # 4. Update score (Each successful pass through a pair of pipes awards the player one point [cite: 62])
        pass

    def render(self, bird: FlappyBirdAgent):
        self.screen.blit(self.images.background, (0,0))
        for pipe in self.pipes:
            self.screen.blit(pygame.transform.scale(self.images.pipe, (PIPE_WIDTH, pipe.left_down)), (pipe.left_x, pipe.left_down))
            self.screen.blit(pygame.transform.scale(self.images.pipe, (PIPE_WIDTH, SCREEN_HEIGHT - pipe.left_up)), (pipe.left_x, 0))
        self.screen.blit(self.images.bird, (bird.y, bird.x))
        pass

    # --- Manual Mode Specifics ---
    def manual_input(self, bird):
        # Handle user input (click or space bar) to make Faby flap [cite: 59, 107]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            bird.flap()
        if keys[pygame.K_r]:
            self.reset_game_state(bird)
        if keys[pygame.K_ESCAPE]:
            self.close_game = True
        pass

    def next_pipe(self, poz_y:int) -> Union[tuple[Pipe, Pipe], tuple[None, Pipe]]:
        l = len(self.pipes)
        for i in range(l-1):
            if self.pipes[i].left_x <= poz_y <= self.pipes[i+1].left_x:
                if self.pipes[i].left_x + self.pipes[i].width <= poz_y:
                    return self.pipes[i], self.pipes[i+1]
                else:
                    return None, self.pipes[i+1]
        raise NotImplementedError


    def reset_game_state(self, bird: FlappyBirdAgent):
        set_bird_def(bird)
        game_reset(self)
        pass

    def game_loop(self):
        bird = FlappyBirdAgent()
        while not self.close_game:
            self.manual_input(bird)
            self.update_game_state([bird])
            self.render(bird)
            pygame.display.update()
            if not bird.is_alive:
                self.reset_game_state(bird)


def game_reset(game: FlappyBirdGame):
    game.pipes = []
    game.score = 0
    game.game_over = False
    game.curr_poz_left = 0