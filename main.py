# ====================================================================
# 5. Main Execution in Jupyter Cells
# ====================================================================
import pygame
import time

from django.contrib.admin import display

from FlappyBirdGame import FlappyBirdGame, game_reset, GAME_CLOSE, GAME_RUNNING, GAME_MENU, GAME_GAME_OVER
from GeneticAlgorithm import GeneticAlgorithm
from FlappyBirdAgent import FlappyBirdAgent


# Make sure all necessary constants are imported or defined (e.g., in GAME_CONSTANTS.py)
# Assuming a constant like 20000 is a reasonable target distance.

def run_autonomous_mode(game: FlappyBirdGame, ga: GeneticAlgorithm, birds, max_generations=100):
    clock = pygame.time.Clock()
    FPS = 60
    DISTANCE_TARGET = 20000
    display_frame = 5
    frame = 0

    for generation in range(ga.current_generation, max_generations):
        print(f"--- Generation {generation} ---")

        alive_birds = list(birds)
        frame_count = 0

        # Setup game for the autonomous run
        game.status = GAME_RUNNING
        game.pipes = []
        game.update_pipes()  # Ensure the first pipe exists

        # Game loop for the current generation
        while alive_birds:
            # 1. Handle Pygame events (e.g., quitting)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                return

            # 2. Bird Decisions (Perceptron feed-forward)
            # Find pipes relative to EACH bird's position (Fixes AttributeError)
            for bird in alive_birds:
                next_pipe, second_pipe = game.get_closest_pipes(bird.y)
                current_pipes = (next_pipe, second_pipe)

                sensors = bird.get_sensors(current_pipes)
                bird.make_decision(sensors)

                # 3. Update Game State
            frame += 1
            game.update_game_state(alive_birds)
            if frame % display_frame == 0:
                # 4. Remove dead birds and Render
                alive_birds = [bird for bird in alive_birds if bird.is_alive]
                game.render(alive_birds)
                # 5. Update Display and Clock
                pygame.display.update()
                clock.tick(FPS)

            frame_count += 1

            # Timeout (optional, if a generation takes too long)
            if frame_count > 5000 or game.score >= 30:
                print("Generation timeout - ending")
                alive_birds = []

        # --- NATURAL SELECTION & NEXT GENERATION ---
        best_score = max(bird.score for bird in birds)
        best_distance = max(bird.distance_traveled for bird in birds)
        avg_distance = sum(bird.distance_traveled for bird in birds) / len(birds)

        print(f"Generation {generation} ended:")
        print(f"  Best score: {best_score}")
        print(f"  Best distance: {best_distance} pixels")
        print(f"  Avg distance: {avg_distance:.1f} pixels")

        # 1. Speciation (FIX: This line defines species_list)
        species_list = ga.speciate(birds)

        # 2. Fitness Score & Sorting
        ga.calculate_fitness(species_list)

        # 3. Generate Next Generation
        birds = ga.create_next_generation(species_list)

        # Reset bird states (but keeps weights) for the next run
        game.reset_game_state_birds(birds)

        # Optional: Break condition for goal achievement
        if best_distance > DISTANCE_TARGET:
            print(f"Target distance of {DISTANCE_TARGET} reached! Best distance: {best_distance}")
            break

    print("Training complete!")
    pygame.quit()

if __name__ == "__main__":
    pygame.init()

    # 1. Setup
    game = FlappyBirdGame(autonomous_mode=False)
    manual_bird = FlappyBirdAgent()  # The single bird for the manual mode

    # 2. Master Game Loop
    while game.status != GAME_CLOSE:

        # --- A. Autonomous Mode Logic ---
        if game.autonomous_mode and game.status == GAME_RUNNING:
            # Initialize GA and birds
            ga = GeneticAlgorithm(population_size=100)
            initial_birds = ga.initial_population

            # Run the autonomous simulation
            run_autonomous_mode(game, ga, initial_birds)

            # The autonomous function calls pygame.quit() and returns, breaking the main loop
            break

            # --- B. Menu / Manual Game Logic (One Frame Update) ---
        game.update_frame(manual_bird)

        # 3. Cleanup (If the main loop exited without pygame.quit() in autonomous mode)
    if game.status == GAME_CLOSE:
        pygame.quit()