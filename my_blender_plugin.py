# Blender Python Plugin Template

class MyBlenderPlugin:
    def __init__(self):
        pass

    def execute(self):
        print('Hello from my Blender plugin!')

# Register the plugin with Blender
import bpy
bpy.utils.register_class(MyBlenderPlugin)
