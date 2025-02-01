from build123d import *
#from ocp_vscode import show_all, Camera

# Parameters
length = 1260
width = 775
height = 25
x_offset = 30
y1_offset = 30
y2_offset = 45
spacing_small = 50
spacing_large = 100

# Radius and diameters
diameter = 6
radius = diameter / 2

# Computed parameters
half_length = length / 2
half_width = width / 2

# Main design
with BuildPart() as part_builder:
    Box(length, width, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((0, spacing_small)):
        with GridLocations(x_spacing=spacing_large, y_spacing=spacing_large, x_count=13, y_count=4, align=(Align.CENTER, Align.MIN, Align.CENTER)):
            Hole(radius)
    with Locations((0, -half_width+y2_offset)):
        with GridLocations(x_spacing=spacing_large, y_spacing=spacing_large, x_count=7, y_count=4, align=(Align.MAX, Align.MIN, Align.CENTER)):
            Hole(radius)        
    with Locations((spacing_small, -half_width+y2_offset)):
        with GridLocations(x_spacing=spacing_small, y_spacing=spacing_small, x_count=12, y_count=7, align=(Align.MIN, Align.MIN, Align.CENTER)):
            Hole(radius)
                           
#show_all(reset_camera=Camera.KEEP)
part = part_builder.part
part

filename_stem = "sacrificial_table"
export_step(part, f"{filename_stem}.step")
export_stl(part, f"{filename_stem}.stl")
