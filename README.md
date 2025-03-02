
# A* Visualizer
A python library to visualize A* Path finding Algorithm in action



![Image](https://raw.githubusercontent.com/karthik-saiharsh/A-star-visualiser/refs/heads/main/demo.png)


# Usage

- Download the source code
- Import the Colors and Visualizer classes

```python
from main import Colors, Visualizer
```

- The Visualizer class takes in 4 parameters
    - `size`: size of the window (in px)
    - `rows`: Number of rows and columns in the grid
    - `Colors`: Colors Used in the Visualizer
    - `Enable Diagonal Paths`: Are diagonal paths allowed ? (boolean)



- Create a Colors Class
```python
col = Colors() # Use Default Colors
vis = Visualizer(1300, 20, col, False)
                                  ^ No Diagonal Paths
```
- The program can now be run.


## Adding Nodes
- The first click (left mouse) adds the start node.
- The second click (left mouse) adds the end/destination node.
- Every click after the second creates a barrier/wall node. A barrier is a node which cannot become a path.
- A right click removes resets a node


## Using Custom Colors
```python
col = Colors() # Create a colors Object

col.neutral = (255, 247, 243) # Neutral Nodes
col.explored = (33, 53, 85) # Nodes which have been explored 
col.exploring = (62, 88, 121) # Nodes being explored in the current iteration
col.inactive = (42, 51, 53) # Wall/Barrier nodes
col.path = (250, 208, 196) # Nodes which form the path
col.end = (239, 182, 200) # End Node
col.start = (239, 182, 200) # Start Node


```
- This colors object can noe be passed into the Visualizer class

```python
vis = Visualizer(1500, 30, col, True)
                            ^ Pass the custom Colors
```


## Custom Heuristic Functions
- The default implementation uses euclidean distance.
- Other Heuristic Functions can be set as follows

```python
from main import Colors, Visualizer

# Custom Heuristic Function
def h(position1, position2):
    x1, y1 = position1
    x2, y2 = position2
    return abs((x2-x1) + (y2-y1))

col = Colors()
vis = Visualizer(1300, 20, col, False)
vis.custom_heuristic = h # the new heuristic function is used
```
