from typing import Literal
from build123d import *
from ocp_vscode import show_object

# card_width = 2.5 * IN
card_width = 65.5 * MM
# card_length = 3.5 * IN
card_length = 80.0 * MM
# height = 0.5 * IN
height = 12 * MM
wall = 3 * MM
gap = 0.5 * MM
pad_spacingX = 50.5 * MM
pad_spacingY = 48 * MM
pad_height = 4 * MM
pad_diameter = 7 * MM
pad_hole_diam = 3.0 * MM
fontsz, fontht = 12.0, 0.2
with BuildPart() as box_builder:
    with BuildSketch() as plan:
        Rectangle(card_width + 2 * wall, card_length + 2 * wall)
        fillet(plan.vertices(), radius=card_width / 15)
    extrude(amount=wall)
    with BuildSketch(box_builder.faces().sort_by(Axis.Z)[-1]) as holes: # box mounting holes
        with GridLocations(
            x_spacing=card_width - 2 -2 * wall , y_spacing=card_length - 2 - 2 * wall, x_count=4, y_count=4
        ):
            Circle(1.5)
    extrude(amount= -wall, mode=Mode.SUBTRACT)        
    with BuildSketch(box_builder.faces().sort_by(Axis.Z)[-1]) as walls:
        add(plan.sketch)
        offset(plan.sketch, amount=-wall, mode=Mode.SUBTRACT)
    extrude(amount=height * 1.333)
    with BuildSketch(box_builder.faces().sort_by(Axis.Z)[-1]) as inset_walls:
        offset(plan.sketch, amount=-(wall + gap) / 2, mode=Mode.ADD)
        offset(plan.sketch, amount=-wall, mode=Mode.SUBTRACT)
    extrude(amount=height / 2)
    with BuildSketch(box_builder.faces().sort_by(Axis.Y)[-1]): # add a hole for the USB lead
        with Locations((-2, -10 - 0.2)): # (x,z())
              RectangleRounded(13,13,1.5)
              offset(amount=0 )
    extrude(amount=10, both=True, mode=Mode.SUBTRACT)
    with BuildSketch(box_builder.faces().sort_by(Axis.Y)[-1]): # add holes for ext wiring
        with Locations((-21, -4)): # (x,z())
              Circle(3)
            #  offset(amount=wall)
        with Locations((21, -4)): # (x,z())
              Circle(3)            
    extrude(amount=wall, both=True, mode=Mode.SUBTRACT)    
#    with BuildSketch(box_builder.faces().sort_by(Axis.Z)[-1]):    
    with BuildSketch(Plane.XY.offset(wall)) as sk2: # add board mounting pads
        with GridLocations(
            x_spacing=pad_spacingX, y_spacing=pad_spacingY, x_count=2, y_count=2
        ):
            Circle(radius=pad_diameter / 2, mode = Mode.ADD)
            offset(amount=wall)
            Circle(radius=pad_hole_diam / 2, mode = Mode.SUBTRACT)
            offset(amount=0)            
    extrude(amount=pad_height)

with BuildPart() as boxLid:
    lid_location = boxLid.location
    lid_location.position = (0, 0, 0)
    lid_location.orientation = (0, 0, 0)
    with BuildSketch(Plane.XY.offset(35)) as plan:
        Rectangle(card_width + 2 * wall, card_length + 2 * wall)
        fillet(plan.vertices(), radius=card_width / 15)
    extrude(amount=wall)
    with BuildSketch(boxLid.faces().sort_by(Axis.Z)[-1]) as walls:
        add(plan.sketch)
        offset(plan.sketch, amount=-0.1 - wall / 2, mode=Mode.SUBTRACT)
    extrude(amount=-wall - height /2)
    with BuildSketch(boxLid.faces().sort_by(Axis.Y)[-1]): # add a hole for the USB lead
        with Locations((-2, 3.8)): # (x,z())
              RectangleRounded(13,7,1.5)
              offset(amount=0 )
    extrude(amount=10, both=True, mode=Mode.SUBTRACT)    
    topf = boxLid.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(topf.rotate(Axis.Z,180)) as lidText:
        with Locations((0,-5)):
            Text("Tank Temp.", font_size=fontsz, align=(Align.CENTER, Align.MAX))
    extrude(amount=-fontht, mode=Mode.SUBTRACT)
    with BuildSketch(topf.rotate(Axis.Z,180)) as lidText2:
        Text("Tank Level", font_size=fontsz, align=(Align.CENTER, Align.MIN))
    extrude(amount=-fontht, mode=Mode.SUBTRACT)      
    
box_builder.label = "Box"
boxLid.label = "Lid"
boxLid.color = Color = "Red"
box_assembly = Compound(label="assembly", children=[box_builder.part,boxLid.part.moved(Location((0, 0, 0)))])
show_object(box_assembly)
# show_object(box_builder.part, "box_builder")
# show_object(boxLid, "box_lid")
#export_step(box_assembly, "box_assembly.step")
export_step(box_builder.part, "box_builderPwrH4.step")
