# Placement utility functions
# Logic-based object placement algorithms

import random
from mathutils import Vector


def generate_poisson_disk_samples(width, height, min_distance, max_attempts=30):
    """
    Generate points using Poisson disk sampling for natural distribution.
    This ensures minimum distance between points while maintaining randomness.
    
    Args:
        width: Width of the area
        height: Height of the area
        min_distance: Minimum distance between points
        max_attempts: Maximum attempts to place each point
    
    Returns:
        List of Vector positions
    """
    cell_size = min_distance / (2 ** 0.5)
    grid_width = int(width / cell_size) + 1
    grid_height = int(height / cell_size) + 1
    
    grid = [[None for _ in range(grid_height)] for _ in range(grid_width)]
    points = []
    active_list = []
    
    # Start with a random point
    first_point = Vector((random.uniform(0, width), random.uniform(0, height), 0))
    points.append(first_point)
    active_list.append(first_point)
    
    grid_x = int(first_point.x / cell_size)
    grid_y = int(first_point.y / cell_size)
    grid[grid_x][grid_y] = first_point
    
    while active_list:
        idx = random.randint(0, len(active_list) - 1)
        point = active_list[idx]
        found = False
        
        for _ in range(max_attempts):
            angle = random.uniform(0, 2 * 3.14159)
            radius = random.uniform(min_distance, 2 * min_distance)
            
            new_x = point.x + radius * random.uniform(-1, 1)
            new_y = point.y + radius * random.uniform(-1, 1)
            
            if 0 <= new_x < width and 0 <= new_y < height:
                new_point = Vector((new_x, new_y, 0))
                
                if is_valid_point(new_point, grid, cell_size, min_distance, grid_width, grid_height):
                    points.append(new_point)
                    active_list.append(new_point)
                    
                    grid_x = int(new_point.x / cell_size)
                    grid_y = int(new_point.y / cell_size)
                    grid[grid_x][grid_y] = new_point
                    found = True
                    break
        
        if not found:
            active_list.pop(idx)
    
    return points


def is_valid_point(point, grid, cell_size, min_distance, grid_width, grid_height):
    """
    Check if a point is valid (far enough from other points).
    """
    grid_x = int(point.x / cell_size)
    grid_y = int(point.y / cell_size)
    
    # Check neighboring cells
    for i in range(max(0, grid_x - 2), min(grid_width, grid_x + 3)):
        for j in range(max(0, grid_y - 2), min(grid_height, grid_y + 3)):
            if grid[i][j] is not None:
                distance = (point - grid[i][j]).length
                if distance < min_distance:
                    return False
    
    return True


def calculate_slope_angle(normal):
    """
    Calculate the slope angle from a surface normal.
    
    Args:
        normal: Surface normal vector
    
    Returns:
        Angle in degrees
    """
    import math
    up = Vector((0, 0, 1))
    angle = math.acos(max(-1, min(1, normal.dot(up))))
    return math.degrees(angle)


def is_valid_slope(normal, max_slope_degrees):
    """
    Check if a surface slope is within acceptable range.
    
    Args:
        normal: Surface normal vector
        max_slope_degrees: Maximum allowed slope in degrees
    
    Returns:
        True if slope is valid
    """
    slope = calculate_slope_angle(normal)
    return slope <= max_slope_degrees
