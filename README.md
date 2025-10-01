# 8-Puzzle Solver

<img width="599" height="434" alt="image" src="https://github.com/user-attachments/assets/aac22d46-f949-4f90-bf9f-93f44779804a" />

This project is a **Graphical User Interface (GUI) based solver for the 8-Puzzle problem**.

It uses different search algorithms (**A\*** and **Greedy Best First Search**) combined with two popular heuristics (**Manhattan Distance** and **Tiles Out of Place**) to find the optimal or near-optimal solution path from an initial state to a goal state.

The GUI is built with **Tkinter** and allows users to:
* Enter a custom initial puzzle state and a custom goal state.
* Select the desired search algorithm and heuristic combination.
* Visualize the puzzle solution step-by-step.
* Automatically fast-forward/backward through the solution path.
* View heuristic values ($g(n)$, $h(n)$, $f(n)$) during the search process.
* Display a performance analysis summary.

---

## Features

### Algorithms Supported

The solver supports the following combinations:
* **A\* Search** with **Manhattan Distance** heuristic
* **A\* Search** with **Tiles Out of Place** heuristic
* **Greedy Best First Search** with **Manhattan Distance** heuristic
* **Greedy Best First Search** with **Tiles Out of Place** heuristic

### Visualization Controls
* Step forward/backward through states (**Next** / **Back**).
* Automatic fast forward/backward traversal (**>>** / **<<**).
* Reset the visualization to the initial state.
* Stop/pause the animation.

### Analysis Display
Once the solution is found, the program displays key performance metrics:
* **Nodes Expanded**
* **Search Depth** (Solution path length)
* **Search Cost**
* **Runtime** (in seconds)

---

## Requirements

* **Python 3.7+**
* **Tkinter** (Usually included with standard Python distributions).

No additional external libraries are required.

---

## How to Run

### Steps
1.  Clone or download this repository.
2.  Run the interface using the following command:

    ```bash
    python interface.py
    ```

### GUI Usage

1.  **Input Initial State**: Click **Enter initial state** and input a 9-digit string (e.g., `724506831`). The digit **0** represents the blank tile.
2.  **Input Goal State (Optional)**: Click **Enter goal state** if you want a custom goal state (the default is `123456780`).
3.  **Select Algorithm**: Choose an algorithm from the dropdown menu.
4.  **Solve**: Click **Solve** to begin the computation and visualization.
5.  **Explore**: Use the navigation buttons (**Back, Next, <<, >>, Reset, Stop**) to explore the solution path.

### Example

* **Initial State**: `724506831`
* **Goal State**: `123456780` (Default)
* **Algorithm**: A\* Manhattan Distance

The program will compute the path and show the step-by-step solution in the puzzle grid.

---

## File Overview

* `main.py`
    * Contains the core search algorithm implementations: A\* Search and Greedy Best First Search, each supporting both heuristics.
    * Includes utility functions for heuristic calculation, solvability checks, child generation, and path reconstruction.

* `interface.py`
    * Provides the Tkinter-based GUI for user interaction and puzzle visualization.
    * Manages input/output states, user controls, and the display of the solution and performance analysis.

---

## Important Notes

* Input states must be **exactly 9 digits long** (0–8) without repetition.
* Not all initial states are solvable. If the puzzle is determined to be **unsolvable**, the program will notify the user.

---

## Author
**Name**: William Hans Chandra  
**Institution**: Institut Teknologi Sepuluh Nopember (ITS), Surabaya  
**Course**: Artificial Intelligence Concepts 
