import streamlit as st
import time
from matplotlib import pyplot as plt
from solver import solve_loop
from utils import word_to_grid, plot_game_of_life
from matplotlib.colors import LinearSegmentedColormap

def plot_grid(grid, title):
    colors = ["#0c1016", "#ffffff"]  # Dark grey for dead cells, white for live cells
    cmap = LinearSegmentedColormap.from_list("custom_binary", colors, N=2)

    fig, ax = plt.subplots()
    ax.imshow(grid, cmap=cmap)
    ax.set_title(title, color='white')
    ax.axis('off')
    fig.patch.set_facecolor('#0c1016')
    ax.set_facecolor('#0c1016')

    return fig

def main():
    st.title('Reversing the Game of Life')
    st.write('Provide input as either a word or a grid of 0s and 1s.')

    input_method = st.radio('Choose input method:', ('Word', 'Grid'))

    if input_method == 'Word':
        word = st.text_input('Enter a word:')
        
        if len(word) > 8:
            padding = 10
        elif len(word) > 5:
            padding = 8
        else:
            padding = 5

        if word:
            grid = word_to_grid(word.upper(), padding=padding)
            st.text('Reversing from the following grid:')
            fig = plot_grid(grid, title="Initial Grid")
            st.pyplot(fig)
    else:
        grid_input = st.text_area('Enter grid as comma-separated 0s and 1s with newlines separating rows:',
                                  '0,1,0\n1,0,1\n0,1,0')
        try:
            grid = [[int(num) for num in row.split(',')] for row in grid_input.split('\n')]
            fig = plot_grid(grid, title="Initial Grid")
            st.pyplot(fig)
        except ValueError:
            st.error('Invalid grid format')
            grid = None

    if st.button('Solve'):
        status_text = st.empty()
        status_text.write('Solving for the earliest possible state (this might take a couple minutes)...')

        result, num_iterations = solve_loop(grid, False)
        status_text.empty()

        if result is not None:
            st.markdown('---')
            st.success(f"{num_iterations} previous states found.")
            evolution_fig = plot_game_of_life(result, num_transitions=num_iterations + 1, states_per_row=3)
            st.pyplot(evolution_fig)
        else:
            st.error('No valid initial state found that evolves into the given final state.')


if __name__ == "__main__":
    main()

