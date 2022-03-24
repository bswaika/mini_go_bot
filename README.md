# MiniGO Agent 
#### CSCI 561 Assignment #2

## IDEAS

### Strategies
-----

**Starting Moves:**  
&nbsp;&nbsp;&nbsp;&nbsp;Remember to never start at the borders of the board because you are starting with lesser liberties on the stones you place. 

**Tips:**  
- Minimizing the amount of liberties your opponent has, and maximizing your own, is key to success.
- Bent lines will always have fewer liberties than straight lines.
- A group with only one eye is effectively a dead group.

### Minimax Tree Search
-----

**Branching and Expansion:**  
&nbsp;&nbsp;&nbsp;&nbsp;It is important to note that even for a 5x5 game of GO, the game tree is huge. The tree generation process can be dependent on the number of nodes in the total game tree, and a threshold that effectively acts as a factor for generating larger trees by the end of the game (when it has lesser nodes remaining), and smaller trees up top (when the number of nodes remaining are a lot). We can identify 2 threshold values which would act as a factor for branching and depth for tree generation.  
&nbsp;&nbsp;&nbsp;&nbsp;The idea here is as follows:
- *Total # of nodes before a move (T)* roughly equals *the number of legal moves* * *the number of legal moves in the next state* * ... * *the number of moves before a terminal state is reached or before the move limit expires*
- *Branching factor (B)* can be increasing as the game progresses, due to lesser and lesser moves remaining in each level as the game progresses. Thus, *Branch threshold (t_b)* needs to keep decreasing as a function of some parameter that possibly chooses a nice subset of the # of moves to expand at a level
- *Depth (D)* can be increasing as the game progresses, since *B* decreases as the game progresses, hence, implying that lesser # of nodes need to be generated for higher depth levels. Thus, *Depth threshold (t_d)* needs to keep decreasing as a function of some parameter.
- Finally, *B* = *T* / *t_b*, and *D* = *T* / *t_d*
- Also, *t_b* and *t_d* are decreasing functions of the number of iterations into the game or increasing functions of remaining moves in the game.  

**Evaluation Functions:**  
&nbsp;&nbsp;&nbsp;&nbsp;Since, we plan to cutoff the tree with some *B* and *D*, we need *eval(BOARD)* to return an estimate value of the board based off the following criterion:  
- *Territory Controlled (control)*: Identifies the territory control on a board by each of the players
- *Capture Opportunities (captures)*: Identifies the possibility of 1-move, 2-move, 3-move captures and weighs them decreasingly, such that 1-move captures are prioritized over 2-move and 2-move captures over 3-move ones.
- *Eyes (eyes)*: Identifies eyes and prioritizes 2-eye shapes, and penalizes 1-eye shapes.
- *Euler Number (e)*: Denotes the number of objects minus the number of holes, and is a good measure for both eyes and connections

**Move Filtering:**  
&nbsp;&nbsp;&nbsp;&nbsp;It is key to identify illegal moves that lead to capture of the agent's pieces, but also write logic to identify where such a move could possibly lead to a capture. Also, Ko moves need to be eliminated.

**Alpha-Beta Pruning:**  
&nbsp;&nbsp;&nbsp;&nbsp;Implement the basic algorithm for pruning, and maybe go on to implement Iterative Deepening Search to do move ordering based on *eval(BOARD)*.



## TODO
- Go through the starter code
- Game Playing  
    - [x] Setup Board
    - [x] Setup Player Logic
      - [x] Parsing File
      - [x] Board Evaluation
      - [x] Identify legal moves
      - [x] Game Tree Expansion
      - [x] Action choosing
      - [x] Generating File
- Minimax
  - [x] Cutoff Thresholds
  - [x] Evaluation Function
  - [x] Alpha-Beta Pruning
  - [x] Move Ordering 