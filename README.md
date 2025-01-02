For fun added cities to see what it would look like, The only time contraints testing the time or GPU processing any data in art. Otherwise your query is done already.
![image](https://github.com/user-attachments/assets/f292ef31-441a-410f-996c-e9c6ad07352b)
# City Path Visualization

This Python project visualizes paths connecting cities or states using an algorithm that sorts and connects points based on their coordinates. The project supports 2D and 3D visualizations and includes animation capabilities.

## Features

- **Sort and Connect Cities**: Sort cities based on their coordinates and connect them to form a path.
- **2D and 3D Visualization**: Visualize the paths in both 2D and 3D spaces.
- **Animated Path Creation**: Animate the creation of paths between cities.
- **Customizable Input**: Use custom datasets or the provided example dataset for visualization.

## Usage

### Example Data

An example dataset of USA states is provided in the `usa_states` list within the script. You can modify or replace this dataset with your own custom data.

### Running the Script

To run the visualization script, simply execute the Python file:
```sh
python draw.py
```

### Code Overview

#### Import Libraries

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors
```

#### Data Preparation

Create a list of dictionaries representing the cities or states with their coordinates and other attributes:
```python
usa_states = [
    {'x': -97.0, 'y': 35.0, 'z': np.nan, 'name': 'Oklahoma', 'size_x': 69.0, 'size_y': 47.0},
    {'x': -98.0, 'y': 31.0, 'z': np.nan, 'name': 'Texas', 'size_x': 268.0, 'size_y': 278.0},
    # Add more states...
]
```

#### Sorting and Connecting Cities

The `sort_cities` function sorts and connects the cities based on their coordinates, considering optional attributes:
```python
def sort_cities(cities):
    # Implementation of sorting algorithm
```

#### Visualization

The `draw_cities` function visualizes the paths between the cities:
```python
def draw_cities(ax, sorted_path, zoom_level=1, offset_x=0, offset_y=0):
    # Implementation of drawing function
```

#### Animation

The `animate` function creates an animation of the path creation:
```python
def animate(frame, sorted_path, ax):
    # Implementation of animation function
```

### Example Command

If no paths are provided, the script will prompt an example command to generate the dataset:
```sh
python draw.py --num_cities 50
```

## Contributing

Feel free to submit issues, fork the repository, and make pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License.
