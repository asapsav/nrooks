import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

def plot_voronoi(board_size, queen_positions):
    # Create a Voronoi diagram from the queen positions
    vor = Voronoi(queen_positions)
    
    # Plot the Voronoi diagram
    fig, ax = plt.subplots()
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='black', line_width=2, line_alpha=0.6, point_size=10)
    
    # Highlight the queen positions
    ax.plot([p[1] for p in queen_positions], [p[0] for p in queen_positions], 'ro')
    
    # Set the limits and grid
    ax.set_xlim([0, board_size-1])
    ax.set_ylim([0, board_size-1])
    ax.set_xticks(range(board_size))
    ax.set_yticks(range(board_size))
    ax.grid(True)
    
    # Customize axes to look like a chessboard
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()  # Invert y axis to match typical matrix indexing
    
    plt.show()

# Define the board size and queen positions
size = 8  # Board size
queen_positions = [(0.5, 0.5), (1.5, 2.5), (2.5, 4.5), (3.5, 6.5), (4.5, 1.5), (5.5, 3.5), (6.5, 5.5), (7.5, 7.5)]

# Plot the Voronoi diagram
plot_voronoi(size, queen_positions)
