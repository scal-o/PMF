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
dim_array = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.775, 0.80, 0.90, 1.00, 1.10, 1.20, 1.30, 1.40, 1.50]


field = 'U' # 'UMean', 'U'
colorBarTitle = 'Velocity'
colorBarSubTitle = '(m/s)'
#############

# find Source
caseFoam = FindSource(caseFoamName)

# set active source
SetActiveSource(caseFoam)

# create a new 'Slice'
slice3 = Slice(Input=caseFoam)
slice3.SliceType = 'Plane'
slice3.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice3.SliceType.Origin = [4.010000228881836, 0.0, 3.009999990463257]

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice3.SliceType)

# Properties modified on slice3.SliceType
slice3.SliceType.Normal = [0.0, 0.0, 1.0]

# show data in view
slice3Display = Show(slice3, renderView1)

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')
pLUT.RGBPoints = [-9241.080078125, 0.02, 0.3813, 0.9981, -8988.57840983073, 0.02000006, 0.424267768, 0.96906969, -8736.076741536457, 0.02, 0.467233763, 0.940033043, -8483.575073242188, 0.02, 0.5102, 0.911, -8231.073404947918, 0.02000006, 0.546401494, 0.872669438, -7978.571736653646, 0.02, 0.582600362, 0.83433295, -7726.070068359375, 0.02, 0.6188, 0.796, -7473.5684000651045, 0.02000006, 0.652535156, 0.749802434, -7221.066731770834, 0.02, 0.686267004, 0.703599538, -6968.565063476563, 0.02, 0.72, 0.6574, -6716.063395182291, 0.02000006, 0.757035456, 0.603735359, -6463.561726888021, 0.02, 0.794067037, 0.55006613, -6211.060058593749, 0.02, 0.8311, 0.4964, -5958.558390299479, 0.021354336738172372, 0.8645368555261631, 0.4285579460761159, -5706.056722005209, 0.023312914349117714, 0.897999359924484, 0.36073871343115577, -5453.5550537109375, 0.015976108242848862, 0.9310479513349017, 0.2925631815088092, -5201.053385416667, 0.27421074700988196, 0.952562960995083, 0.15356836602739213, -4948.5517171223955, 0.4933546281681699, 0.9619038625309482, 0.11119493614749336, -4696.050048828126, 0.6439, 0.9773, 0.0469, -4443.548380533854, 0.762401813, 0.984669591, 0.034600153, -4191.046712239584, 0.880901185, 0.992033407, 0.022299877, -3938.5450439453125, 0.9995285432627147, 0.9995193706781492, 0.0134884641450013, -3686.043375651041, 0.999402998, 0.955036376, 0.079066628, -3433.5417073567705, 0.9994, 0.910666223, 0.148134024, -3181.0400390625, 0.9994, 0.8663, 0.2172, -2928.5383707682295, 0.999269665, 0.818035981, 0.217200652, -2676.036702473958, 0.999133332, 0.769766184, 0.2172, -2423.5350341796866, 0.999, 0.7215, 0.2172, -2171.033365885417, 0.99913633, 0.673435546, 0.217200652, -1918.5316975911455, 0.999266668, 0.625366186, 0.2172, -1666.030029296875, 0.9994, 0.5773, 0.2172, -1413.5283610026036, 0.999402998, 0.521068455, 0.217200652, -1161.026692708334, 0.9994, 0.464832771, 0.2172, -908.5250244140643, 0.9994, 0.4086, 0.2172, -656.0233561197911, 0.9947599917687346, 0.33177297300202935, 0.2112309638520206, -403.5216878255196, 0.9867129505479589, 0.2595183410914934, 0.19012239549291934, -151.02001953125182, 0.9912458875646419, 0.14799417507952672, 0.21078892136920357, 101.48164876302144, 0.949903037, 0.116867171, 0.252900603, 353.9833170572929, 0.903199533, 0.078432949, 0.291800389, 606.4849853515625, 0.8565, 0.04, 0.3307, 858.9866536458321, 0.798902627, 0.04333345, 0.358434298, 1111.4883219401036, 0.741299424, 0.0466667, 0.386166944, 1363.989990234375, 0.6837, 0.05, 0.4139]
pLUT.ColorSpace = 'RGB'
pLUT.NanColor = [1.0, 0.0, 0.0]
pLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
slice3Display.Representation = 'Surface'
slice3Display.ColorArrayName = ['POINTS', 'p']
slice3Display.LookupTable = pLUT
slice3Display.OSPRayScaleArray = 'p'
slice3Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice3Display.SelectOrientationVectors = 'U'
slice3Display.ScaleFactor = 2.0020000457763674
slice3Display.SelectScaleArray = 'p'
slice3Display.GlyphType = 'Arrow'
slice3Display.GlyphTableIndexArray = 'p'
slice3Display.GaussianRadius = 0.10010000228881837
slice3Display.SetScaleArray = ['POINTS', 'p']
slice3Display.ScaleTransferFunction = 'PiecewiseFunction'
slice3Display.OpacityArray = ['POINTS', 'p']
slice3Display.OpacityTransferFunction = 'PiecewiseFunction'
slice3Display.DataAxesGrid = 'GridAxesRepresentation'
slice3Display.PolarAxes = 'PolarAxesRepresentation'
slice3Display.SelectInputVectors = ['POINTS', 'U']
slice3Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
slice3Display.ScaleTransferFunction.Points = [-1182.015380859375, 0.0, 0.5, 0.0, 1286.77001953125, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
slice3Display.OpacityTransferFunction.Points = [-1182.015380859375, 0.0, 0.5, 0.0, 1286.77001953125, 1.0, 0.5, 0.0]

# hide data in view
Hide(caseFoam, renderView1)

# show color bar/color legend
slice3Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get opacity transfer function/opacity map for 'p'
pPWF = GetOpacityTransferFunction('p')
pPWF.Points = [-9241.080078125, 0.0, 0.5, 0.0, 1363.989990234375, 1.0, 0.5, 0.0]
pPWF.ScalarRangeInitialized = 1

# set scalar coloring
ColorBy(slice3Display, ('POINTS', field, 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice3Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice3Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'UMean'
uMeanLUT = GetColorTransferFunction(field)
uMeanLUT.AutomaticRescaleRangeMode = 'Never'
uMeanLUT.RGBPoints = [0.0, 0.267004, 0.004874, 0.329415, 0.27454, 0.26851, 0.009605, 0.335427, 0.54901, 0.269944, 0.014625, 0.341379, 0.82355, 0.271305, 0.019942, 0.347269, 1.09802, 0.272594, 0.025563, 0.353093, 1.37256, 0.273809, 0.031497, 0.358853, 1.64703, 0.274952, 0.037752, 0.364543, 1.92157, 0.276022, 0.044167, 0.370164, 2.19611, 0.277018, 0.050344, 0.375715, 2.47058, 0.277941, 0.056324, 0.381191, 2.74512, 0.278791, 0.062145, 0.386592, 3.01959, 0.279566, 0.067836, 0.391917, 3.2941299999999996, 0.280267, 0.073417, 0.397163, 3.5686000000000004, 0.280894, 0.078907, 0.402329, 3.84314, 0.281446, 0.08432, 0.407414, 4.11768, 0.281924, 0.089666, 0.412415, 4.39215, 0.282327, 0.094955, 0.417331, 4.66669, 0.282656, 0.100196, 0.42216, 4.94116, 0.28291, 0.105393, 0.426902, 5.215700000000001, 0.283091, 0.110553, 0.431554, 5.49017, 0.283197, 0.11568, 0.436115, 5.764710000000001, 0.283229, 0.120777, 0.440584, 6.03925, 0.283187, 0.125848, 0.44496, 6.31372, 0.283072, 0.130895, 0.449241, 6.588259999999999, 0.282884, 0.13592, 0.453427, 6.86273, 0.282623, 0.140926, 0.457517, 7.13727, 0.28229, 0.145912, 0.46151, 7.41174, 0.281887, 0.150881, 0.465405, 7.68628, 0.281412, 0.155834, 0.469201, 7.960750000000001, 0.280868, 0.160771, 0.472899, 8.23529, 0.280255, 0.165693, 0.476498, 8.50983, 0.279574, 0.170599, 0.479997, 8.7843, 0.278826, 0.17549, 0.483397, 9.05884, 0.278012, 0.180367, 0.486697, 9.33331, 0.277134, 0.185228, 0.489898, 9.60785, 0.276194, 0.190074, 0.493001, 9.88232, 0.275191, 0.194905, 0.496005, 10.15686, 0.274128, 0.199721, 0.498911, 10.431400000000002, 0.273006, 0.20452, 0.501721, 10.705869999999999, 0.271828, 0.209303, 0.504434, 10.980410000000001, 0.270595, 0.214069, 0.507052, 11.25488, 0.269308, 0.218818, 0.509577, 11.529420000000002, 0.267968, 0.223549, 0.512008, 11.803889999999999, 0.26658, 0.228262, 0.514349, 12.07843, 0.265145, 0.232956, 0.516599, 12.35297, 0.263663, 0.237631, 0.518762, 12.62744, 0.262138, 0.242286, 0.520837, 12.90198, 0.260571, 0.246922, 0.522828, 13.17645, 0.258965, 0.251537, 0.524736, 13.45099, 0.257322, 0.25613, 0.526563, 13.72546, 0.255645, 0.260703, 0.528312, 14.0, 0.253935, 0.265254, 0.529983, 14.27454, 0.252194, 0.269783, 0.531579, 14.549009999999999, 0.250425, 0.27429, 0.533103, 14.823550000000001, 0.248629, 0.278775, 0.534556, 15.09802, 0.246811, 0.283237, 0.535941, 15.37256, 0.244972, 0.287675, 0.53726, 15.64703, 0.243113, 0.292092, 0.538516, 15.92157, 0.241237, 0.296485, 0.539709, 16.19611, 0.239346, 0.300855, 0.540844, 16.47058, 0.237441, 0.305202, 0.541921, 16.74512, 0.235526, 0.309527, 0.542944, 17.01959, 0.233603, 0.313828, 0.543914, 17.29413, 0.231674, 0.318106, 0.544834, 17.5686, 0.229739, 0.322361, 0.545706, 17.843140000000002, 0.227802, 0.326594, 0.546532, 18.11768, 0.225863, 0.330805, 0.547314, 18.39215, 0.223925, 0.334994, 0.548053, 18.66669, 0.221989, 0.339161, 0.548752, 18.94116, 0.220057, 0.343307, 0.549413, 19.2157, 0.21813, 0.347432, 0.550038, 19.49017, 0.21621, 0.351535, 0.550627, 19.76471, 0.214298, 0.355619, 0.551184, 20.03925, 0.212395, 0.359683, 0.55171, 20.31372, 0.210503, 0.363727, 0.552206, 20.58826, 0.208623, 0.367752, 0.552675, 20.86273, 0.206756, 0.371758, 0.553117, 21.137269999999997, 0.204903, 0.375746, 0.553533, 21.411739999999998, 0.203063, 0.379716, 0.553925, 21.68628, 0.201239, 0.38367, 0.554294, 21.960749999999997, 0.19943, 0.387607, 0.554642, 22.23529, 0.197636, 0.391528, 0.554969, 22.50983, 0.19586, 0.395433, 0.555276, 22.784299999999995, 0.1941, 0.399323, 0.555565, 23.058840000000004, 0.192357, 0.403199, 0.555836, 23.33331, 0.190631, 0.407061, 0.556089, 23.607850000000003, 0.188923, 0.41091, 0.556326, 23.88232, 0.187231, 0.414746, 0.556547, 24.15686, 0.185556, 0.41857, 0.556753, 24.4314, 0.183898, 0.422383, 0.556944, 24.70587, 0.182256, 0.426184, 0.55712, 24.98041, 0.180629, 0.429975, 0.557282, 25.25488, 0.179019, 0.433756, 0.55743, 25.52942, 0.177423, 0.437527, 0.557565, 25.80389, 0.175841, 0.44129, 0.557685, 26.07843, 0.174274, 0.445044, 0.557792, 26.35297, 0.172719, 0.448791, 0.557885, 26.62744, 0.171176, 0.45253, 0.557965, 26.90198, 0.169646, 0.456262, 0.55803, 27.176449999999996, 0.168126, 0.459988, 0.558082, 27.450989999999997, 0.166617, 0.463708, 0.558119, 27.725459999999998, 0.165117, 0.467423, 0.558141, 28.0, 0.163625, 0.471133, 0.558148, 28.274540000000002, 0.162142, 0.474838, 0.55814, 28.54901, 0.160665, 0.47854, 0.558115, 28.82355, 0.159194, 0.482237, 0.558073, 29.098019999999998, 0.157729, 0.485932, 0.558013, 29.372559999999996, 0.15627, 0.489624, 0.557936, 29.64703, 0.154815, 0.493313, 0.55784, 29.921570000000003, 0.153364, 0.497, 0.557724, 30.19611, 0.151918, 0.500685, 0.557587, 30.47058, 0.150476, 0.504369, 0.55743, 30.74512, 0.149039, 0.508051, 0.55725, 31.01959, 0.147607, 0.511733, 0.557049, 31.29413, 0.14618, 0.515413, 0.556823, 31.568600000000004, 0.144759, 0.519093, 0.556572, 31.84314, 0.143343, 0.522773, 0.556295, 32.11768, 0.141935, 0.526453, 0.555991, 32.39215, 0.140536, 0.530132, 0.555659, 32.66669, 0.139147, 0.533812, 0.555298, 32.94116, 0.13777, 0.537492, 0.554906, 33.2157, 0.136408, 0.541173, 0.554483, 33.49017, 0.135066, 0.544853, 0.554029, 33.764709999999994, 0.133743, 0.548535, 0.553541, 34.039249999999996, 0.132444, 0.552216, 0.553018, 34.31372, 0.131172, 0.555899, 0.552459, 34.58826, 0.129933, 0.559582, 0.551864, 34.86273, 0.128729, 0.563265, 0.551229, 35.13727, 0.127568, 0.566949, 0.550556, 35.41174, 0.126453, 0.570633, 0.549841, 35.686280000000004, 0.125394, 0.574318, 0.549086, 35.96075, 0.124395, 0.578002, 0.548287, 36.23529, 0.123463, 0.581687, 0.547445, 36.509829999999994, 0.122606, 0.585371, 0.546557, 36.7843, 0.121831, 0.589055, 0.545623, 37.05884, 0.121148, 0.592739, 0.544641, 37.33331, 0.120565, 0.596422, 0.543611, 37.60785, 0.120092, 0.600104, 0.54253, 37.88232, 0.119738, 0.603785, 0.5414, 38.156859999999995, 0.119512, 0.607464, 0.540218, 38.4314, 0.119423, 0.611141, 0.538982, 38.705870000000004, 0.119483, 0.614817, 0.537692, 38.98041, 0.119699, 0.61849, 0.536347, 39.25488, 0.120081, 0.622161, 0.534946, 39.52942, 0.120638, 0.625828, 0.533488, 39.80389, 0.12138, 0.629492, 0.531973, 40.07843, 0.122312, 0.633153, 0.530398, 40.35297, 0.123444, 0.636809, 0.528763, 40.62744, 0.12478, 0.640461, 0.527068, 40.90198, 0.126326, 0.644107, 0.525311, 41.176449999999996, 0.128087, 0.647749, 0.523491, 41.450990000000004, 0.130067, 0.651384, 0.521608, 41.72546, 0.132268, 0.655014, 0.519661, 42.0, 0.134692, 0.658636, 0.517649, 42.274539999999995, 0.137339, 0.662252, 0.515571, 42.54901, 0.14021, 0.665859, 0.513427, 42.82355, 0.143303, 0.669459, 0.511215, 43.09802, 0.146616, 0.67305, 0.508936, 43.37256, 0.150148, 0.676631, 0.506589, 43.64703000000001, 0.153894, 0.680203, 0.504172, 43.92157000000001, 0.157851, 0.683765, 0.501686, 44.19611, 0.162016, 0.687316, 0.499129, 44.47058, 0.166383, 0.690856, 0.496502, 44.74512, 0.170948, 0.694384, 0.493803, 45.019589999999994, 0.175707, 0.6979, 0.491033, 45.29413, 0.180653, 0.701402, 0.488189, 45.56859999999999, 0.185783, 0.704891, 0.485273, 45.84313999999999, 0.19109, 0.708366, 0.482284, 46.11768000000001, 0.196571, 0.711827, 0.479221, 46.39215, 0.202219, 0.715272, 0.476084, 46.66669, 0.20803, 0.718701, 0.472873, 46.941159999999996, 0.214, 0.722114, 0.469588, 47.215700000000005, 0.220124, 0.725509, 0.466226, 47.49017, 0.226397, 0.728888, 0.462789, 47.764709999999994, 0.232815, 0.732247, 0.459277, 48.03924999999999, 0.239374, 0.735588, 0.455688, 48.31372, 0.24607, 0.73891, 0.452024, 48.58826, 0.252899, 0.742211, 0.448284, 48.86273, 0.259857, 0.745492, 0.444467, 49.137269999999994, 0.266941, 0.748751, 0.440573, 49.41174, 0.274149, 0.751988, 0.436601, 49.68628, 0.281477, 0.755203, 0.432552, 49.960750000000004, 0.288921, 0.758394, 0.428426, 50.23529, 0.296479, 0.761561, 0.424223, 50.50983, 0.304148, 0.764704, 0.419943, 50.784299999999995, 0.311925, 0.767822, 0.415586, 51.05884, 0.319809, 0.770914, 0.411152, 51.33331, 0.327796, 0.77398, 0.40664, 51.60785, 0.335885, 0.777018, 0.402049, 51.88231999999999, 0.344074, 0.780029, 0.397381, 52.15686, 0.35236, 0.783011, 0.392636, 52.431400000000004, 0.360741, 0.785964, 0.387814, 52.70587, 0.369214, 0.788888, 0.382914, 52.98041, 0.377779, 0.791781, 0.377939, 53.25488, 0.386433, 0.794644, 0.372886, 53.52942, 0.395174, 0.797475, 0.367757, 53.803889999999996, 0.404001, 0.800275, 0.362552, 54.078430000000004, 0.412913, 0.803041, 0.357269, 54.35297, 0.421908, 0.805774, 0.35191, 54.62744000000001, 0.430983, 0.808473, 0.346476, 54.901979999999995, 0.440137, 0.811138, 0.340967, 55.17645, 0.449368, 0.813768, 0.335384, 55.45099, 0.458674, 0.816363, 0.329727, 55.72546, 0.468053, 0.818921, 0.323998, 56.0, 0.477504, 0.821444, 0.318195, 56.27454, 0.487026, 0.823929, 0.312321, 56.54900999999999, 0.496615, 0.826376, 0.306377, 56.823550000000004, 0.506271, 0.828786, 0.300362, 57.09802, 0.515992, 0.831158, 0.294279, 57.37256, 0.525776, 0.833491, 0.288127, 57.647029999999994, 0.535621, 0.835785, 0.281908, 57.92157, 0.545524, 0.838039, 0.275626, 58.196110000000004, 0.555484, 0.840254, 0.269281, 58.47058, 0.565498, 0.84243, 0.262877, 58.74511999999999, 0.575563, 0.844566, 0.256415, 59.01959, 0.585678, 0.846661, 0.249897, 59.29413, 0.595839, 0.848717, 0.243329, 59.568599999999996, 0.606045, 0.850733, 0.236712, 59.843140000000005, 0.616293, 0.852709, 0.230052, 60.11768, 0.626579, 0.854645, 0.223353, 60.39215, 0.636902, 0.856542, 0.21662, 60.666689999999996, 0.647257, 0.8584, 0.209861, 60.94116, 0.657642, 0.860219, 0.203082, 61.2157, 0.668054, 0.861999, 0.196293, 61.49017, 0.678489, 0.863742, 0.189503, 61.76471000000001, 0.688944, 0.865448, 0.182725, 62.03925, 0.699415, 0.867117, 0.175971, 62.313719999999996, 0.709898, 0.868751, 0.169257, 62.58826, 0.720391, 0.87035, 0.162603, 62.86273, 0.730889, 0.871916, 0.156029, 63.13727, 0.741388, 0.873449, 0.149561, 63.41174000000001, 0.751884, 0.874951, 0.143228, 63.68628, 0.762373, 0.876424, 0.137064, 63.96075, 0.772852, 0.877868, 0.131109, 64.23529, 0.783315, 0.879285, 0.125405, 64.50983, 0.79376, 0.880678, 0.120005, 64.7843, 0.804182, 0.882046, 0.114965, 65.05884, 0.814576, 0.883393, 0.110347, 65.33330999999998, 0.82494, 0.88472, 0.106217, 65.60785, 0.83527, 0.886029, 0.102646, 65.88232, 0.845561, 0.887322, 0.099702, 66.15686, 0.85581, 0.888601, 0.097452, 66.4314, 0.866013, 0.889868, 0.095953, 66.70587, 0.876168, 0.891125, 0.09525, 66.98041, 0.886271, 0.892374, 0.095374, 67.25487999999999, 0.89632, 0.893616, 0.096335, 67.52941999999999, 0.906311, 0.894855, 0.098125, 67.80389, 0.916242, 0.896091, 0.100717, 68.07843, 0.926106, 0.89733, 0.104071, 68.35297, 0.935904, 0.89857, 0.108131, 68.62744, 0.945636, 0.899815, 0.112838, 68.90198, 0.9553, 0.901065, 0.118128, 69.17645, 0.964894, 0.902323, 0.123941, 69.45098999999999, 0.974417, 0.90359, 0.130215, 69.72546, 0.983868, 0.904867, 0.136897, 70.0, 0.993248, 0.906157, 0.143936]
uMeanLUT.NanColor = [1.0, 0.0, 0.0]
uMeanLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'UMean'
uMeanPWF = GetOpacityTransferFunction(field)
uMeanPWF.Points = [0.0, 0.0, 0.5, 0.0, 70.0, 1.0, 0.5, 0.0]
uMeanPWF.ScalarRangeInitialized = 1

# get color legend/bar for uMeanLUT in view renderView1
uMeanLUTColorBar = GetScalarBar(uMeanLUT, renderView1)
uMeanLUTColorBar.Orientation = 'Horizontal'
uMeanLUTColorBar.WindowLocation = 'AnyLocation'
uMeanLUTColorBar.Position = [0.2849350649350649, 0.013510638297872336]
uMeanLUTColorBar.Title = colorBarTitle
uMeanLUTColorBar.ComponentTitle = colorBarSubTitle
uMeanLUTColorBar.HorizontalTitle = 1
uMeanLUTColorBar.ScalarBarLength = 0.4000000000000003

# Properties modified on uMeanLUTColorBar
uMeanLUTColorBar.WindowLocation = 'LowerCenter'

# current camera placement for renderView1
renderView1.CameraPosition = [-3.0, 5.0, 3.2]
renderView1.CameraFocalPoint = [-3.0, 0.0, 0.0]
renderView1.CameraViewUp = [0.0, 1.0, 0.0]
renderView1.CameraParallelScale = 10.453
renderView1.Update()

# get color legend/bar for uMeanLUT in view renderView1
uMeanLUTColorBar = GetScalarBar(uMeanLUT, renderView1)
uMeanLUTColorBar.Orientation = 'Horizontal'
uMeanLUTColorBar.WindowLocation = 'AnyLocation'
uMeanLUTColorBar.Position = [0.2849350649350649, 0.013510638297872336]
uMeanLUTColorBar.Title = colorBarTitle
uMeanLUTColorBar.ComponentTitle = colorBarSubTitle
uMeanLUTColorBar.HorizontalTitle = 1
uMeanLUTColorBar.ScalarBarLength = 0.4000000000000003

# Properties modified on uMeanLUTColorBar
uMeanLUTColorBar.WindowLocation = 'LowerCenter'

# Hide orientation axes
renderView1.OrientationAxesVisibility = 0

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Text'
text1 = Text()
# destroy text1
Delete(text1)
del text1

# get layout
layout1 = GetLayout()

# save screenshot
SaveScreenshot('C:/Users/PMF/Desktop/slices/AAdaButtare.png', layout1, ImageResolution=[1549, 526],
    OverrideColorPalette='WhiteBackground')


k = 1

for i in dim_array:
    z_deep = 9 + float(i)
    iInCentimeters = float(i) * 100.0

    slice3.SliceType.Origin = [0.0, 0.0, float(i)]

    renderView1.CameraPosition = [-3.0, 0.0, float(z_deep)]
    renderView1.Update()

    # get layout
    layout1 = GetLayout()
    fileName = 'C:/Users/PMF/Desktop/slices/' +caseFoamName+'_'+ field +'_'+ str(int(iInCentimeters)) +'cm_sliceZ0' +str(k)+'.png'
    SaveScreenshot(fileName, layout1, ImageResolution=[1483, 526],
        OverrideColorPalette='WhiteBackground')

    renderView1.CameraPosition = [-3.0, 0.0, float(z_deep)]
    renderView1.Update()

    k = int(k) +1

