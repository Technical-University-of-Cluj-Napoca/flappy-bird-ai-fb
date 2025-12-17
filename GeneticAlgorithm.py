# ====================================================================
# 4. Evolutionary Algorithm (GeneticAlgorithm)
# Manages the natural selection process[cite: 179].
# ====================================================================
import random
import copy

from FlappyBirdAgent import FlappyBirdAgent


class Species:
    """Helper class to represent a species of birds."""

    def __init__(self, representative):
        self.representative = representative  # The bird that represents this species
        self.birds = [representative]  # List of birds in this species
        self.average_fitness = 0  # Average fitness of all birds in this species

    def add_bird(self, bird):
        self.birds.append(bird)

    def calculate_average_fitness(self):
        """Calculate the average fitness of all birds in this species."""
        if len(self.birds) == 0:
            self.average_fitness = 0
        else:
            total_fitness = sum(bird.score for bird in self.birds)
            self.average_fitness = total_fitness / len(self.birds)
        return self.average_fitness

    def sort_birds_by_fitness(self):
        """Sort birds in descending order by their individual fitness."""
        self.birds.sort(key=lambda bird: bird.score, reverse=True)


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
        return birds

    def speciate(self, birds):
        """
        Group birds into species based on the similarities of their corresponding weights[cite: 181].
        """
        species_list = []
        speciation_threshold = 0.8  # Reduced from 1.5 for more species diversity

        # For each bird, compare its brain weights to the representatives of existing species
        for bird in birds:
            added_to_species = False

            for species in species_list:
                # Calculate total weight difference between the bird and the species representative
                # Difference = sum(|w_A,i - w_B,i|) [cite: 183]
                weight_difference = sum(
                    abs(w_bird - w_rep)
                    for w_bird, w_rep in zip(bird.brain.weights, species.representative.brain.weights)
                )

                # If difference < threshold, add bird to species [cite: 185, 186]
                if weight_difference < speciation_threshold:
                    species.add_bird(bird)
                    added_to_species = True
                    break

            # If no species match, create a new species with this bird as the representative [cite: 185]
            if not added_to_species:
                new_species = Species(bird)
                species_list.append(new_species)

        return species_list

    def calculate_fitness(self, species_list):
        """
        Calculates and sorts fitness scores.
        Uses distance_traveled as fitness metric for better granularity.
        """
        # 1. Calculate Player fitness score (individual bird score) [cite: 188]
        # Use distance_traveled for more granular fitness (not just discrete scores)

        # 2. Calculate Species fitness score (average fitness of all birds in that species) [cite: 188]
        # This prevents a species with one genius bird and ten foolish ones from being unfairly rewarded[cite: 189].
        for species in species_list:
            # Calculate average using distance_traveled for better evolution
            if len(species.birds) > 0:
                total_fitness = sum(bird.distance_traveled for bird in species.birds)
                species.average_fitness = total_fitness / len(species.birds)
            else:
                species.average_fitness = 0

            # Sort birds within each species by distance traveled
            species.birds.sort(key=lambda bird: bird.distance_traveled, reverse=True)

        # 3. Sort Everything (descending order of excellence) [cite: 191]
        # - Species are sorted by species fitness
        species_list.sort(key=lambda species: species.average_fitness, reverse=True)

        return species_list

    def create_next_generation(self, sorted_species):
        """
        Generate children for the next generation[cite: 193].
        """
        new_population = []

        # Calculate how many offspring each species should produce
        # based on their fitness (better species get more offspring)
        total_average_fitness = sum(species.average_fitness for species in sorted_species)

        for species in sorted_species:
            # Skip empty species
            if len(species.birds) == 0:
                continue

            # Keep the champion from each species by cloning (without changing anything) [cite: 194]
            champion = species.birds[0]
            champion_clone = FlappyBirdAgent(brain_weights=champion.brain.weights.copy())
            new_population.append(champion_clone)

            # Calculate how many offspring this species should produce
            if total_average_fitness > 0:
                species_offspring_count = int(
                    (species.average_fitness / total_average_fitness) * self.population_size
                )
            else:
                # If all birds scored 0, distribute evenly
                species_offspring_count = max(2, self.population_size // len(sorted_species))

            # Make sure at least the champion is kept
            species_offspring_count = max(1, species_offspring_count)

            # Fill remaining places with mutations of randomly selected birds [cite: 195]
            for _ in range(species_offspring_count - 1):  # -1 because we already added the champion
                # Select a parent (can be any bird in the species, including champion)
                parent = random.choice(species.birds)

                # Create a child by cloning the parent's weights
                child_weights = parent.brain.weights.copy()

                # Apply smaller random mutations on its weights [cite: 195]
                mutated_weights = self.mutate_weights(child_weights)

                # Create the child bird with mutated weights
                child = FlappyBirdAgent(brain_weights=mutated_weights)
                new_population.append(child)

        # If the population is too small, fill up to population_size with random individuals
        while len(new_population) < self.population_size:
            new_population.append(FlappyBirdAgent())

        # If the population is too large, trim it down
        new_population = new_population[:self.population_size]

        self.current_generation += 1
        return new_population

    def mutate_weights(self, weights):
        """
        Applies small random mutations to the weights for innovation[cite: 196].
        """
        mutation_rate = 0.15  # 15% chance each weight will mutate
        mutation_amount = 0.05  # Smaller mutation range for stability

        new_weights = []
        for w in weights:
            if random.random() < mutation_rate:
                # Add a random mutation
                mutation = random.uniform(-mutation_amount, mutation_amount)
                w += mutation
                # Clamp weights to reasonable range (smaller range due to normalized inputs)
                w = max(-1.0, min(1.0, w))
            new_weights.append(w)

        return new_weights