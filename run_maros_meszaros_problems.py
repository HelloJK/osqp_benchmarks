'''
Run Maros-Meszaros problems for the OSQP paper

This code tests the solvers:
    - OSQP
    - GUROBI
    - MOSEK

'''
from maros_meszaros_problems.maros_meszaros_problem import MarosMeszarosRunner
import solvers.solvers as s
from utils.general import plot_performance_profiles
from utils.benchmark import \
    compute_performance_profiles, \
    compute_shifted_geometric_means, \
    compute_failure_rates, \
    compute_polish_statistics
import os
import argparse


parser = argparse.ArgumentParser(description='Maros Meszaros Runner')
parser.add_argument('--high_accuracy', help='Test with high accuracy', default=False)
parser.add_argument('--verbose', help='Verbose solvers', default=False)
parser.add_argument('--parallel', help='Parallel solution', default=True)
args = parser.parse_args()
high_accuracy = args.high_accuracy
verbose = args.verbose
parallel = args.parallel

# Add high accuracy solvers when accurazy
if high_accuracy:
    solvers = [s.OSQP_high, s.OSQP_polish_high, s.GUROBI, s.MOSEK]
    OUTPUT_FOLDER = 'maros_meszaros_problems'
    for key in s.settings:
        s.settings[key]['high_accuracy'] = True

else:
    solvers = [s.OSQP, s.OSQP_polish, s.GUROBI, s.MOSEK]
    OUTPUT_FOLDER = 'maros_meszaros_problems_high_accuracy'

# Shut up solvers
if verbose:
    for key in s.settings:
        s.settings[key]['verbose'] = True

# Run all examples
maros_meszaros_runner = MarosMeszarosRunner(solvers,
                                            s.settings,
                                            OUTPUT_FOLDER)

# DEBUG only: Choose only 2 problems
maros_meszaros_runner.problems = ["STADAT1", "BOYD1"]

maros_meszaros_runner.solve(parallel=parallel, cores=12)
statistics_file = os.path.join(".", "results", OUTPUT_FOLDER,
                               "statistics.txt")
print("Saving statistics to %s" % statistics_file)

# Compute failure rates
compute_failure_rates(solvers, OUTPUT_FOLDER)

# Compute performance profiles
compute_performance_profiles(solvers, OUTPUT_FOLDER)

# Compute performance profiles
compute_shifted_geometric_means(solvers, OUTPUT_FOLDER)

# Compute polish statistics
compute_polish_statistics(OUTPUT_FOLDER)

# Plot performance profiles
plot_performance_profiles(OUTPUT_FOLDER,
                          ["OSQP", "GUROBI",  "MOSEK"])
