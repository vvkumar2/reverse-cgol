import os
import subprocess
import time
import numpy as np

from utils import *
from constants import *

def solve(puzzle=None, delta=None, start_time=time.time(), second_neighbors=False):
    budget = TIME_BUDGET - (time.time() - start_time)
    budget = min(budget, MAX_BUDGET)

    if budget <= 0:
        print("Time Budget Exceeded.")
        return None

    if not puzzle.any() or not delta:
      print("Missing Input.")
      return None

    W, H = puzzle.shape

    # get SAT clauses
    clauses = get_clauses(puzzle, delta, W, H, second_neighbors=second_neighbors)
    nb = clauses.count('\n')

    # write .cnf file
    filename = 'puzzle.cnf'
    with open(filename, 'w') as f:
        f.write(f'p cnf {W*H*delta} {nb}\n')
        f.write(clauses)

    preprocessed_filename = 'preprocessed.cnf'
    subprocess.run(['./SBVA/sbva', '-i', filename, '-o', preprocessed_filename])


    # invoke kissat
    cmd = ["./kissat/build/kissat", "-q", preprocessed_filename]
    cmd = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    solution = cmd.communicate()[0]
    solution = solution.decode('utf8')
    os.remove(filename)
    os.remove(preprocessed_filename)

    if solution == '' or 'UNSAT' in solution:
        print("UNSAT")
        return None

    print("Solved")

    # parse solution
    parsed = []
    for x in solution.split():
        try:
            parsed.append(int(x))
        except:
            pass
    parsed = set(parsed)

    # format solution
    solution = np.zeros((W, H), dtype=int)
    for x in range(W):
        for y in range(H):
            z = v(x, y, W, H)
            if z in parsed:
                solution[x, y] = 1

    return solution


def main():
    initial_state = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])


    prev_state = initial_state  # Assuming initial_state is defined and is a NumPy array
    state = prev_state
    start_time = time.time()
    max_iterations = 100
    iteration_count = 0

    while state is not None and np.any(state) and iteration_count < max_iterations:
        prev_state = state
        state = solve(puzzle=prev_state, 
                      delta=1, 
                      start_time=start_time)

        # Check if state is not None and is empty, then try with second_neighbors
        if state is None or not np.any(state):
            state = solve(puzzle=prev_state, 
                          delta=1,
                          start_time=start_time, 
                          second_neighbors=True)

        iteration_count += 1

    print(f"\n{iteration_count} previous states found.")
    plot_game_of_life(prev_state, num_transitions=iteration_count)


if __name__ == "__main__":
    main()