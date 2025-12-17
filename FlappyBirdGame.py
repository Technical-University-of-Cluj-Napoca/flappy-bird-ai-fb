
import sys
from typing import Union

import pygame
import random
import Button

from FlappyBirdAgent import FlappyBirdAgent, set_bird_def
from GAME_CONSTANTS import SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_WIDTH, BIRD_DIMENSION, GRAVITY, PIPE_SPEED, PIPE_DISTANCE, \
    PIPE_GAP, set_d_p, ORIGINAL_PIPE_DISTANCE, set_speed, ORIGINAL_PIPE_SPEED
from Pipe import Pipe

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
        self.bird = image_color_transparent("Ryan.png", BIRD_DIMENSION, (255, 0, 0))
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
        self.d_first_pipe = 0

        game_reset(self)

    def update_pipes(self):
        update_done:bool = False
        l = len(self.pipes)
        if l == 0:
            self.pipes.append(self.new_pipe(int(SCREEN_WIDTH * 0.33), PIPE_WIDTH, PIPE_GAP))
            self.d_first_pipe = self.pipes[0].left_y + self.pipes[0].width
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
        up_pipe = random.randint( int(SCREEN_HEIGHT * 0.1), int(SCREEN_HEIGHT * 0.9) - pipe_gap)
        return Pipe(up_pipe + pipe_gap, up_pipe, pipe_width, y)
    def update_physics(self, bird: FlappyBirdAgent):
        bird.velocity += GRAVITY
        bird.x += bird.velocity

        if bird.x + BIRD_DIMENSION > SCREEN_HEIGHT or bird.x < 0:  # Assuming 50 is ground level
            bird.is_alive = False


    def check_collision(self, bird: FlappyBirdAgent) -> bool:
        for pipe in self.pipes:
            if pipe.collides_with(bird.x, bird.y, BIRD_DIMENSION):
                return True
        return False
    def update_game_state(self, birds: list[FlappyBirdAgent]):

        self.distance += PIPE_SPEED
        self.score = max(int(((self.distance - self.d_first_pipe + SCREEN_WIDTH * 0.33) / PIPE_DISTANCE)), 0)
        for bird in birds:
            if bird.is_alive:
                bird.score = self.score
            print("bird score = ", bird.score, " is live = ", bird.is_alive, "mode auto = ",
                  self.autonomous_mode, "game score = ", self.score, "game d = ", self.distance)
        pygame.event.pump()
        self.update_pipes()
        for pipe in self.pipes:
            pipe.left_y -= PIPE_SPEED
        for bird in birds:
            self.update_physics(bird)

            if bird.x + BIRD_DIMENSION > SCREEN_HEIGHT or bird.x < 0:
                bird.is_alive = False

            if self.check_collision(bird):
                bird.is_alive = False

        if not self.autonomous_mode:
            no_bird_live = True
            for bird in birds:
                if bird.is_alive:
                    no_bird_live = False
            if no_bird_live:
                self.reset_game_state_birds(birds)
                self.status = GAME_MENU

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
            self.screen.blit(pygame.transform.scale(self.images.pipe, (PIPE_WIDTH, pipe.left_up)),
                             (pipe.left_y, 0))
            self.screen.blit(pygame.transform.scale(self.images.pipe, (PIPE_WIDTH, SCREEN_HEIGHT - pipe.left_down)),
                             (pipe.left_y, pipe.left_down))

        for bird in birds:
            if bird.is_alive:  # Only draw alive birds
                self.screen.blit(self.images.bird, (bird.y, bird.x))

        if self.autonomous_mode:
            font = pygame.font.SysFont("Arial", 48, bold=True)
            alive_count = len([b for b in birds if b.is_alive])

            score_text = font.render(f"Score: {self.score} | Alive: {alive_count}/{len(birds)}",
                                     True, (255, 255, 255))

            text_rect = score_text.get_rect()
            text_rect.topleft = (10, 10)
            pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(20, 10))

            self.screen.blit(score_text, (20, 15))
        else:
            font = pygame.font.SysFont("Arial", 64, bold=True)
            score_text = font.render(f"{self.score}", True, (255, 255, 255))
            text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

            pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(20, 10))
            self.screen.blit(score_text, text_rect)
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
        print("MENU")
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
    def get_closest_pipes(self, poz_y: int) -> Union[tuple[Pipe, Pipe], tuple[None, Pipe]]:
        l = len(self.pipes)

        # No pipes yet
        if l == 0:
            return None, None

        # Only one pipe
        if l == 1:
            return None, self.pipes[0]

        # Bird is before the first pipe
        if poz_y < self.pipes[0].left_y:
            return None, self.pipes[0]

        # Check between pipes
        for i in range(l - 1):
            pipe_current = self.pipes[i]
            pipe_next = self.pipes[i + 1]

            # Bird is between pipe i and pipe i+1
            if pipe_current.left_y <= poz_y < pipe_next.left_y:
                # Check if bird has passed pipe_current (cleared it)
                if poz_y >= pipe_current.left_y + pipe_current.width:
                    # Bird is in the gap between pipes
                    return None, pipe_next
                else:
                    # Bird is still inside/approaching pipe_current
                    return pipe_current, pipe_next

        # Bird is past all pipes but the last one .This means bird is at or past the last pipe

        last_pipe = self.pipes[l - 1]
        if poz_y >= last_pipe.left_y:
            if poz_y >= last_pipe.left_y + last_pipe.width:
                # Bird passed the last pipe - return None for both (needs new pipe)
                return None, last_pipe
            else:
                # Bird is going through the last pipe
                return last_pipe, last_pipe

        return None, self.pipes[0]

    def reset_game_state(self, bird: FlappyBirdAgent):
        set_bird_def(bird)
        game_reset(self)
        pass
    def reset_game_state_birds(self, birds: list[FlappyBirdAgent]):
        for bird in birds:
            set_bird_def(bird)
        game_reset(self)
        pass

    def update_frame(self, bird: FlappyBirdAgent) -> None:

        clock = pygame.time.Clock()
        FPS = 60

        self.manual_input(bird)

        if self.status == GAME_RUNNING and not self.autonomous_mode:
            self.update_game_state([bird])

        if self.status == GAME_RUNNING and not self.autonomous_mode and not bird.is_alive:
            self.status = GAME_GAME_OVER

        if self.status in (GAME_RUNNING, GAME_MENU, GAME_GAME_OVER):
            self.render([bird])

        pygame.display.update()
        clock.tick(FPS)
    def increase_dificulty(self):
        if self.score >= 3:
            set_d_p(ORIGINAL_PIPE_DISTANCE - 20)
        if self.score >= 6:
            set_d_p(ORIGINAL_PIPE_DISTANCE - 20)
        if self.score >= 9:
            set_speed(ORIGINAL_PIPE_SPEED + 2)
            pass


def game_reset(game: FlappyBirdGame):
    game.pipes = []
    game.score = 0

    game.status = GAME_MENU
    game.curr_poz_left = 0
    game.distance = 0
    game.d_first_pipe = 0