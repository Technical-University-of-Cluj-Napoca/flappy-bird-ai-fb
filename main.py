# ====================================================================
# 5. Main Execution in Jupyter Cells
# ====================================================================
import pygame
import time

from FlappyBirdGame import FlappyBirdGame
from GeneticAlgorithm import GeneticAlgorithm

# Cell 1: Setup and Initialization
# Initialize the game and the genetic algorithm
pygame.init()
MyGame = FlappyBirdGame(autonomous_mode=True)
MyGA = GeneticAlgorithm(population_size=100)
MyBirds = MyGA.initial_population


# Cell 2: The Main Simulation Loop
def run_autonomous_mode(game: FlappyBirdGame, ga: GeneticAlgorithm, birds, max_generations=100):
    for generation in range(ga.current_generation, max_generations):
        print(f"--- Generation {generation} ---")

        # Keep track of only the alive birds
        alive_birds = list(birds)

        # Game loop for the current generation
        while alive_birds:
            # 1. Handle Pygame events (e.g., quitting)
            # 2. For each alive bird, make a decision
            for bird in alive_birds:
                bird.make_decision(game)

            # 3. Update game state and physics for all birds
            for bird in alive_birds:
                game.update_physics(bird)
                if game.check_collision(bird):
                    bird.is_alive = False

            # 4. Remove dead birds and update the list
            alive_birds = [bird for bird in alive_birds if bird.is_alive]

            # 5. Render the game (optional, but helpful for visualization)
            game.update_game_state(birds)
            game.render(alive_birds)

            # ... (Add a small delay/clock tick)

        # Natural Selection Process [cite: 179]
        # All birds go extinct [cite: 180] -> Time to evolve!

        # 1. Speciation
        species_list = ga.speciate(birds)

        # 2. Fitness Score & Sorting
        ga.calculate_fitness(species_list)  # Sorts species and birds within species [cite: 191]

        # 3. Generate Next Generation
        birds = ga.create_next_generation(species_list)

        # Reset game for the new generation
        game.reset_game_state_birds(birds)

        # Break condition if a very high score is reached

def run_manual_mode():
    game = FlappyBirdGame()
    game.game_loop()
    time.sleep(1)

run_manual_mode()

#run_autonomous_mode(MyGame, MyGA, MyBirds)