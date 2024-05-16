# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Wetness Index
#
#   Try to quantify topographic wetness for salamander connectivity
#
#   **Currently setup for windows OS**
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

# import tools from WBT module

from WBT.whitebox_tools import WhiteboxTools
import os as os

# declare a name for the tools

wbt = WhiteboxTools()

# Set your working directory - where you will read and write files. 
# NOTE: You will need to customize the path name below. 

work =  r"G:\Shared drives\GEOG0352-S24"

wbt.work_dir = work

# Declare a director for our outputs  

out = work + r"\atakoudes\vernal_pools\outputs\02_Least_Cost"

# ------------------------------------------------------------------------------
# 0. Resample the exports from EE so they lineup with Wetness Index
#    Whitebox requires that all layers have the exact same extent and resolution
# ------------------------------------------------------------------------------

wbt.resample(
    inputs = work + r"\atakoudes\vernal_pools\inputs\breeding_habitat_clipped.tif", 
    output = out + r"\_01_resample.tif", 
    cell_size=None, 
    base= work + r"\atakoudes\vernal_pools\outputs\01_Wetness_Index\_05_wetness.tif", 
    method="nn"
)

wbt.resample(
    inputs = work + r"\atakoudes\vernal_pools\inputs\stream_image_clipped.tif",
    output = out + r"\_02_resample.tif", 
    cell_size=None, 
    base= work + r"\atakoudes\vernal_pools\outputs\01_Wetness_Index\_05_wetness.tif", 
    method="nn"
)


# ------------------------------------------------------------------------------
# 1. Simple Raster Math to Isolate Wet Corridors
#    Also masks out any possible corridors inside a stream area since these
#    appear as odd grids.
# ------------------------------------------------------------------------------

#Wetness index > 8

wbt.greater_than(
    input1 = work + r"\atakoudes\vernal_pools\outputs\01_Wetness_Index\_05_wetness.tif", 
    input2 = 8, 
    output = out + r"\_10_reclass.tif", 
    incl_equals=False
)

# Masking out area-type streams since they are not habitat and create odd artifacts

wbt.add(
    input1 = out + r"\_10_reclass.tif", 
    input2 = out + r"\_02_resample.tif", 
    output = out + r"\_11_add.tif"
)

wbt.equal_to(
    input1 = out + r"\_11_add.tif", 
    input2 = 1, 
    output = out + r"\_12_equal_to.tif"
)

wbt.set_nodata_value(
    i = out + r"\_12_equal_to.tif",
    output = out + r"\_13_no_data.tif", 
    back_value=0
)

# ------------------------------------------------------------------------------
# 2. Cost Distance
# ------------------------------------------------------------------------------

wbt.cost_distance(
    source = out + r"\_01_resample.tif", 
    cost = out + r"\_13_no_data.tif",
    out_accum = out + r"\_20_cost_distance.tif", 
    out_backlink = out + r"\_20_back_link.tif", 
)

# Equals 140 meters distance (70 cm resolution)

wbt.less_than(
    input1 = out + r"\_20_cost_distance.tif", 
    input2 = 200, 
    output = out + r"\_21_cost_threshold.tif", 
    incl_equals=False
)

# Extract possible migration paths

wbt.extract_streams(
    flow_accum = out + r"\_21_cost_threshold.tif", 
    output = out + r"\_22_extract_streams.tif", 
    threshold = 0, 
    zero_background=False
)

# Create a vector of the migration lines

wbt.raster_streams_to_vector(
    streams = out + r"\_22_extract_streams.tif", 
    d8_pntr = work + r"\atakoudes\vernal_pools\outputs\01_Wetness_Index\_02_rh08_pointer.tif", 
    output = out + r"\_23_stream_lines.shp", 
    esri_pntr=False
)