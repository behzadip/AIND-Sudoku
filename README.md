# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Naked twins strategy addresses a situation where among members of a unit (row,column,square,diagonal), there are two boxes with identical two available options. So if one box is digit 1, the other has to be digit 2 and vise versa, and this eliminates these two digits as possible values for their peers. In naked_twins function first a set of candidates which has only two possible values are identified. Next, from the list it identifies duplicate values, which corresponds to two boxes having the same available digits. Then, for each duplicate values, it goes through the peers and remove these digits from their set of possible numbers. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Two diagonal units and their corresponding members can be added to the set of all units of the game. Thereafter, all subsequent constraints and strategies will be applied to the diagonal units as well, ensuring we have no duplicate values. These new unit memebers are defined inside diag_units list in solutions.py.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.