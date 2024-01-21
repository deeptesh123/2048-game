# 2048-game
The classic 2048 game made using tkinter, python
It consists of three classes:

1. grid-> In this class, the grid is initialized and the various operations to be performed are defined here
   
   a. create_empty_grid(): creates an empty board to start with
   
   b. retrieve_empty_cells(): creates a list of all available empty cells
   
   c. select_random_cell(): from the list of empty cells, it selects a cell at random
   
   d. reverse_row(): reverses the contents of a row
   
   e. reverse_grid(): reverses every row of the grid
   
   f. transpose(): transposes the grid
   
   g. row_merge_left(): merges a row towards left according to the rules of the game
   
   h. grid_merge_left(): merges the whole grid/board towars left
   
   i. can_merge(): checks whether any merging is possible in the grid
   
   j. has_empty_cells(): checks for empty cells in the grid
   
   k. reached_2048(): checks whether player has reached 2048(goal) or not

3. GUI-> This class sets up and manages the Graphic User Interface.
   
   a. start(): It paints/updates the board based of the values of the grid

5. Game_flow-> Dictates the flow of the game
   
   a. game_over(): Checks whether the game has finished or not
   
   b. set_ random_cells():sets the two initial cells at the start of the game
   
   c. initialize(): initiates the game by setting up the board
   
   d. can_move(): checks whether the player can make a move or not
   
   e. merge_left(): simulated the move of swipe left
   
   f. merge_right(): simulated the move of swipe right
   
   g. merge_up(): simulated the move of swipe up
   
   h. merge_down(): simulated the move of swipe down
   
   i. undo(): simulates the effects of undo
   
   j. movements(): It controls the game proceedings, making the move, as specified by the player and chwcking for game over                     of game won at after each move
   
