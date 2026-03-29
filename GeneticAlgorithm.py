
import random

from FlappyBirdAgent import FlappyBirdAgent


class Species:


    def __init__(self, representative):
        self.representative = representative
        self.birds = [representative]
        self.average_fitness = 0

    def add_bird(self, bird):
        self.birds.append(bird)

    def calculate_average_fitness(self):

        if len(self.birds) == 0:
            self.average_fitness = 0
        else:
            total_fitness = sum(bird.score for bird in self.birds)
            self.average_fitness = total_fitness / len(self.birds)
        return self.average_fitness

    def sort_birds_by_fitness(self):

        self.birds.sort(key=lambda bird: bird.score, reverse=True)


class GeneticAlgorithm:
    def __init__(self, population_size=100):
        self.population_size = population_size
        self.current_generation = 0
        self.initial_population = self._spawn_initial_population(population_size)

    def _spawn_initial_population(self, N):

        birds = []
        for i in range(N):
            birds.append(FlappyBirdAgent())
        return birds

    def speciate(self, birds):

        species_list = []
        speciation_threshold = 0.8

        for bird in birds:
            added_to_species = False

            for species in species_list:

                weight_difference = sum(
                    abs(w_bird - w_rep)
                    for w_bird, w_rep in zip(bird.brain.weights, species.representative.brain.weights)
                )

                if weight_difference < speciation_threshold:
                    species.add_bird(bird)
                    added_to_species = True
                    break

            if not added_to_species:
                new_species = Species(bird)
                species_list.append(new_species)

        return species_list

    def calculate_fitness(self, species_list):

        for species in species_list:
            if len(species.birds) > 0:
                total_fitness = sum(bird.distance_traveled for bird in species.birds)
                species.average_fitness = total_fitness / len(species.birds)
            else:
                species.average_fitness = 0
            species.birds.sort(key=lambda bird: bird.distance_traveled, reverse=True)

        species_list.sort(key=lambda species: species.average_fitness, reverse=True)

        return species_list

    def create_next_generation(self, sorted_species):

        new_population = []
        total_average_fitness = sum(species.average_fitness for species in sorted_species)

        for species in sorted_species:
            if len(species.birds) == 0:
                continue

            champion = species.birds[0]
            champion_clone = FlappyBirdAgent(brain_weights=champion.brain.weights.copy())
            new_population.append(champion_clone)

            if total_average_fitness > 0:
                species_offspring_count = int(
                    (species.average_fitness / total_average_fitness) * self.population_size
                )
            else:
                species_offspring_count = max(2, self.population_size // len(sorted_species))

            species_offspring_count = max(1, species_offspring_count)

            for _ in range(species_offspring_count - 1):

                parent = random.choice(species.birds)
                child_weights = parent.brain.weights.copy()
                mutated_weights = self.mutate_weights(child_weights)

                child = FlappyBirdAgent(brain_weights=mutated_weights)
                new_population.append(child)

        while len(new_population) < self.population_size:
            new_population.append(FlappyBirdAgent())

        new_population = new_population[:self.population_size]

        self.current_generation += 1
        return new_population

    def mutate_weights(self, weights):

        mutation_rate = 0.15
        mutation_amount = 0.05

        new_weights = []
        for w in weights:
            if random.random() < mutation_rate:
                mutation = random.uniform(-mutation_amount, mutation_amount)
                w += mutation
                w = max(-1.0, min(1.0, w))
            new_weights.append(w)

        return new_weights