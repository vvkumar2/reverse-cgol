import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from sympy.logic import POSform

def life_step(X):
    nbrs_count = convolve2d(X, np.ones((3, 3)), mode='same', boundary='wrap') - X
    return (nbrs_count == 3) | (X & (nbrs_count == 2))

def templatize(cnf):
    return (
        str(cnf)
        .replace(' & ', ' 0\n')
        .replace(' | ', ' ')
        .replace('(', '')
        .replace(')', '')
        .replace('~', '-')
        + ' 0\n'
    )

def replace(template, a, b, c, d, e, f, g, h, i, x=None):
    return (
        template
        .replace('a', str(a))
        .replace('b', str(b))
        .replace('c', str(c))
        .replace('d', str(d))
        .replace('e', str(e))
        .replace('f', str(f))
        .replace('g', str(g))
        .replace('h', str(h))
        .replace('i', str(i))
        .replace('x', str(x))
    )

def v(x, y, W, H):
    return 1 + (x % W) + (y % H) * W

def ensure_non_empty_grid(W, H):
    clause = []
    for x in range(W):
        for y in range(H):
            clause.append(v(x, y, W, H))  # Adding each cell variable to the clause
    return ' '.join(str(cell) for cell in clause) + ' 0\n'  # SAT solvers typically require clauses to be terminated with a '0'


def create_templates():
    live = []
    dead = []
    for a in (0,1):
        for b in (0,1):
            for c in (0,1):
                for d in (0,1):
                    for e in (0,1):
                        for f in (0,1):
                            for g in (0,1):
                                for h in (0,1):
                                    for i in (0,1):
                                        crown = (a+b+c+d+ f+g+h+i)
                                        var = [a, b, c, d, e, f, g, h, i]
                                        if crown == 3 or (e == 1 and crown == 2):
                                            live.append(var)
                                        else:
                                            dead.append(var)

    live = POSform(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'], live)
    dead = POSform(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'], dead)

    template_live = templatize(live)
    template_dead = templatize(dead)

    return template_live, template_dead


def get_clauses(puzzle, delta, W, H, second_neighbors=False):
    template_live, template_dead = create_templates()
    clauses = ''
    
    # Apply initial state rules
    for x in range(W):
        for y in range(H):
            # Existing condition: determine live or dead templates based on the puzzle
            clauses += replace(template_live if puzzle[x, y] else template_dead,
                               v(x-1, y-1, W, H), v(x, y-1, W, H), v(x+1, y-1, W, H),
                               v(x-1, y, W, H), v(x, y, W, H), v(x+1, y, W, H),
                               v(x-1, y+1, W, H), v(x, y+1, W, H), v(x+1, y+1, W, H))

    for x in range(W):
        for y in range(H):
            if puzzle[x, y] == 0:  # The cell is currently dead
                # Initialize flag to check if all relevant neighbors are also dead
                all_neighbors_dead = True
                max_distance = 2 if second_neighbors else 1
                for dx in range(-max_distance, max_distance + 1):
                    for dy in range(-max_distance, max_distance + 1):
                        if dx != 0 or dy != 0:  # Avoid the cell itself
                            nx, ny = x + dx, y + dy
                            # Check bounds
                            if nx >= 0 and nx < W and ny >= 0 and ny < H:
                                if puzzle[nx, ny] == 1:
                                    all_neighbors_dead = False
                                    break
                    if not all_neighbors_dead:
                        break

                if all_neighbors_dead:
                    # If the cell and all neighbors (and second neighbors, if applicable) are dead,
                    # ensure it was dead in the previous state
                    clauses += f"-{v(x, y, W, H)} 0\n"  # Using DIMACS format for SAT solver

    # Ensure the grid is not completely empty
    clauses += ensure_non_empty_grid(W, H)
    return clauses

def life_step(X):
    """Compute one generation in the Game of Life."""
    neighbor_kernel = np.array([[1, 1, 1],
                                [1, 0, 1],
                                [1, 1, 1]])
    neighbor_count = convolve2d(X, neighbor_kernel, mode='same', boundary='wrap')
    return (neighbor_count == 3) | ((X == 1) & (neighbor_count == 2))

def plot_game_of_life(initial_state, num_transitions=10):
    """Plot the Game of Life states in a grid layout."""
    state = initial_state.copy()
    rows = (num_transitions + 4) // 5  # Calculate how many rows are needed
    fig, axes = plt.subplots(nrows=rows, ncols=5, figsize=(15, 3 * rows))
    if rows == 1:
        axes = [axes]  # Ensure axes is iterable in the single row case

    # If less than 5 columns are needed in the last row, turn off the unused axes
    for i in range(num_transitions, rows * 5):
        fig.delaxes(axes[i // 5][i % 5])

    for i in range(num_transitions):
        ax = axes[i // 5][i % 5]  # Determine the correct subplot
        ax.imshow(state, cmap='Greys', interpolation='nearest')
        ax.set_title(f"Generation {i + 1}")
        ax.grid(False)
        ax.axis('off')  # Turn off axis numbering
        state = life_step(state)  # Update the state

    plt.savefig('game_of_life.png', format='png', dpi=300)
    plt.tight_layout()
    plt.show()