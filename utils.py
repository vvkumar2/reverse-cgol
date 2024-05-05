import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from sympy.logic import POSform
from matplotlib.colors import LinearSegmentedColormap
import logging
from font import character_matrices

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def life_step(X):
    nbrs_count = convolve2d(X, np.ones((3, 3)), mode='same', boundary='wrap') - X
    return (nbrs_count == 3) | (X & (nbrs_count == 2))


def templatize(cnf):
    return str(cnf).replace(' & ', ' 0\n').replace(' | ', ' ').replace('(', '').replace(')', '').replace('~', '-') + ' 0\n'


def replace(template, a, b, c, d, e, f, g, h, i, x=None):
    return template.replace('a', str(a)).replace('b', str(b)).replace('c', str(c)).replace('d', str(d)).replace('e', str(e)).replace('f', str(f)).replace('g', str(g)).replace('h', str(h)).replace('i', str(i)).replace('x', str(x))


def v(x, y, W, H):
    """Return the variable number for the cell at position (x, y) with wrap-around."""
    return 1 + (x % W) + (y % H) * W


def ensure_non_empty_grid(W, H):
    clause = [v(x, y, W, H) for x in range(W) for y in range(H)]
    return ' '.join(str(cell) for cell in clause) + ' 0\n'


def create_templates():
    """These templates represent the rules of the Game of Life in a 3x3 grid with the center cell being the current cell."""
    live, dead = [], []
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                for d in (0, 1):
                    for e in (0, 1):
                        for f in (0, 1):
                            for g in (0, 1):
                                for h in (0, 1):
                                    for i in (0, 1):
                                        crown = (a+b+c+d+f+g+h+i)
                                        var = [a, b, c, d, e, f, g, h, i]
                                        if crown == 3 or (e == 1 and crown == 2):
                                            live.append(var)
                                        else:
                                            dead.append(var)

    live = POSform(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'], live)
    dead = POSform(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'], dead)

    return templatize(live), templatize(dead)


def get_clauses(puzzle, W, H, second_neighbors=False):
    """Generate the SAT clauses for the Game of Life puzzle."""
    template_live, template_dead = create_templates()
    clauses = ''
    
    for x in range(W):
        for y in range(H):
            clauses += replace(template_live if puzzle[x][y] else template_dead,
                               v(x-1, y-1, W, H), v(x, y-1, W, H), v(x+1, y-1, W, H),
                               v(x-1, y, W, H), v(x, y, W, H), v(x+1, y, W, H),
                               v(x-1, y+1, W, H), v(x, y+1, W, H), v(x+1, y+1, W, H))

            if puzzle[x][y] == 0:
                all_neighbors_dead = True
                max_distance = 2 if second_neighbors else 1
                for dx in range(-max_distance, max_distance + 1):
                    for dy in range(-max_distance, max_distance + 1):
                        if dx != 0 or dy != 0:
                            nx, ny = x + dx, y + dy
                            if nx >= 0 and nx < W and ny >= 0 and ny < H:
                                if puzzle[nx][ny] == 1:
                                    all_neighbors_dead = False
                                    break
                    if not all_neighbors_dead:
                        break
                if all_neighbors_dead:
                    clauses += f"-{v(x, y, W, H)} 0\n" 

    clauses += ensure_non_empty_grid(W, H)
    return clauses


def life_step(X):
    """Compute one generation in the Game of Life."""
    neighbor_kernel = np.array([[1, 1, 1],
                                [1, 0, 1],
                                [1, 1, 1]])
    neighbor_count = convolve2d(X, neighbor_kernel, mode='same', boundary='wrap')
    return (neighbor_count == 3) | ((X == 1) & (neighbor_count == 2))


def plot_game_of_life(initial_state, num_transitions, states_per_row=5):
    """Plot the Game of Life states in a grid layout."""
    colors = ["#0c1016", "#ffffff"]  # Dark grey for dead cells, white for live cells
    cmap = LinearSegmentedColormap.from_list("custom_binary", colors, N=2)

    state = initial_state.copy()
    rows = (num_transitions + 4) // states_per_row
    fig, axes = plt.subplots(nrows=rows, ncols=states_per_row, figsize=(15, 3 * rows))
    if rows == 1:
        axes = [axes]
    for i in range(num_transitions, rows * states_per_row):
        fig.delaxes(axes[i // states_per_row][i % states_per_row])
    for i in range(num_transitions):
        ax = axes[i // states_per_row][i % states_per_row]
        ax.imshow(state, cmap=cmap)
        ax.set_title(f"Generation {i + 1}", color='white')
        ax.grid(False)
        ax.axis('off')
        state = life_step(state)
    
    fig.patch.set_facecolor('#0c1016')
    ax.set_facecolor('#0c1016')

    plt.savefig('game_of_life.png', format='png', dpi=300)
    plt.tight_layout()
    return fig


def load_puzzle(filename):
    try:
        with open(filename, 'r') as file:
            puzzle, row_length = [], None
            for line_number, line in enumerate(file, start=1):
                row = line.strip().split(',')
                try:
                    row = [int(num) for num in row]
                except ValueError:
                    logger.error(f"Error: Non-integer value found in the file at line {line_number}.")
                    return None
                if row_length is None:
                    row_length = len(row)
                elif len(row) != row_length:
                    logger.error(f"Error: Inconsistent row length found in the file at line {line_number}.")
                    return None
                puzzle.append(row)
            return puzzle
    except FileNotFoundError:
        logger.error(f"Error: File '{filename}' not found.")
        return None
    except IOError:
        logger.error(f"Error: Unable to read the file '{filename}'.")
        return None


def save_state(state):
    with open(f'output.txt', 'w') as file:
        for row in state:
            file.write(','.join(str(cell) for cell in row) + '\n')


def word_to_grid(word, padding=5):
    word = word.upper()
    grid_height = len(next(iter(character_matrices.values())))

    total_width = sum(len(character_matrices[char][0]) + 1 for char in word if char in character_matrices) - 1
    total_width += 2 * padding

    grid = [[0] * total_width for _ in range(grid_height + 2 * padding)]

    start_col = padding
    for row_idx in range(grid_height):
        col_idx = start_col
        for char in word:
            if char in character_matrices:
                char_width = len(character_matrices[char][row_idx])
                for i in range(char_width):
                    grid[row_idx + padding][col_idx + i] = character_matrices[char][row_idx][i]
                col_idx += char_width + 1
    return grid