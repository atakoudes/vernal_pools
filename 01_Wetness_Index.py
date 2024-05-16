# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Wetness Index
#
#   Identifying possible salamander migration routes
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

out = work + r"\atakoudes\vernal_pools\outputs\01_Wetness_Index"

# Declare name for DEM

dem = work + r"\atakoudes\vernal_pools\inputs\region_dem.tif"

# ------------------------------------------------------------------------------
# 1. Breach Depressions
# ------------------------------------------------------------------------------

wbt.breach_depressions_least_cost(
    dem = dem, 
    output = out + r"\_01_breach_depressions11.tif", 
    dist = 10, 
    max_cost=None, 
    min_dist=True, 
    flat_increment=None, 
    fill=True
)

# ------------------------------------------------------------------------------
# 2. RH08 Pointer
# ------------------------------------------------------------------------------

wbt.rho8_pointer(
    dem = out + "_01_breach_depressions10.tif", 
    output = out + "_02_rh08_pointer.tif", 
    esri_pntr=False
)

# ------------------------------------------------------------------------------
# 3. RH08 Flow Accumulation
# Generates flow accumulation
# ------------------------------------------------------------------------------

wbt.rho8_flow_accumulation(
    i = out + "_02_rh08_pointer.tif", 
    output = out + "_03_flow_accumulation.tif", 
    out_type="specific contributing area", 
    log=False, 
    clip=False, 
    pntr=True,     #Using an rh08 pointer as input
    esri_pntr=False
)

# ------------------------------------------------------------------------------
# 4. Slope
# ------------------------------------------------------------------------------

wbt.slope(
    dem = dem, 
    output = out + "_04_slope.tif", 
    zfactor=None, 
    units="degrees"
)

# ------------------------------------------------------------------------------
# 5. Wetness Index
# ------------------------------------------------------------------------------

wbt.wetness_index(
    sca = out + r"\_03_flow_accumulation.tif", 
    slope = out + r"\_04_slope.tif", 
    output = out + r"\_05_wetness.tif"
)