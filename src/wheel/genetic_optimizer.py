import numpy as np
import random
from itertools import combinations
from typing import List, Tuple
from src.config import Config

class GeneticWheelOptimizer:
    def __init__(self, number_pool: List[int], line_length: int = 6, 
                 target_coverage: float = 0.95, 
                 population_size: int = Config.GA_POPULATION_SIZE,
                 generations: int = Config.GA_GENERATIONS):
        self.number_pool = number_pool
        self.line_length = line_length
        self.target_coverage = target_coverage
        self.population_size = population_size
        self.generations = generations
        self.all_combinations = list(combinations(number_pool, line_length))
        self.best_solution = None
        self.best_fitness = 0
        
    def initialize_population(self, min_tickets: int = 10, max_tickets: int = 50) -> List[List[Tuple]]:
        population = []
        for _ in range(self.population_size):
            num_tickets = random.randint(min_tickets, max_tickets)
            wheel = random.sample(self.all_combinations, min(num_tickets, len(self.all_combinations)))
            population.append(wheel)
        return population
    
    def calculate_pair_coverage(self, wheel: List[Tuple]) -> float:
        all_pairs = set(combinations(self.number_pool, 2))
        covered_pairs = set()
        for ticket in wheel:
            for pair in combinations(ticket, 2):
                covered_pairs.add(pair)
        return len(covered_pairs) / len(all_pairs) if all_pairs else 0
    
    def fitness(self, wheel: List[Tuple]) -> float:
        coverage = self.calculate_pair_coverage(wheel)
        ticket_penalty = len(wheel) / max(1, self.target_coverage * 100)
        return max(0, coverage - ticket_penalty * 0.01)
    
    def select_parents(self, population, fitness_scores):
        tournament_size = 3
        def tournament():
            contestants = random.sample(list(zip(population, fitness_scores)), tournament_size)
            return max(contestants, key=lambda x: x[1])[0]
        return tournament(), tournament()
    
    def crossover(self, parent1, parent2):
        combined = parent1 + parent2
        unique = []
        seen = set()
        for t in combined:
            if t not in seen:
                seen.add(t)
                unique.append(t)
        max_tickets = max(len(parent1), len(parent2))
        if len(unique) > max_tickets:
            random.shuffle(unique)
            unique = unique[:max_tickets]
        return unique
    
    def mutate(self, wheel, mutation_rate=Config.GA_MUTATION_RATE):
        if random.random() > mutation_rate:
            return wheel
        mutated = wheel.copy()
        if random.random() < 0.5 and len(mutated) < len(self.all_combinations)*0.3:
            new_ticket = random.choice(self.all_combinations)
            if new_ticket not in mutated:
                mutated.append(new_ticket)
        elif len(mutated) > 1:
            mutated.pop(random.randint(0, len(mutated)-1))
        return mutated
    
    def evolve(self):
        population = self.initialize_population()
        for gen in range(self.generations):
            fitness_scores = [self.fitness(w) for w in population]
            gen_best_idx = np.argmax(fitness_scores)
            if fitness_scores[gen_best_idx] > self.best_fitness:
                self.best_fitness = fitness_scores[gen_best_idx]
                self.best_solution = population[gen_best_idx].copy()
            next_pop = [self.best_solution.copy()]
            while len(next_pop) < self.population_size:
                p1, p2 = self.select_parents(population, fitness_scores)
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                next_pop.append(child)
            population = next_pop
            if gen % 10 == 0:
                coverage = self.calculate_pair_coverage(self.best_solution)
                print(f"Gen {gen}: fitness={self.best_fitness:.4f}, coverage={coverage:.2%}, tickets={len(self.best_solution)}")
        return self.best_solution
    
    def get_optimal_wheel(self):
        if self.best_solution is None:
            self.evolve()
        return self.best_solution
