import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import random

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class QGA:
  def __init__(self, X, y, n_of_pop, n_of_gen):
    self.X =  X
    self.y = y
    self.n_of_pop = n_of_pop
    self.n_of_gen = n_of_gen

  def initialize(self):
    n_of_feat =  len(self.X.columns)
    angle = 0.25*np.pi
    alpha = np.sin(angle)
    beta = np.cos(angle)

    alphas = np.round(np.array([alpha for i in range(n_of_feat)]), 3)
    betas = np.round(np.array([beta for i in range(n_of_feat)]), 3)

    individual_alpha_beta = np.vstack([alphas, betas])
    Q = np.tile(individual_alpha_beta, (self.n_of_pop, 1, 1))

    Q_0 = Q.copy()

    return Q, alpha, beta
  def observe(self, Q):
    n_of_feat = len(self.X.columns)
    X_obs = np.zeros([self.n_of_pop, n_of_feat])
    population_alpha = Q[:, 0, :]
    for i in range(population_alpha.shape[0]):
        for j in range(population_alpha.shape[1]):
            rand = np.random.rand()
            if rand>population_alpha[i, j]**2:
                X_obs[i, j] = 1

    for individual in X_obs:
        if not np.any(individual):
            zero_indices = np.where(individual == 0)[0]
            random_index = np.random.choice(zero_indices)
            individual[random_index] = 1

    return X_obs
  def evaluate(self, X_obs):
    fitness = []
    pop_acc = dict()
    for i, individual in enumerate(X_obs):
        # create a ds
        selected_features = []
        for k, j in enumerate(individual):
            if j == 1:
                selected_features.append(self.X.columns[k])
            else:
                continue
        dataset = self.X[selected_features]
        #print(f"for population: {X_obs[i]} \n {dataset}")
        ss = StandardScaler()
        dataset_new = ss.fit_transform(dataset)
        X_train, X_test, y_train, y_test = train_test_split(dataset_new, self.y, test_size = 0.2, random_state = 42)
        nb = GaussianNB()
        nb.fit(X_train, y_train)
        y_pred = nb.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        fitness.append(np.round(acc, 3))
        pop_acc[tuple(X_obs[i])] = acc

    # max fitness
    f = max(pop_acc.values())
    fitness = np.array(fitness)

    return fitness, f, pop_acc
  def storage(self, pop_acc, alpha, beta):
    f = max(pop_acc.values())
    best_pops = [key for key, value in pop_acc.items() if value == f]
    chosen_pop = random.choice(best_pops)

    #print(chosen_pop, f)

    B = np.array([
            list(chosen_pop),
            [np.round(alpha, 3)] * len(chosen_pop),
            [np.round(beta, 3)] * len(chosen_pop)
        ])
    fitness_B = f
    return B, fitness_B

  def run_gen_0(self):
    print("################################### this is Generation 0... #############################################")
    Q, alpha, beta = self.initialize()
    X_obs = self.observe(Q)
    fitness, f, pop_acc = self.evaluate(X_obs)
    B, fitness_B = self.storage(pop_acc, alpha, beta)
    return Q, X_obs, fitness, f, B, fitness_B

  def crossover(self, crossover_X, X_fitness, B, B_fitness):
    # crossover:
    n_of_feat = len(self.X.columns)
    for i in range(n_of_feat):
      if crossover_X[2, i] == 0 and B[0, i] == 0:
        delta_theta = 0

      elif crossover_X[2, i] == 0 and B[0, i] == 1:
        if X_fitness > B_fitness:
          delta_theta = 0.05*np.pi
          if crossover_X[0, i]*crossover_X[1, i] > 0:
            delta_theta = -delta_theta
          elif crossover_X[0, i]*crossover_X[1, i] < 0:
            delta_theta = delta_theta
          elif crossover_X[0, i] == 0:
            delta_theta = delta_theta
          elif crossover_X[1, i] == 0:
            delta_theta = 0
        else:
          delta_theta = 0

      elif crossover_X[2, i] == 1 and B[0, i] == 0:
        if X_fitness > B_fitness:
          delta_theta = 0.025*np.pi
          if crossover_X[0, i]*crossover_X[1, i] > 0:
            delta_theta = delta_theta
          elif crossover_X[0, i]*crossover_X[1, i] < 0:
            delta_theta = -delta_theta
          elif crossover_X[0, i] == 0:
            delta_theta = 0
          elif crossover_X[1, i] == 0:
            delta_theta = delta_theta
        else:
          delta_theta = 0.01*np.pi
          if crossover_X[0, i]*crossover_X[1, i] > 0:
            delta_theta = -delta_theta
          elif crossover_X[0, i]*crossover_X[1, i] < 0:
            delta_theta = delta_theta
          elif crossover_X[0, i] == 0:
            delta_theta = delta_theta
          elif crossover_X[1, i] == 0:
            delta_theta = 0

      elif crossover_X[2, i] == 1 and B[0, i] == 1:
        if X_fitness > B_fitness:
          delta_theta = 0.025*np.pi
          if crossover_X[0, i]*crossover_X[1, i] > 0:
            delta_theta = delta_theta
          elif crossover_X[0, i]*crossover_X[1, i] < 0:
            delta_theta = -delta_theta
          elif crossover_X[0, i] == 0:
            delta_theta = 0
          elif crossover_X[1, i] == 0:
            delta_theta = delta_theta
        else:
          delta_theta = 0.005*np.pi
          if crossover_X[0, i]*crossover_X[1, i] > 0:
            delta_theta = delta_theta
          elif crossover_X[0, i]*crossover_X[1, i] < 0:
            delta_theta = -delta_theta
          elif crossover_X[0, i] == 0:
            delta_theta = 0
          elif crossover_X[1, i] == 0:
            delta_theta = delta_theta

        crossover_X[0, i] = np.round(np.cos(delta_theta)*crossover_X[0, i] - np.sin(delta_theta)*crossover_X[1, i], 3)
        crossover_X[1, i] = np.round(np.sin(delta_theta)*crossover_X[0, i] + np.cos(delta_theta)*crossover_X[1, i], 3)

    return np.array(crossover_X)

  def run_qga(self, Q):
    g = 1
    n_of_gen = 20
    n_of_feat = len(self.X.columns)
    Qnewnew = np.zeros((self.n_of_pop, 3, n_of_feat))
    best_individuals_per_gen = []
    fitness_per_gen = []

    while g <= n_of_gen:
        print(f"######################## #################### ##################### ############# Generation No: {g}")

        if g == 1:
            initialize = Q
        elif g > 1:
            initialize = Q
        # observe
        X_obs = self.observe(initialize)
        print(F"Observed Values: \n {X_obs}")
        # evaluate
        fitness, f, pop_acc = self.evaluate(X_obs)
        print(f"Fitness for each individual: \n {fitness} \n best fitness(chosen randomly is more than one have the same max fitness...) \n {f}")

        min_features = float('inf')
        best_fitness = 0
        best_individual = None

        # Update the best individual logic
        for i in range(len(fitness)):
            num_features = sum(X_obs[i])
            if fitness[i] > best_fitness or (fitness[i] == best_fitness and num_features < min_features):
                best_fitness = fitness[i]
                best_individual = X_obs[i]
                min_features = num_features
            elif fitness[i] == best_fitness and num_features == min_features:
                if random.choice([True, False]):
                    best_individual = X_obs[i]

        best_individuals_per_gen.append(best_individual)
        fitness_per_gen.append(best_fitness)

        print(f"for generation: {g}, best individual is {best_individual} with fitness: {best_fitness}")

        # Update the best individual
        best_idx = np.argmax(fitness)
        best_individual = X_obs[best_idx]
        best_alphas = initialize[best_idx, 0, :]
        best_betas = initialize[best_idx, 1, :]
        B = np.array([best_individual, best_alphas, best_betas])
        fitness_B = f
        # crossover
        for i in range(self.n_of_pop):
            alphas = initialize[i, 0, :]
            betas = initialize[i, 1, :]
            crossover_X = np.array([
                np.round(alphas, 3),
                np.round(betas, 3),
                list(X_obs[i])
            ])
            X_fitness = fitness[i]
            print(f"Xij: {crossover_X} \n fitness: {X_fitness}")
            Qnew = self.crossover(crossover_X, X_fitness, B, fitness_B)
            print(f"Updated Xij after crossover: \n {Qnew}")
            Qnewnew[i] = Qnew
        Q = Qnewnew.copy()
        print(f"End of Generation {g}")
        g = g + 1
        print()

    # Plot generation vs fitness
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, n_of_gen + 1), fitness_per_gen, marker='o', color='b', label='Best Fitness')
    plt.title("Generation vs Best Fitness", fontsize=14)
    plt.xlabel("Generation", fontsize=12)
    plt.ylabel("Fitness", fontsize=12)
    plt.xticks(range(1, n_of_gen + 1))
    plt.legend()
    plt.grid()
    plt.show()

    # Find the best individual among all generations
    final_best_fitness = max(fitness_per_gen)
    candidates = [
        (ind, sum(ind), fit)
        for ind, fit in zip(best_individuals_per_gen, fitness_per_gen)
        if fit == final_best_fitness
    ]
    final_best_individual, _, _ = min(candidates, key=lambda x: (x[1], random.random()))

    # Output final best individual and its fitness
    print("Final Best Individual:", final_best_individual)
    print("Final Best Fitness:", final_best_fitness)
    print("Minimum Features Used:", sum(final_best_individual))

    return final_best_individual

  def build_new_dataset(self, final_best_individual):
    selected_features = []
    for k, j in enumerate(final_best_individual):
        if j == 1:
            selected_features.append(self.X.columns[k])
        else:
            continue
    new_dataset = self.X[selected_features]
    return new_dataset