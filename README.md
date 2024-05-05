# Game of Life SAT Solver
The Game of Life SAT Solver is hosted at [URL](http://18.118.210.39:8501/).

## Overview
The Game of Life SAT Solver is a sophisticated tool developed to tackle the inherent non-reversibility of Conway's Game of Life, a cellular automaton devised by the British mathematician John Horton Conway in 1970. Unlike forward operations in the Game of Life, determining previous states is not straightforward due to its non-reversible nature. This tool transforms the problem into a boolean satisfiability (SAT) problem, allowing it to discover one of the potentially infinite previous states of a given configuration. This approach provides unique insights and facilitates deeper research into cellular automaton behaviors.

## Installation

### Setup
1. **Clone the repository:**
   ```bash
    git clone https://github.com/yourusername/reverse-cgol.git
    cd reverse-cgol
   ```

2. **Install Python dependencies:**
   ```bash
        pip install -r requirements.txt
   ```

3. **Setup SAT Solver and Tools:**
     ```bash
        python setup_project.py --setup # Run the setup script
        python solver.py --setup --puzzle path/to/your/puzzlefile.txt # Run the solver with the setup flag
     ```

## How to Use
The Game of Life SAT Solver can be run from the command line with various options:

### Command Line Arguments
- `--setup`: Set up necessary tools and configurations. Use this the first time you run the solver.
- `--puzzle <filename>`: Specify the filename of a puzzle file to solve. The file should contain a grid of 0s and 1s, where each number is separated by commas. Each line in the file represents a row in the Game of Life grid. It is crucial that all rows are of equal length to ensure a valid rectangular grid. Here is an example of the file format:
    ```
    0,1,0,0,1
    1,0,0,1,0
    0,0,1,0,0
    1,1,0,1,1
    0,1,0,0,1
    ```
- `--word <word>`: Convert the given word into a Game of Life grid and solve its backward states.
- `--keep_cnf`: Retain the CNF files generated during solving for debugging or analysis.

### Running the Solver
To solve a puzzle from a file:
```bash
python solver.py --puzzle path/to/your/puzzlefile.txt
```

To generate and solve a grid from a word:
```bash
python solver.py --word "Hello"
```