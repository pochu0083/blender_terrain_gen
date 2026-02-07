# Collision detection utility functions
# Prevent object intersections and overlaps

from mathutils import Vector
import bpy


def check_collision_sphere(position, radius, existing_objects):
    """
    Check if a sphere at the given position collides with existing objects.
    
    Args:
        position: Vector position to check
        radius: Radius of the sphere
        existing_objects: List of (position, radius) tuples for existing objects
    
    Returns:
        True if collision detected, False otherwise
    """
    for obj_pos, obj_radius in existing_objects:
        distance = (position - obj_pos).length
        if distance < (radius + obj_radius):
            return True
    return False


def check_collision_bbox(position, bbox_size, existing_objects):
    """
    Check if a bounding box at the given position collides with existing objects.
    
    Args:
        position: Vector position (center) to check
        bbox_size: Vector representing the size of the bounding box
        existing_objects: List of (position, bbox_size) tuples for existing objects
    
    Returns:
        True if collision detected, False otherwise
    """
    half_size = bbox_size / 2
    
    for obj_pos, obj_bbox in existing_objects:
        obj_half = obj_bbox / 2
        
        # AABB collision detection
        if (abs(position.x - obj_pos.x) < (half_size.x + obj_half.x) and
            abs(position.y - obj_pos.y) < (half_size.y + obj_half.y) and
            abs(position.z - obj_pos.z) < (half_size.z + obj_half.z)):
            return True
    
    return False


def get_object_bounds(obj):
    """
    Get the bounding box size of a Blender object.
    
    Args:
        obj: Blender object
    
    Returns:
        Vector representing the bounding box dimensions
    """
    if obj.type == 'MESH':
        bbox = obj.bound_box
        min_co = Vector((min(v[0] for v in bbox), 
                        min(v[1] for v in bbox), 
                        min(v[2] for v in bbox)))
        max_co = Vector((max(v[0] for v in bbox), 
                        max(v[1] for v in bbox), 
                        max(v[2] for v in bbox)))
        return max_co - min_co
    return Vector((1, 1, 1))  # Default size


def get_object_radius(obj):
    """
    Get an approximate radius for an object (for sphere collision).
    
    Args:
        obj: Blender object
    
    Returns:
        Float radius value
    """
    bounds = get_object_bounds(obj)
    return max(bounds.x, bounds.y, bounds.z) / 2


class CollisionManager:
    """
    Manager class to track placed objects and check collisions.
    """
    
    def __init__(self):
        self.objects = []  # List of (position, radius) tuples
    
    def add_object(self, position, radius):
        """Add an object to the collision tracking."""
        self.objects.append((Vector(position), radius))
    
    def check_collision(self, position, radius):
        """Check if a new object would collide."""
        return check_collision_sphere(Vector(position), radius, self.objects)
    
    def clear(self):
        """Clear all tracked objects."""
        self.objects.clear()
    
    def get_count(self):
        """Get the number of tracked objects."""
        return len(self.objects)
