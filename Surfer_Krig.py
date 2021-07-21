import subprocess
import os
import sys

import numpy as np
import pandas as pd
import tkinter
from tkinter import filedialog
import geoprocess as gp
from pyproj import Transformer


print('Select survey points file to grid .csv')
tkinter.Tk().withdraw()
InFile = filedialog.askopenfilename(title="Select Survey Points file (.csv):")


columnNames = ['Location_Code', 'LineNumber', 'SurveyNumber', 'Latitude',
               'Longitude', 'Easting', 'Northing', 'FRF_X', 'FRF_Y', 'Elevation',
               'Ellipsoid', 'Date', 'UTC_time', 'hypack_time']

#InFile = "C:\surveyGrid\incoming\FRF_20200721_1188_FRF_NAVD88_LARC_GPS_UTC_v20200722.csv"

sdata = pd.read_csv(InFile, names=columnNames)

lines = np.unique(sdata['LineNumber'])
lines_diff = np.diff(lines)


if np.any(lines_diff > 149):
    print('Max spacing between survey lines exceeded - will not grid data')
    sys.exit()



xarr=(50, 62, 74, 86, 98, 110, 122, 134, 146,
  158, 170, 182, 194, 206, 218, 230, 242, 254,
  266, 278, 290, 302, 314, 326, 338, 350, 362,
  374, 386, 398, 410, 422, 434, 446, 458, 470,
  482, 494, 506, 518, 530, 542, 554, 566, 578,
  590, 602, 614, 626, 638, 650, 662, 674, 686,
  698, 710, 722, 734, 746, 758, 770, 782, 794,
  806, 818, 830, 842, 854, 866, 878, 890, 902,
  914, 926, 938, 950)

yarr = ( -100,   -76,   -52,   -28,    -4,    20,    44,    68,
           92,   116,   140,   164,   188,   212,   236,   260,
          284,   308,   332,   356,   380,   404,   428,   452,
          476,   500,   524,   548,   572,   596,   620,   644,
          668,   692,   716,   740,   764,   788,   812,   836,
          860,   884,   908,   932,   956,   980,  1004,  1028,
         1052,  1076,  1100)

xs_max = np.max(xarr)
xs_min = np.min(xarr)

ls_max = np.max(yarr)
ls_min = np.min(yarr)

#if np.max(sdata['FRF_X']) < np.max(xarr):
    #xs_max = np.max(sdata['FRF_X'])

xsSpace = 12
lsSpace = 24
ncol = int((xs_max - xs_min)/xsSpace) + 1
nrow = int((ls_max - ls_min)/lsSpace) + 1

srfdat = {'InFile': [os.path.basename(InFile)], 'ls_min': [ls_min], 'ls_max': [ls_max],
          'xs_min': [xs_min], 'xs_max': [xs_max], 'ncol': [ncol], 'nrow': [nrow], 'dirName': [os.path.dirname(InFile) + '/']}

srf_df = pd.DataFrame(srfdat)

if os.path.isdir('C:/Scratch'):
    print('Scratch Directory Exists')
else:
    os.mkdir('C:/Scratch')
    print('making Scratch Directory')


datFile = "C:/Scratch/InputFiles.dat"
srf_df.to_csv(datFile, header=False, index=False)

print('Gridding Data')

# dos command that runs the surfer scripter
cmd = "C:/Temp/Scripter/Scripter.exe -x C:/Surfer_Krig/ContourGrid_ascii.BAS"
subprocess.call(cmd)


# convert FRF coords to lat long
FRFdf = pd.read_csv(InFile+'_grid.txt', names=['FRF_X', 'FRF_Y', 'Elevation'], delimiter=' ')
FRF_latlong = gp.FRF2ncsp(FRFdf['FRF_X'], FRFdf['FRF_Y'])

spX = FRF_latlong['StateplaneE']
spX = np.array(spX)

spY = FRF_latlong['StateplaneN']
spY = np.array(spY)

#setup transformer going from stateplane to geographic using EPSG codes
transformer = Transformer.from_crs("EPSG:3358", "EPSG:4269")
latlong = transformer.transform(spX, spY)


grid = {}
grid['lon'] = latlong[1]
grid['lat'] = latlong[0]
grid['elevation'] = FRFdf['Elevation']
grid['FRF_X'] = FRFdf['FRF_X']
grid['FRF_Y'] = FRFdf['FRF_Y']

gridDF = pd.DataFrame(grid)
# writeout to csv file
gridDF.to_csv(InFile[:-4] + '_grid_latlon.txt', index=False, header=False)
os.remove(InFile[:-4] + '.csv_grid.txt')
print('complete')