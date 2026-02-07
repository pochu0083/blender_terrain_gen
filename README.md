# Blender Terrain Generator Plugin

A Blender addon for generating realistic terrain scenes with trees, rocks, grass, and animals using intelligent, logic-based placement algorithms.

## Features

- **Logic-Based Placement**: Objects are placed using Poisson disk sampling for natural distribution
- **Collision Avoidance**: Prevents objects from intersecting or overlapping
- **Slope Filtering**: Avoids placing objects on steep terrain
- **Customizable Parameters**: Control density, spacing, and placement rules
- **Asset Reuse**: Works with your existing 3D assets

## Installation

1. Download or clone this repository
2. In Blender, go to `Edit > Preferences > Add-ons`
3. Click `Install...` and select the `blender_plugin` folder (or zip it first)
4. Enable the addon by checking the box next to "Object: Terrain Generator"

## Usage

1. Open Blender and look for the "Terrain Gen" tab in the 3D Viewport sidebar (press `N` if not visible)
2. Configure your terrain settings:
   - **Terrain Size**: Overall size of the terrain area
   - **Random Seed**: Set a seed for reproducible results (0 for random)
3. Adjust object densities:
   - **Trees**: Number and minimum spacing
   - **Rocks**: Number and minimum spacing
   - **Grass**: Number of patches
   - **Animals**: Number to place
4. Configure placement logic:
   - **Collision Detection**: Prevent overlapping objects
   - **Slope Filter**: Avoid steep slopes
   - **Max Slope Angle**: Maximum terrain angle for placement
5. Click "Generate Terrain" to create your scene

## Project Structure

```
blender_plugin/
├── __init__.py              # Main addon file with registration
├── operators/               # Operator classes
│   ├── __init__.py
│   └── terrain_generator.py # Main terrain generation operator
├── panels/                  # UI panel classes
│   ├── __init__.py
│   └── main_panel.py        # Main UI panels
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── placement.py         # Placement algorithms (Poisson disk sampling)
│   ├── collision.py         # Collision detection
│   └── terrain.py           # Terrain creation and manipulation
├── PLUGIN_SPECS.md          # Detailed plugin specifications
└── README.md                # This file
```

## Requirements

- Blender 3.0 or higher
- Python 3.x (included with Blender)

## Development Status

**Current Version**: 1.0.0 (Initial Structure)

This is the initial project structure with boilerplate code. The core terrain generation logic is ready to be implemented in the operator classes.

### TODO:
- [ ] Implement asset collection system
- [ ] Complete terrain generation algorithm
- [ ] Add tree placement logic
- [ ] Add rock placement logic
- [ ] Add grass placement with particle systems
- [ ] Add animal placement with behavioral logic
- [ ] Add terrain height variation
- [ ] Add biome support
- [ ] Add preset system

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

GPL v2 or later

## Links

- GitHub Repository: https://github.com/pochu0083/blender_terrain_gen
- Documentation: See PLUGIN_SPECS.md for detailed specifications
