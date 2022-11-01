# trace generated using paraview version 5.7.0
#
# To ensure correct image size when batch processing, please search
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

renderView1 = GetActiveViewOrCreate('RenderView')
HideAll(renderView1)


# VARIABLES #
caseFoamName = 'P23_str_u50_ca0_pa0_pp0_rv21_ANSA_casobase'
preTitle = ''
############



# find source
caseFoam = FindSource(caseFoamName)

# Properties modified on caseFoam
caseFoam.MeshRegions = ['RA', 'RA_disco', 'RA_patch_no_layers', 'RA_pinza', 'RP', 'RP_disco', 'RP_patch_no_layers', 'RP_pinza', 'airbox', 'carena_2021', 'casco', 'catena', 'forcella', 'forcellone', 'internalMesh', 'link', 'motore', 'parafango_ant_petrol_2021', 'parafango_post_petrol_2021', 'pedane', 'pilota', 'radiatori', 'scarico', 'sella', 'telaio']

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Extract Block'
extractBlock1 = ExtractBlock(Input=caseFoam)

# Properties modified on extractBlock1
extractBlock1.BlockIndices = [2]

# show data in view
extractBlock1Display = Show(extractBlock1, renderView1)

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')

# trace defaults for the display properties.
extractBlock1Display.Representation = 'Surface'
extractBlock1Display.ColorArrayName = ['POINTS', 'p']
extractBlock1Display.LookupTable = pLUT
extractBlock1Display.OSPRayScaleArray = 'p'
extractBlock1Display.OSPRayScaleFunction = 'PiecewiseFunction'
extractBlock1Display.SelectOrientationVectors = 'U'
extractBlock1Display.ScaleFactor = 0.18389970660209656
extractBlock1Display.SelectScaleArray = 'p'
extractBlock1Display.GlyphType = 'Arrow'
extractBlock1Display.GlyphTableIndexArray = 'p'
extractBlock1Display.GaussianRadius = 0.009194985330104828
extractBlock1Display.SetScaleArray = ['POINTS', 'p']
extractBlock1Display.ScaleTransferFunction = 'PiecewiseFunction'
extractBlock1Display.OpacityArray = ['POINTS', 'p']
extractBlock1Display.OpacityTransferFunction = 'PiecewiseFunction'
extractBlock1Display.DataAxesGrid = 'GridAxesRepresentation'
extractBlock1Display.PolarAxes = 'PolarAxesRepresentation'
extractBlock1Display.SelectInputVectors = ['POINTS', 'U']
extractBlock1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
extractBlock1Display.ScaleTransferFunction.Points = [-11332.2900390625, 0.0, 0.5, 0.0, 1320.12744140625, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
extractBlock1Display.OpacityTransferFunction.Points = [-11332.2900390625, 0.0, 0.5, 0.0, 1320.12744140625, 1.0, 0.5, 0.0]

# get the material library
materialLibrary1 = GetMaterialLibrary()

# hide data in view
Hide(caseFoam, renderView1)

# set scalar coloring
ColorBy(extractBlock1Display, ('POINTS', 'p'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
extractBlock1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
extractBlock1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'pMean'
pMeanLUT = GetColorTransferFunction('p')
pMeanLUT.RGBPoints = [-12714.58984375, 0.231373, 0.298039, 0.752941, -5715.7698974609375, 0.865003, 0.865003, 0.865003, 1283.050048828125, 0.705882, 0.0156863, 0.14902]
pMeanLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'pMean'
pMeanPWF = GetOpacityTransferFunction('p')
pMeanPWF.Points = [-12714.58984375, 0.0, 0.5, 0.0, 1283.050048828125, 1.0, 0.5, 0.0]
pMeanPWF.ScalarRangeInitialized = 1

# Rescale transfer function
pMeanLUT.RescaleTransferFunction(-1800.0, 1800.0)

# Rescale transfer function
pMeanPWF.RescaleTransferFunction(-1800.0, 1800.0)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
pMeanLUT.ApplyPreset('Cool to Warm (Extended)', True)

# get color legend/bar for pMeanLUT in view renderView1
pMeanLUTColorBar = GetScalarBar(pMeanLUT, renderView1)
pMeanLUTColorBar.Title = 'Pressure Difference'
pMeanLUTColorBar.ComponentTitle = ''

# Properties modified on pMeanLUTColorBar
pMeanLUTColorBar.AutoOrient = 0
pMeanLUTColorBar.Orientation = 'Horizontal'
pMeanLUTColorBar.WindowLocation = 'LowerCenter'
pMeanLUTColorBar.Title = 'Pressure Difference'
pMeanLUTColorBar.ScalarBarLength = 0.7

renderView1.Update()

# Properties modified on pLUT
pMeanLUT.NumberOfTableValues = 1024


# get layout
layout1 = GetLayout()

#ISOMETRIC
# current camera placement for renderView1
renderView1.CameraPosition = [3.26, 3.66, 1.4]
renderView1.CameraFocalPoint = [0.62, 0, 0.65]
renderView1.CameraViewUp = [0.1697329102547218, 0.12908074044342488, 0.9769999496535503]
renderView1.CameraViewAngle = 23.111
renderView1.CameraParallelScale = 1.169

# update the view to ensure updated data information
renderView1.Update()

# save screenshot
fileName = 'C:/Users/PMF/Desktop/slices/'+preTitle +'_' +caseFoamName+'_pressure_aIso.png'
SaveScreenshot(fileName, layout1, ImageResolution=[1549, 1548], OverrideColorPalette='WhiteBackground')


#VERTICAL - y
renderView1.ResetCamera()
renderView1.CameraPosition = [0.62, 4.5, 0.65]
renderView1.CameraFocalPoint = [0.62, 0.0, 0.6]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraViewAngle = 30.00
renderView1.CameraParallelScale = 1.169
renderView1.Update()
fileName = 'C:/Users/PMF/Desktop/slices/'+preTitle +'_' +caseFoamName+'_pressure_side.png'
SaveScreenshot(fileName, layout1, ImageResolution=[1549, 1548], OverrideColorPalette='WhiteBackground')

#FRONT - x
renderView1.CameraPosition = [5.13, 0.0, 0.65]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.6]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 1.169
renderView1.Update()
fileName = 'C:/Users/PMF/Desktop/slices/'+preTitle +'_' +caseFoamName+'_pressure_front.png'
SaveScreenshot(fileName, layout1, ImageResolution=[1549, 1548], OverrideColorPalette='WhiteBackground')

#UPPER - z
renderView1.CameraPosition = [0.62, 0.0, 5.16]
renderView1.CameraFocalPoint = [0.62, 0.0, 0.0]
renderView1.CameraViewUp = [0.0, 1.0, 0.0]
renderView1.CameraParallelScale = 1.169
renderView1.Update()
fileName = 'C:/Users/PMF/Desktop/slices/'+preTitle +caseFoamName+'_pressure_upper.png'
SaveScreenshot(fileName, layout1, ImageResolution=[1549, 1548], OverrideColorPalette='WhiteBackground')
