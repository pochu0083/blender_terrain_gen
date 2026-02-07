# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Terrain Generator",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Terrain Gen",
    "description": "Generate realistic terrain with trees, rocks, grass, and animals using logic-based placement",
    "warning": "",
    "doc_url": "https://github.com/pochu0083/blender_terrain_gen",
    "category": "Object",
}

import bpy
from bpy.props import (
    FloatProperty,
    IntProperty,
    BoolProperty,
    EnumProperty,
    PointerProperty,
)
from bpy.types import PropertyGroup

# Import modules (will be created)
# from . import operators
# from . import panels
# from . import utils


# Property Group for addon preferences
class TerrainGenProperties(PropertyGroup):
    """Properties for Terrain Generator"""
    
    # Terrain settings
    terrain_size: FloatProperty(
        name="Terrain Size",
        description="Size of the terrain area",
        default=100.0,
        min=10.0,
        max=1000.0,
        unit='LENGTH'
    )
    
    # Tree settings
    tree_density: IntProperty(
        name="Tree Density",
        description="Number of trees to place",
        default=50,
        min=0,
        max=500
    )
    
    tree_min_distance: FloatProperty(
        name="Min Tree Distance",
        description="Minimum distance between trees",
        default=3.0,
        min=0.5,
        max=20.0,
        unit='LENGTH'
    )
    
    # Rock settings
    rock_density: IntProperty(
        name="Rock Density",
        description="Number of rocks to place",
        default=30,
        min=0,
        max=300
    )
    
    rock_min_distance: FloatProperty(
        name="Min Rock Distance",
        description="Minimum distance between rocks",
        default=2.0,
        min=0.5,
        max=10.0,
        unit='LENGTH'
    )
    
    # Grass settings
    grass_density: IntProperty(
        name="Grass Density",
        description="Number of grass patches to place",
        default=100,
        min=0,
        max=1000
    )
    
    # Animal settings
    animal_count: IntProperty(
        name="Animal Count",
        description="Number of animals to place",
        default=10,
        min=0,
        max=100
    )
    
    # Placement settings
    use_slope_filter: BoolProperty(
        name="Use Slope Filter",
        description="Avoid placing objects on steep slopes",
        default=True
    )
    
    max_slope_angle: FloatProperty(
        name="Max Slope Angle",
        description="Maximum slope angle for object placement (degrees)",
        default=30.0,
        min=0.0,
        max=90.0,
        subtype='ANGLE'
    )
    
    use_collision_detection: BoolProperty(
        name="Collision Detection",
        description="Prevent objects from intersecting",
        default=True
    )
    
    random_seed: IntProperty(
        name="Random Seed",
        description="Seed for random generation (0 for random)",
        default=0,
        min=0
    )


# Placeholder operator (will be expanded)
class TERRAIN_OT_generate(bpy.types.Operator):
    """Generate terrain with objects"""
    bl_idname = "terrain.generate"
    bl_label = "Generate Terrain"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.terrain_gen_props
        
        self.report({'INFO'}, f"Generating terrain with {props.tree_density} trees...")
        # TODO: Implement terrain generation logic
        
        return {'FINISHED'}


# Placeholder panel (will be expanded)
class TERRAIN_PT_main_panel(bpy.types.Panel):
    """Main panel for Terrain Generator"""
    bl_label = "Terrain Generator"
    bl_idname = "TERRAIN_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Terrain Gen'
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.terrain_gen_props
        
        # Terrain settings
        box = layout.box()
        box.label(text="Terrain Settings", icon='WORLD')
        box.prop(props, "terrain_size")
        box.prop(props, "random_seed")
        
        # Tree settings
        box = layout.box()
        box.label(text="Trees", icon='OUTLINER_OB_FORCE_FIELD')
        box.prop(props, "tree_density")
        box.prop(props, "tree_min_distance")
        
        # Rock settings
        box = layout.box()
        box.label(text="Rocks", icon='MESH_ICOSPHERE')
        box.prop(props, "rock_density")
        box.prop(props, "rock_min_distance")
        
        # Grass settings
        box = layout.box()
        box.label(text="Grass", icon='OUTLINER_OB_HAIR')
        box.prop(props, "grass_density")
        
        # Animal settings
        box = layout.box()
        box.label(text="Animals", icon='OUTLINER_OB_ARMATURE')
        box.prop(props, "animal_count")
        
        # Placement settings
        box = layout.box()
        box.label(text="Placement Logic", icon='SETTINGS')
        box.prop(props, "use_collision_detection")
        box.prop(props, "use_slope_filter")
        if props.use_slope_filter:
            box.prop(props, "max_slope_angle")
        
        # Generate button
        layout.separator()
        layout.operator("terrain.generate", text="Generate Terrain", icon='PLAY')


# Registration
classes = (
    TerrainGenProperties,
    TERRAIN_OT_generate,
    TERRAIN_PT_main_panel,
)


def register():
    """Register addon classes and properties"""
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Add properties to scene
    bpy.types.Scene.terrain_gen_props = PointerProperty(type=TerrainGenProperties)
    
    print("Terrain Generator addon registered")


def unregister():
    """Unregister addon classes and properties"""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Remove properties from scene
    del bpy.types.Scene.terrain_gen_props
    
    print("Terrain Generator addon unregistered")


if __name__ == "__main__":
    register()
