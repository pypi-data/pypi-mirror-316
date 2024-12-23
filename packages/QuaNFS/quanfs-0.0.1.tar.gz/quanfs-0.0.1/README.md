# QuantumBasedGeneticAlgorithm
Implements Quantum Based Genetic Algorithm for Feature Selection

How to use:

Step 1: Preprocess the dataset (Encoding, Imputing, Removing null values etc...)

Step 2: Split the dataset into X, y where both X and y are PandasDataFrame

Step 3: run the QGA_Algorithm 

Step 4: initialize the algorithm

              qga = QGA(X, y, n_of_pop, n_of_gen) # where X and y are dependent and independent variables. And n_of_pop and n_of_gen is numnber of population and number of generations
              
Step 5: Run generation 0

              Q = qga.run_gen_0()
              
Step 6: Run QGA

              best_individuals = qga.run_qga(Q[0]) # Q[0] because Q is a numpy array in a tuple... we only need numpy array
              
Step 7: Build a new dataset with reduced features

              qga.build_new_dataset(best_individuals)

