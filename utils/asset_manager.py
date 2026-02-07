# Asset Manager
# Handles asset library management and metadata

import bpy
from mathutils import Vector
import os
import json


class AssetMetadata:
    """Metadata for a single asset."""
    
    def __init__(self, name, category, obj=None):
        self.name = name
        self.category = category  # 'tree', 'rock', 'grass', 'animal'
        self.obj = obj
        
        # Calculate bounding info if object provided
        if obj:
            self.bounding_radius = self._calculate_radius(obj)
            self.height = self._calculate_height(obj)
        else:
            self.bounding_radius = 1.0
            self.height = 2.0
        
        # Default placement preferences
        self.min_slope = 0.0
        self.max_slope = 30.0 if category == 'tree' else 90.0
        self.clustering_type = 'grouped' if category == 'tree' else 'scattered'
        self.min_spacing = self.bounding_radius * 2.0
    
    def _calculate_radius(self, obj):
        """Calculate approximate radius from bounding box."""
        if obj.type == 'MESH':
            bbox = obj.bound_box
            x_size = max(v[0] for v in bbox) - min(v[0] for v in bbox)
            y_size = max(v[1] for v in bbox) - min(v[1] for v in bbox)
            return max(x_size, y_size) / 2.0
        return 1.0
    
    def _calculate_height(self, obj):
        """Calculate height from bounding box."""
        if obj.type == 'MESH':
            bbox = obj.bound_box
            return max(v[2] for v in bbox) - min(v[2] for v in bbox)
        return 2.0
    
    def to_dict(self):
        """Convert to dictionary for serialization."""
        return {
            'name': self.name,
            'category': self.category,
            'bounding_radius': self.bounding_radius,
            'height': self.height,
            'min_slope': self.min_slope,
            'max_slope': self.max_slope,
            'clustering_type': self.clustering_type,
            'min_spacing': self.min_spacing
        }


class AssetLibrary:
    """Manages a collection of assets for terrain generation."""
    
    def __init__(self):
        self.assets = {
            'tree': [],
            'rock': [],
            'grass': [],
            'animal': []
        }
        self._load_default_assets()
    
    def _load_default_assets(self):
        """Load default primitive assets if no custom assets available."""
        # These will be created as simple primitives if needed
        self.default_assets = {
            'tree': {'name': 'Default_Tree', 'primitive': 'CONE', 'scale': (1, 1, 3)},
            'rock': {'name': 'Default_Rock', 'primitive': 'ICOSPHERE', 'scale': (1, 1, 0.7)},
            'grass': {'name': 'Default_Grass', 'primitive': 'CUBE', 'scale': (0.5, 0.5, 0.3)},
            'animal': {'name': 'Default_Animal', 'primitive': 'CUBE', 'scale': (1, 0.5, 0.5)}
        }
    
    def add_asset_from_object(self, obj, category):
        """Add an asset from an existing Blender object."""
        if category not in self.assets:
            return False
        
        metadata = AssetMetadata(obj.name, category, obj)
        self.assets[category].append(metadata)
        return True
    
    def add_asset_from_collection(self, collection_name, category):
        """Add all objects from a collection as assets."""
        if collection_name not in bpy.data.collections:
            return 0
        
        collection = bpy.data.collections[collection_name]
        count = 0
        
        for obj in collection.objects:
            if obj.type == 'MESH':
                if self.add_asset_from_object(obj, category):
                    count += 1
        
        return count
    
    def get_assets(self, category):
        """Get all assets of a specific category."""
        return self.assets.get(category, [])
    
    def get_random_asset(self, category):
        """Get a random asset from a category."""
        import random
        assets = self.get_assets(category)
        if not assets:
            return None
        return random.choice(assets)
    
    def create_default_asset(self, category):
        """Create a default primitive asset if no custom assets available."""
        if category not in self.default_assets:
            return None
        
        asset_info = self.default_assets[category]
        
        # Create primitive mesh
        if asset_info['primitive'] == 'CONE':
            bpy.ops.mesh.primitive_cone_add()
        elif asset_info['primitive'] == 'ICOSPHERE':
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2)
        elif asset_info['primitive'] == 'CUBE':
            bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.active_object
        obj.name = asset_info['name']
        obj.scale = asset_info['scale']
        
        # Create metadata
        metadata = AssetMetadata(obj.name, category, obj)
        
        return obj, metadata
    
    def has_assets(self, category):
        """Check if category has any assets."""
        return len(self.assets.get(category, [])) > 0
    
    def get_asset_count(self, category=None):
        """Get count of assets in a category or all categories."""
        if category:
            return len(self.assets.get(category, []))
        return sum(len(assets) for assets in self.assets.values())
    
    def clear_category(self, category):
        """Clear all assets from a category."""
        if category in self.assets:
            self.assets[category].clear()
    
    def clear_all(self):
        """Clear all assets from all categories."""
        for category in self.assets:
            self.assets[category].clear()
    
    def save_to_file(self, filepath):
        """Save asset library to JSON file."""
        data = {}
        for category, assets in self.assets.items():
            data[category] = [asset.to_dict() for asset in assets]
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filepath):
        """Load asset library from JSON file."""
        if not os.path.exists(filepath):
            return False
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Note: This loads metadata only, not actual objects
        # Objects need to be linked separately
        for category, assets_data in data.items():
            if category in self.assets:
                for asset_data in assets_data:
                    metadata = AssetMetadata(asset_data['name'], category)
                    metadata.bounding_radius = asset_data.get('bounding_radius', 1.0)
                    metadata.height = asset_data.get('height', 2.0)
                    metadata.min_slope = asset_data.get('min_slope', 0.0)
                    metadata.max_slope = asset_data.get('max_slope', 30.0)
                    metadata.clustering_type = asset_data.get('clustering_type', 'scattered')
                    metadata.min_spacing = asset_data.get('min_spacing', 2.0)
                    self.assets[category].append(metadata)
        
        return True


# Global asset library instance
_asset_library = None


def get_asset_library():
    """Get the global asset library instance."""
    global _asset_library
    if _asset_library is None:
        _asset_library = AssetLibrary()
    return _asset_library


def reset_asset_library():
    """Reset the global asset library."""
    global _asset_library
    _asset_library = AssetLibrary()
    return _asset_library
