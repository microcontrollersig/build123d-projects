"""This file acts as the main module for this script."""

import traceback
import adsk.core
import adsk.fusion
# import adsk.cam

# Initialize the global variables for the Application and UserInterface objects.
app = adsk.core.Application.get()
ui  = app.userInterface

def run(_context: str):
    """This function is called by Fusion when the script is run."""

    try:
        
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        # User parameters

        ## Parameters
        user_params = design.userParameters        
        user_params.add('length', adsk.core.ValueInput.createByString("50.0mm"), 'mm', '')
        user_params.add('width', adsk.core.ValueInput.createByString("20.0mm"), 'mm', '')
        user_params.add('height', adsk.core.ValueInput.createByString("5.0mm"), 'mm', '')
        
        user_params.add('x_offset', adsk.core.ValueInput.createByString("30.0mm"), 'mm', '')
        user_params.add('y1_offset', adsk.core.ValueInput.createByString("30.0mm"), 'mm', '')
        user_params.add('y2_offset', adsk.core.ValueInput.createByString("45.0mm"), 'mm', '')

        user_params.add('spacing_small', adsk.core.ValueInput.createByString("50.0mm"), 'mm', '')
        user_params.add('spacing_large', adsk.core.ValueInput.createByString("100.0mm"), 'mm', '')

        ## Radius and diameters
        user_params.add('diameter', adsk.core.ValueInput.createByString("6.0mm"), 'mm', '')
        user_params.add('radius', adsk.core.ValueInput.createByString("diameter/2"), 'mm', '')
 

        ## Computed parameters
        user_params.add('half_length', adsk.core.ValueInput.createByString("length/2"), 'mm', '')
        user_params.add('half_width', adsk.core.ValueInput.createByString("width/2"), 'mm', '')


        # Get the root component of the active design
        rootComp = design.rootComponent
        
        # Create sketch in root component
        sketches = rootComp.sketches        

        
    except:  #pylint:disable=bare-except
        # Write the error message to the TEXT COMMANDS window.
        app.log(f'Failed:\n{traceback.format_exc()}')
