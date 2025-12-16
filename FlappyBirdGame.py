# ====================================================================
# 1. Game Environment Class (FlappyBirdGame)
# Handles all physics, rendering, and game-specific logic.
# ====================================================================
import sys
from typing import Union

import pygame
import random
import Button

from FlappyBirdAgent import FlappyBirdAgent, set_bird_def
from GAME_CONSTANTS import SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_WIDTH, BIRD_DIMENSION, GRAVITY, PIPE_SPEED, PIPE_DISTANCE, \
    PIPE_GAP
from Pipe import Pipe

# Constants (Adjust as needed for screen size, bird size, etc.)

GAME_RUNNING = 0
GAME_PAUSE = 1
GAME_GAME_OVER = 2
GAME_MENU = 3
GAME_CLOSE = 4

COLOR_BUTTON: tuple[int,int,int] = (255,127,39)
COLOR_BLACK: tuple[int,int,int] = (0,0,0)


def image_color_transparent(path: str, size: float, color:tuple[int,int,int]) -> pygame.Surface:
    image_full = pygame.transform.scale(pygame.image.load(path),(size, size)).convert_alpha()
    image_full.set_colorkey(color)
    return image_full

class Images:
    def __init__(self):
        self.background = pygame.transform.scale(pygame.image.load("Background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pipe = pygame.transform.scale(pygame.image.load("Pipe.png"), (PIPE_WIDTH, SCREEN_HEIGHT))
        self.bird = image_color_transparent("Bird.png", BIRD_DIMENSION, (255, 0, 0))
        self.pipe_top = pygame.transform.scale(pygame.image.load("Pipe_TOP.png"), (SCREEN_WIDTH * 1.1, SCREEN_HEIGHT * 0.1))
        i = pygame.transform.scale(pygame.image.load("FlapyBirdText.png"), (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.2))
        i.set_colorkey(COLOR_BLACK)
        self.fb_text = i
        self.game_over = pygame.transform.scale(pygame.image.load("GameOverText.png"), (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.2))

class Buttons:
    def __init__(self, screen):
        self.auto_mode = Button.Button(screen, (int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.66))
                                       , "automatic mode", COLOR_BUTTON, COLOR_BLACK, 100)
        self.manual_mode = Button.Button(screen, (int(SCREEN_WIDTH * 0.55), int(SCREEN_HEIGHT * 0.66))
                                         , "manual mode", COLOR_BUTTON, COLOR_BLACK, 100)
        self.continue_button = Button.Button(screen, (int(SCREEN_WIDTH * 0.45), int(SCREEN_HEIGHT * 0.66)),
                                             "continue", COLOR_BUTTON, COLOR_BLACK, 100)
        self.play = Button.Button(screen, (int(SCREEN_WIDTH * 0.4), int(SCREEN_HEIGHT * 0.8)),
                                             "play", COLOR_BUTTON, COLOR_BLACK, 100)

class FlappyBirdGame:
    def __init__(self, autonomous_mode=False):
        self.autonomous_mode:bool = autonomous_mode
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pipes:list[Pipe] = []
        self.score = 0
        self.status = GAME_MENU
        self.curr_poz_left = 0
        self.images = Images()
        self.flap_key_pressed:bool = False
        self.buttons:Buttons = Buttons(self.screen)
        self.distance = 0
        self.first_pipe_pass_dis = 0

        game_reset(self)
    def update_pipes(self):
        update_done:bool = False
        l = len(self.pipes)
        if l == 0:
            self.pipes.append(self.new_pipe(int(SCREEN_WIDTH * 0.33), PIPE_WIDTH, PIPE_GAP))
            self.first_pipe_pass_dis = self.pipes[0].left_y + PIPE_WIDTH
        while not update_done:
            ref_poz = 0
            l = len(self.pipes)
            if l > 0:
                ref_poz = self.pipes[0].left_y + self.pipes[0].width
            if ref_poz < 0:
                self.pipes.remove(self.pipes[0])
            elif self.pipes[l-1].left_y + PIPE_DISTANCE <= SCREEN_WIDTH:
                self.pipes.append(self.new_pipe(self.pipes[l-1].left_y + PIPE_DISTANCE, PIPE_WIDTH, PIPE_GAP))
            else:
                update_done = True
    def new_pipe(self, y:int, pipe_width:int, pipe_gap:int) -> Pipe:
        up_pipe = random.randint( int(SCREEN_HEIGHT * 0.2), int(SCREEN_HEIGHT * 0.8) - pipe_gap)
        # print("up_pipe = ", up_pipe)
        # print(up_pipe + pipe_gap, up_pipe, y)
        return Pipe(up_pipe + pipe_gap, up_pipe, pipe_width, y)
    def update_physics(self, bird: FlappyBirdAgent):
        bird.velocity += GRAVITY
        bird.x += bird.velocity

        if bird.x + BIRD_DIMENSION > SCREEN_HEIGHT or bird.x < 0:  # Assuming 50 is ground level
            bird.is_alive = False

        for pipe in self.pipes:
            pipe.left_y -= PIPE_SPEED
    def check_collision(self, bird: FlappyBirdAgent) -> bool:
        for pipe in self.pipes:
            if pipe.collides_with(bird.x, bird.y, BIRD_DIMENSION):
                return True
        return False
    def update_game_state(self, birds: list[FlappyBirdAgent]):
        if self.status != GAME_RUNNING:
            return
        self.distance += PIPE_SPEED
        self.score = max((self.distance - self.first_pipe_pass_dis) // PIPE_DISTANCE + 2, 0)
        pygame.event.pump()
        self.update_pipes()
        for bird in birds:
            self.update_physics(bird)
            if self.check_collision(bird):
                bird.is_alive = False

        if not self.autonomous_mode:
            for bird in birds:
                if not bird.is_alive:
                    self.status = GAME_GAME_OVER
        pass
    def render(self, birds: list[FlappyBirdAgent]):
        if self.status == GAME_RUNNING or self.status == GAME_GAME_OVER:
            self.render_game(birds)
        elif self.status == GAME_GAME_OVER:
            self.renter_game_over()
        elif self.status == GAME_MENU:
            self.render_menu()
        else:
            print("status = ", self.status)
            raise NotImplementedError
        pass
    def renter_game_over(self):
        self.screen.blit(self.images.game_over, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        pass
    def render_menu(self):
        self.screen.blit(self.images.fb_text, (SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.25))
        self.buttons.auto_mode.draw()
        self.buttons.manual_mode.draw()
        self.buttons.play.draw()
        pass
    def render_game(self, birds: list[FlappyBirdAgent]):
        self.screen.blit(self.images.background, (0, 0))
        for pipe in self.pipes:
            self.screen.blit(pygame.transform.scale(self.images.pipe, (PIPE_WIDTH, pipe.left_up)), (pipe.left_y, 0))
            print((PIPE_WIDTH, SCREEN_HEIGHT - pipe.left_down), (pipe.left_y, pipe.left_down))
            self.screen.blit(pygame.transform.scale(self.images.pipe, (PIPE_WIDTH, SCREEN_HEIGHT - pipe.left_down)),
                             (pipe.left_y, pipe.left_down))
        for bird in birds:
            self.screen.blit(self.images.bird, (bird.y, bird.x))

        draw_text(self.screen, (int(SCREEN_WIDTH * 0.48), int(SCREEN_HEIGHT * 0.1)), "Score: %d" % self.score)
    def manual_input(self, bird):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.status = GAME_CLOSE
        if self.status == GAME_RUNNING:
            self.manual_input_game(bird)
        elif self.status == GAME_MENU:
            self.manual_input_menu()
        pass
    def manual_input_menu(self):
        if self.status != GAME_MENU:
            raise NotImplementedError
        if self.buttons.auto_mode.click():
            self.autonomous_mode = True
        if self.buttons.manual_mode.click():
            self.autonomous_mode = False
        if self.buttons.play.click():
            self.status = GAME_RUNNING
    def manual_input_game(self, bird):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if not self.flap_key_pressed:
                bird.flap()
                self.flap_key_pressed = True
        else:
            self.flap_key_pressed = False
        if keys[pygame.K_r]:
            self.reset_game_state(bird)
        if keys[pygame.K_ESCAPE]:
            self.status = GAME_CLOSE
        pass
    def next_pipe(self, poz_y:int) -> Union[tuple[Pipe, Pipe], tuple[None, Pipe]]:
        l = len(self.pipes)
        for i in range(l-1):
            if self.pipes[i].left_y <= poz_y <= self.pipes[i + 1].left_y:
                if self.pipes[i].left_y + self.pipes[i].width <= poz_y:
                    return self.pipes[i], self.pipes[i+1]
                else:
                    return None, self.pipes[i+1]
        raise NotImplementedError
    def reset_game_state(self, bird: FlappyBirdAgent):
        set_bird_def(bird)
        game_reset(self)
        pass
    def reset_game_state_birds(self, birds: list[FlappyBirdAgent]):
        for bird in birds:
            set_bird_def(bird)
        game_reset(self)
        pass
    def game_loop(self):
        bird = FlappyBirdAgent()
        while self.status != GAME_CLOSE:
            print("automatic_mode = ", self.autonomous_mode)
            if self.autonomous_mode:
                return
            self.manual_input(bird)
            self.update_game_state([bird])
            self.render([bird])
            pygame.display.update()
            if not bird.is_alive:
                #self.close_game = True
                self.reset_game_state(bird)

def game_reset(game: FlappyBirdGame):
    game.pipes = []
    game.score = 0
    game.status = GAME_MENU
    game.curr_poz_left = 0
    game.distance = 0
    game.first_pipe_pass_dis = 0
def draw_text(screen, poz: tuple[int, int], text: str):
    pygame.event.get()  # process events to prevent freezing
    font = pygame.font.SysFont("Arial", 40)
    text_surface = font.render(text, True, COLOR_BLACK)
    screen.blit(text_surface, poz)