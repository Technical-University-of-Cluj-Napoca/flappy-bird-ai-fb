
import pygame

from FlappyBirdGame import FlappyBirdGame, GAME_CLOSE, GAME_RUNNING
from GeneticAlgorithm import GeneticAlgorithm
from FlappyBirdAgent import FlappyBirdAgent


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
        game.update_pipes()

        # Game loop for the current generation
        while alive_birds:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                return


            for bird in alive_birds:
                next_pipe, second_pipe = game.get_closest_pipes(bird.y)
                current_pipes = (next_pipe, second_pipe)

                sensors = bird.get_sensors(current_pipes)
                bird.make_decision(sensors)

            frame += 1
            game.update_game_state(alive_birds)
            if frame % display_frame == 0:

                alive_birds = [bird for bird in alive_birds if bird.is_alive]
                game.render(alive_birds)

                pygame.display.update()
                clock.tick(FPS)

            frame_count += 1

            if frame_count > 5000 or game.score >= 30:
                print("Generation timeout - ending")
                alive_birds = []

        #NATURAL SELECTION & NEXT GENERATION
        best_score = max(bird.score for bird in birds)
        best_distance = max(bird.distance_traveled for bird in birds)
        avg_distance = sum(bird.distance_traveled for bird in birds) / len(birds)

        print(f"Generation {generation} ended:")
        print(f"  Best score: {best_score}")
        print(f"  Best distance: {best_distance} pixels")
        print(f"  Avg distance: {avg_distance:.1f} pixels")

        species_list = ga.speciate(birds)
        ga.calculate_fitness(species_list)
        birds = ga.create_next_generation(species_list)
        game.reset_game_state_birds(birds)

        if best_distance > DISTANCE_TARGET:
         print(f"Target distance of {DISTANCE_TARGET} reached! Best distance: {best_distance}")
        break

    print("Training complete!")
    pygame.quit()

if __name__ == "__main__":
    pygame.init()

    game = FlappyBirdGame(autonomous_mode=False)
    manual_bird = FlappyBirdAgent()

    while game.status != GAME_CLOSE:

        if game.autonomous_mode and game.status == GAME_RUNNING:

            ga = GeneticAlgorithm(population_size=100)
            initial_birds = ga.initial_population

            run_autonomous_mode(game, ga, initial_birds)
            break

        game.update_frame(manual_bird)

    if game.status == GAME_CLOSE:
        pygame.quit()