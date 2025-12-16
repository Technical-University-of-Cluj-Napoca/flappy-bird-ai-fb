# ====================================================================
# 4. Evolutionary Algorithm (GeneticAlgorithm)
# Manages the natural selection process[cite: 179].
# ====================================================================
import random

from FlappyBirdAgent import FlappyBirdAgent


class GeneticAlgorithm:
    def __init__(self, population_size=100):
        self.population_size = population_size
        self.current_generation = 0
        self.initial_population = self._spawn_initial_population(population_size)

    def _spawn_initial_population(self, N):
        """
        Start the training process by spawning an initial population of N birds
        that have the same brain, but with slightly different weights[cite: 179].
        """
        birds = []
        for i in range(N):
            birds.append(FlappyBirdAgent())
        # Create N FlappyBirdAgent objects
        # ...
        return birds

    def speciate(self, birds):
        """
        Group birds into species based on the similarities of their corresponding weights[cite: 181].
        """
        species_list = []
        speciation_threshold = 1.0  # Set a threshold value [cite: 184]

        # For each bird, compare its brain weights to the representatives of existing species
        for bird in birds:
            added_to_species = False
            for species in species_list:
                # Calculate total weight difference between the bird and the species representative
                # Difference = sum(|w_A,i - w_B,i|) [cite: 183]
                # If difference < threshold, add bird to species [cite: 185, 186]
                pass

            # If no species match, create a new species with this bird as the representative [cite: 185]
            if not added_to_species:
                # ...
                pass

        return species_list

    def calculate_fitness(self, species_list):
        """
        Calculates and sorts fitness scores.
        """
        # 1. Calculate Player fitness score (individual bird score) [cite: 188]
        # (This is already stored in the FlappyBirdAgent.score)

        # 2. Calculate Species fitness score (average fitness of all birds in that species) [cite: 188]
        # This prevents a species with one genius bird and ten foolish ones from being unfairly rewarded[cite: 189].

        # 3. Sort Everything (descending order of excellence) [cite: 191]
        # - Species are sorted by species fitness
        # - Players inside each species are sorted by individual fitness
        pass

    def create_next_generation(self, sorted_species):
        """
        Generate children for the next generation[cite: 193].
        """
        new_population = []

        for species in sorted_species:
            # Keep the champion from each species by cloning (without changing anything) [cite: 194]
            champion = species.birds[0]
            new_population.append(champion)

            # Fill remaining places with mutations of randomly selected birds [cite: 195]
            # Select a parent (not the champion)
            # Create a child by cloning the parent's weights
            # Apply smaller random mutations on its weights [cite: 195]
            # ...

        # If the population is too small, fill up to population_size with random individuals
        # ...

        self.current_generation += 1
        return new_population

    def mutate_weights(self, weights):
        """
        Applies small random mutations to the weights for innovation[cite: 196].
        """
        mutation_rate = 0.1  # Example rate
        mutation_amount = 0.5  # Example range
        new_weights = []
        for w in weights:
            if random.random() < mutation_rate:
                w += random.uniform(-mutation_amount, mutation_amount)
            new_weights.append(w)
        return new_weights