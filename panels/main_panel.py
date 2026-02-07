# Main UI Panel for Terrain Generator

import bpy


class TERRAIN_PT_main(bpy.types.Panel):
    """Main panel for Terrain Generator"""
    bl_label = "Terrain Generator"
    bl_idname = "TERRAIN_PT_main"
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


class TERRAIN_PT_objects(bpy.types.Panel):
    """Object settings panel"""
    bl_label = "Object Settings"
    bl_idname = "TERRAIN_PT_objects"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Terrain Gen'
    bl_parent_id = "TERRAIN_PT_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.terrain_gen_props
        
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


class TERRAIN_PT_placement(bpy.types.Panel):
    """Placement logic settings panel"""
    bl_label = "Placement Logic"
    bl_idname = "TERRAIN_PT_placement"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Terrain Gen'
    bl_parent_id = "TERRAIN_PT_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.terrain_gen_props
        
        layout.prop(props, "use_collision_detection")
        layout.prop(props, "use_slope_filter")
        
        if props.use_slope_filter:
            layout.prop(props, "max_slope_angle")


class TERRAIN_PT_actions(bpy.types.Panel):
    """Action buttons panel"""
    bl_label = "Actions"
    bl_idname = "TERRAIN_PT_actions"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Terrain Gen'
    bl_parent_id = "TERRAIN_PT_main"
    
    def draw(self, context):
        layout = self.layout
        
        # Generate button
        layout.operator("terrain.generate", text="Generate Terrain", icon='PLAY')


def register():
    bpy.utils.register_class(TERRAIN_PT_main)
    bpy.utils.register_class(TERRAIN_PT_objects)
    bpy.utils.register_class(TERRAIN_PT_placement)
    bpy.utils.register_class(TERRAIN_PT_actions)


def unregister():
    bpy.utils.unregister_class(TERRAIN_PT_actions)
    bpy.utils.unregister_class(TERRAIN_PT_placement)
    bpy.utils.unregister_class(TERRAIN_PT_objects)
    bpy.utils.unregister_class(TERRAIN_PT_main)
