import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors
import json
import os

def bit_spread(value):
    value = (value | (value << 8)) & 0x00FF00FF
    value = (value | (value << 4)) & 0x0F0F0F0F
    value = (value | (value << 2)) & 0x33333333
    value = (value | (value << 1)) & 0x55555555
    return value

def morton_code(city):
    x, y = city['x'], city['y']
    x = int(x * 10000)
    y = int(y * 10000)
    return bit_spread(x) | (bit_spread(y) << 1)

def is_path_intersect(new_path, paths):
    for path in paths:
        path = [np.array(p) for p in path]
        new_path = [np.array(p) for p in new_path]
        if len(path[0]) == 2:
            path[0] = np.append(path[0], 0)
        if len(path[1]) == 2:
            path[1] = np.append(path[1], 0)
        if len(new_path[0]) == 2:
            new_path[0] = np.append(new_path[0], 0)
        if len(new_path[1]) == 2:
            new_path[1] = np.append(new_path[1], 0)
        cross1 = np.cross(path[1] - path[0], new_path[0] - path[0])
        cross2 = np.cross(path[1] - path[0], new_path[1] - path[0])
        cross3 = np.cross(new_path[1] - new_path[0], path[0] - new_path[0])
        cross4 = np.cross(new_path[1] - new_path[0], path[1] - new_path[0])
        if (np.all(cross1 * cross2 <= 0) and np.all(cross3 * cross4 <= 0)):
            return True
    return False

def connect_cities(cities):
    if not cities:
        print("No cities to process.")
        return []
    cities_sorted = sorted(cities, key=lambda c: (c['x'], c['y']), reverse=True)
    sorted_route = [cities_sorted.pop(0)]
    paths = []
    while cities_sorted:
        current_city = sorted_route[-1]
        current_coords = [current_city.get('x', 0), current_city.get('y', 0)]
        if 'z' in current_city:
            current_coords.append(current_city['z'])
        min_distance = float('inf')
        closest_city_idx = -1
        for i, city in enumerate(cities_sorted):
            city_coords = [city.get('x', 0), city.get('y', 0)]
            if 'z' in city:
                city_coords.append(city['z'])
            distance = np.linalg.norm(np.array(city_coords) - np.array(current_coords))
            if distance < min_distance:
                new_path = [np.array(current_coords), np.array(city_coords)]
                if not is_path_intersect(new_path, paths):
                    min_distance = distance
                    closest_city_idx = i
        sorted_route.append(cities_sorted.pop(closest_city_idx))
        new_path = [np.array([current_city['x'], current_city['y'], current_city.get('z', 0)]), 
                    np.array([sorted_route[-1]['x'], sorted_route[-1]['y'], sorted_route[-1].get('z', 0)])]
        paths.append(new_path)
    sorted_route.append(sorted_route[0])
    return sorted_route

def visualize_route(ax, sorted_route, zoom=1, offset_x=0, offset_y=0):
    ax.clear()
    ax.set_facecolor('black')
    ax.set_xticks([])
    ax.set_yticks([])
    min_x = min(city.get('x', 0) for city in sorted_route)
    max_x = max(city.get('x', 0) for city in sorted_route)
    min_y = min(city.get('y', 0) for city in sorted_route)
    max_y = max(city.get('y', 0) for city in sorted_route)
    container_coords = [(min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x, min_y), (min_x, min_y)]
    ax.plot([c[0] + offset_x for c in container_coords], [c[1] + offset_y for c in container_coords], color='white')
    colors = list(mcolors.TABLEAU_COLORS.values())
    for index in range(1, len(sorted_route)):
        city = sorted_route[index]
        prev_city = sorted_route[index - 1]
        color = colors[index % len(colors)]
        x_coords = [prev_city.get('x', 0) + offset_x, city.get('x', 0) + offset_x]
        y_coords = [prev_city.get('y', 0) + offset_y, city.get('y', 0) + offset_y]
        if 'z' in city and 'z' in prev_city:
            z_coords = [prev_city.get('z', 0), city.get('z', 0)]
            ax.plot(x_coords, y_coords, zs=z_coords, color=color)
        else:
            ax.plot(x_coords, y_coords, color=color)
    if 'z' in sorted_route[0]:
        ax.scatter([city.get('x', 0) + offset_x for city in sorted_route], 
                   [city.get('y', 0) + offset_y for city in sorted_route], 
                   [city.get('z', 0) for city in sorted_route], 
                   c='white', s=5)
    else:
        ax.scatter([city.get('x', 0) + offset_x for city in sorted_route], 
                   [city.get('y', 0) + offset_y for city in sorted_route], 
                   c='white', s=5)

def animate_route(frame, sorted_route, ax):
    ax.clear()
    visualize_route(ax, sorted_route[:frame + 1])

def save_data(file, primary, secondary=None):
    with open(file, 'w') as f:
        data = {'primary': primary}
        if secondary:
            data['secondary'] = secondary
        json.dump(data, f)

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data, []
            return data.get('primary', []), data.get('secondary', [])
    return [], []

def calculate_short_paths(cities):
    # Implement your logic here
    return []

file = 'usa_states.json'
primary, secondary = load_data(file)
usa_states = primary

if not usa_states:
    print("No paths found.")
else:
    sorted_route = connect_cities(usa_states)
    short_paths = []
    if not secondary:
        short_paths = calculate_short_paths(usa_states)
        save_data('sorted_paths.json', sorted_route, short_paths)
    else:
        short_paths = secondary

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d' if 'z' in usa_states[0] else 'rectilinear')
    visualize_route(ax, sorted_route)
    ani = FuncAnimation(fig, animate_route, frames=len(sorted_route), fargs=(sorted_route, ax), interval=1, repeat=False)
    plt.show()
