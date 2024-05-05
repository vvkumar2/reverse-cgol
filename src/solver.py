import os
import subprocess
import time
import numpy as np
import argparse
import logging
from utils import *
from constants import *
from setup_project import setup_project

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def solve(puzzle, start_time, second_neighbors=False, keep_cnf=False, file_location=''):
    """Attempt to solve the Game of Life puzzle using SAT solver."""
    budget = TIME_BUDGET - (time.time() - start_time)
    budget = min(budget, MAX_BUDGET)
    if budget <= 0:
        logger.error("Time Budget Exceeded.")
        return None

    W, H = np.shape(puzzle)

    clauses = get_clauses(puzzle, W, H, second_neighbors=second_neighbors)
    nb = clauses.count('\n')
    filename = f'{file_location}puzzle.cnf'

    with open(filename, 'w') as f:
        f.write(f'p cnf {W*H} {nb}\n')
        f.write(clauses)

    preprocessed_filename = f'{file_location}preprocessed_puzzle.cnf'
    subprocess.run(['SBVA/sbva', '-i', filename, '-o', preprocessed_filename])
    solution = subprocess.run(["./kissat/build/kissat", "-q", preprocessed_filename], stdout=subprocess.PIPE).stdout.decode('utf8')

    if not keep_cnf:
        os.remove(filename)
        os.remove(preprocessed_filename)

    if solution == '' or 'UNSAT' in solution:
        logger.info("Puzzle is UNSAT")
        return None

    logger.info("Puzzle Iteration Solved")
    return parse_solution(solution, W, H)


def parse_solution(solution, W, H):
    """Parse the SAT solver output to format it into a solution grid."""
    parsed = {int(x) for x in solution.split() if x.isdigit()}
    solution_grid = np.zeros((W, H), dtype=int)
    for x in range(W):
        for y in range(H):
            z = v(x, y, W, H)
            if z in parsed:
                solution_grid[x, y] = 1
    return solution_grid


def solve_loop(initial_state, keep_cnf, file_location=''):
    state, prev_state = initial_state, None
    start_time, max_iterations = time.time(), 100

    for iteration_count in range(max_iterations):
        prev_state = state
        state = solve(puzzle=prev_state, 
                      start_time=start_time, 
                      keep_cnf=keep_cnf,
                      file_location=file_location)
        
        if state is None or not np.any(state):
            state = solve(puzzle=prev_state, 
                          start_time=start_time, 
                          second_neighbors=True, 
                          keep_cnf=keep_cnf,
                          file_location=file_location)
            if state is None:
                break
    
    logger.info(f"Found {iteration_count} previous states.")
    
    return prev_state, iteration_count
    

def main():
    parser = argparse.ArgumentParser(description='Solve the Game of Life puzzle using SAT solvers.')
    parser.add_argument('--setup', action='store_true', help='Trigger project setup.')
    parser.add_argument('--puzzle', type=str, help='Filename of the puzzle file (optional).')
    parser.add_argument('--word', type=str, help='Word to convert into a puzzle (optional).')
    parser.add_argument('--keep_cnf', action='store_true', help='Keep the CNF file after solving.')

    args = parser.parse_args()

    if args.setup:
        logger.info("Setting up the project.")
        setup_project()

    if not os.path.exists('SBVA') or not os.path.exists('kissat'):
        logger.error("SBVA and/or kissat not found. Run with --setup flag.")
        return

    if args.puzzle:
        initial_state = load_puzzle(args.puzzle)
        if initial_state is None:
            logger.error("Failed to load the initial puzzle state from file.")
            return
    elif args.word:
        word_length = len(args.word)
        if word_length > 5:
            padding = 8
        elif word_length > 8:
            padding = 10
        initial_state = word_to_grid(args.word, padding=padding)
        logger.info(f"Generated grid from word '{args.word.upper()}'.")
    else:
        logger.error("No puzzle file or word provided. Please specify one.")
        return

    prev_state, iteration_count = solve_loop(initial_state, args.keep_cnf)

    if prev_state is not None:
        save_state(prev_state, iteration_count)
        plot_game_of_life(prev_state, num_transitions=iteration_count+1)


if __name__ == "__main__":
    main()
