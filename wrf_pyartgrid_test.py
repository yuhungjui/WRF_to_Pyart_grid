{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 296,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/anaconda3/lib/python3.8/site-packages/ipykernel/ipkernel.py:287: DeprecationWarning: `should_run_async` will not call `transform_cell` automatically in the future. Please pass the result to `transformed_cell` argument and any exception that happen during thetransform in `preprocessing_exc_tuple` in IPython 7.17 and above.\n",
      "  and should_run_async(code)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Once deleted, variables cannot be recovered. Proceed (y/[n])? y\n"
     ]
    }
   ],
   "source": [
    "%reset"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Convert reflectivity from WRF output to Pyart grid object."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 297,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/anaconda3/lib/python3.8/site-packages/ipykernel/ipkernel.py:287: DeprecationWarning: `should_run_async` will not call `transform_cell` automatically in the future. Please pass the result to `transformed_cell` argument and any exception that happen during thetransform in `preprocessing_exc_tuple` in IPython 7.17 and above.\n",
      "  and should_run_async(code)\n"
     ]
    }
   ],
   "source": [
    "import sys\n",
    "import numpy as np\n",
    "import math\n",
    "import pyart as pyart\n",
    "from netCDF4 import Dataset\n",
    "import pandas as pd\n",
    "import xarray as xr\n",
    "from datetime import datetime \n",
    "\n",
    "import matplotlib.pyplot as plt\n",
    "from matplotlib.cm import get_cmap\n",
    "from matplotlib.colors import from_levels_and_colors\n",
    "\n",
    "import cartopy.crs as crs\n",
    "from cartopy.feature import NaturalEarthFeature\n",
    "import cartopy.feature as cfeature\n",
    "import cartopy.io.shapereader as shpreader\n",
    "\n",
    "from wrf import (getvar, vinterp, interplevel, to_np, get_cartopy, latlon_coords, vertcross,\n",
    "                 cartopy_xlim, cartopy_ylim, interpline, CoordPair)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 298,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/anaconda3/lib/python3.8/site-packages/ipykernel/ipkernel.py:287: DeprecationWarning: `should_run_async` will not call `transform_cell` automatically in the future. Please pass the result to `transformed_cell` argument and any exception that happen during thetransform in `preprocessing_exc_tuple` in IPython 7.17 and above.\n",
      "  and should_run_async(code)\n"
     ]
    }
   ],
   "source": [
    "# Get WRF output data:\n",
    "\n",
    "filename_list = ['/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_20:00:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_20:15:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_20:30:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_20:45:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_21:00:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_21:15:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_21:30:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_21:45:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_22:00:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_22:15:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_22:30:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_22:45:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_23:00:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_23:15:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_23:30:00'\n",
    "                ,'/home/krasmussen/scratch/DATA/PRECIP/June2017_meiyu/CTRL_fromJen_1km/wrfout_d01_2017-06-01_23:45:00'\n",
    "                ]\n",
    "# print(filename_list[0])\n",
    "\n",
    "file_num = 0\n",
    "\n",
    "wrf_file = Dataset(filename_list[file_num])\n",
    "# print(wrf_file)\n",
    "\n",
    "# Set output gird numner:\n",
    "output_grid_obj_num = '%03d' % file_num"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 299,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/anaconda3/lib/python3.8/site-packages/ipykernel/ipkernel.py:287: DeprecationWarning: `should_run_async` will not call `transform_cell` automatically in the future. Please pass the result to `transformed_cell` argument and any exception that happen during thetransform in `preprocessing_exc_tuple` in IPython 7.17 and above.\n",
      "  and should_run_async(code)\n"
     ]
    }
   ],
   "source": [
    "def distance(origin, destination):\n",
    "    \"\"\"\n",
    "    Calculate the Haversine distance.\n",
    "\n",
    "    Parameters\n",
    "    ----------\n",
    "    origin : tuple of float\n",
    "        (lat, long)\n",
    "    destination : tuple of float\n",
    "        (lat, long)\n",
    "\n",
    "    Returns\n",
    "    -------\n",
    "    distance_in_km : float\n",
    "\n",
    "    Examples\n",
    "    --------\n",
    "    >>> origin = (48.1372, 11.5756)  # Munich\n",
    "    >>> destination = (52.5186, 13.4083)  # Berlin\n",
    "    >>> round(distance(origin, destination), 1)\n",
    "    504.2\n",
    "    \"\"\"\n",
    "    lat1, lon1 = origin\n",
    "    lat2, lon2 = destination\n",
    "    radius = 6371  # km\n",
    "\n",
    "    dlat = math.radians(lat2 - lat1)\n",
    "    dlon = math.radians(lon2 - lon1)\n",
    "    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +\n",
    "         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *\n",
    "         math.sin(dlon / 2) * math.sin(dlon / 2))\n",
    "    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))\n",
    "    d = radius * c\n",
    "\n",
    "    return d\n",
    "\n",
    "# distance = np.frompyfunc(distance, 2, 1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 300,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/anaconda3/lib/python3.8/site-packages/ipykernel/ipkernel.py:287: DeprecationWarning: `should_run_async` will not call `transform_cell` automatically in the future. Please pass the result to `transformed_cell` argument and any exception that happen during thetransform in `preprocessing_exc_tuple` in IPython 7.17 and above.\n",
      "  and should_run_async(code)\n"
     ]
    }
   ],
   "source": [
    "# Get variable and interpolate:\n",
    "\n",
    "wrf_var = getvar(wrf_file, 'REFL_10CM')\n",
    "\n",
    "# print(dbz)\n",
    "\n",
    "# Interpolate reflectivity to pressure levels:\n",
    "\n",
    "# interp_levels = [850]\n",
    "# interp_field = vinterp(wrf_file,\n",
    "#                        field=wrf_dbz,\n",
    "#                        vert_coord='p',\n",
    "#                        interp_levels=interp_levels,\n",
    "#                        extrapolate=True,\n",
    "#                        field_type='none',\n",
    "#                        log_p=True)\n",
    "\n",
    "# Interpolate reflectivity to hieghts:\n",
    "\n",
    "interp_levels = np.linspace(0,15,31)\n",
    "# print(interp_levels)\n",
    "interp_field = vinterp(wrf_file,\n",
    "                       field=wrf_var,\n",
    "                       vert_coord='ght_msl',\n",
    "                       interp_levels=interp_levels,\n",
    "                       extrapolate=True,\n",
    "                       field_type='none'\n",
    "                      )\n",
    "# print(interp_field)\n",
    "# print(type(interp_field))\n",
    "# print(interp_field.sizes)\n",
    "# print(latlon_coords(interp_field))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 301,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(31, 600, 600)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/anaconda3/lib/python3.8/site-packages/ipykernel/ipkernel.py:287: DeprecationWarning: `should_run_async` will not call `transform_cell` automatically in the future. Please pass the result to `transformed_cell` argument and any exception that happen during thetransform in `preprocessing_exc_tuple` in IPython 7.17 and above.\n",
      "  and should_run_async(code)\n"
     ]
    }
   ],
   "source": [
    "# Reshaping data:\n",
    "\n",
    "# interp_field = interp_field.squeeze('interp_level')\n",
    "print(interp_field.shape)\n",
    "\n",
    "# interp_field_3d = interp_field.squeeze('interp_level')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 302,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/anaconda3/lib/python3.8/site-packages/ipykernel/ipkernel.py:287: DeprecationWarning: `should_run_async` will not call `transform_cell` automatically in the future. Please pass the result to `transformed_cell` argument and any exception that happen during thetransform in `preprocessing_exc_tuple` in IPython 7.17 and above.\n",
      "  and should_run_async(code)\n"
     ]
    }
   ],
   "source": [
    "# Get model output time:\n",
    "wrf_valid_datetime = interp_field['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 303,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/anaconda3/lib/python3.8/site-packages/ipykernel/ipkernel.py:287: DeprecationWarning: `should_run_async` will not call `transform_cell` automatically in the future. Please pass the result to `transformed_cell` argument and any exception that happen during thetransform in `preprocessing_exc_tuple` in IPython 7.17 and above.\n",
      "  and should_run_async(code)\n"
     ]
    }
   ],
   "source": [
    "# # Test plot:\n",
    "\n",
    "# # print(interp_field.sizes)\n",
    "# # interp_field.plot()\n",
    "\n",
    "# # Get the lat/lon coordinates\n",
    "# lats, lons = latlon_coords(interp_field)\n",
    "# # print(lats,lons)\n",
    "\n",
    "# # Get the cartopy projection object\n",
    "# dat_crs_proj = get_cartopy(interp_field)\n",
    "\n",
    "# # fig_crs = crs.LambertConformal(central_longitude=120.9, central_latitude=23.5)\n",
    "# fig_crs = dat_crs_proj\n",
    "# dat_crs = crs.PlateCarree()\n",
    "\n",
    "# # Create the figure\n",
    "# fig = plt.figure(figsize=(12,12))\n",
    "# ax1 = plt.axes(projection=fig_crs)\n",
    "\n",
    "# # ax1.set_extent([118,124,21,26.5])\n",
    "# ax1.coastlines()\n",
    "\n",
    "# # plt.rcParams['font.size'] = '18'\n",
    "\n",
    "# # Create the color table found on NWS pages.\n",
    "\n",
    "# # dbz_levels = np.arange(5., 75., 5.)\n",
    "# # dbz_rgb = np.array([[4,233,231],\n",
    "# #                     [1,159,244], [3,0,244],\n",
    "# #                     [2,253,2], [1,197,1],\n",
    "# #                     [0,142,0], [253,248,2],\n",
    "# #                     [229,188,0], [253,149,0],\n",
    "# #                     [253,0,0], [212,0,0],\n",
    "# #                     [188,0,0],[248,0,253],\n",
    "# #                     [152,84,198]], np.float32) / 255.0\n",
    "# # dbz_map, dbz_norm = from_levels_and_colors(dbz_levels, dbz_rgb, extend=\"max\")\n",
    "\n",
    "# clevs = [-5,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,85]\n",
    "# ccols = ['#ffffff','#98ffff','#009aff','#1919ff','#19ff19','#19cd19','#19A019','#fefe08','#ffcb00','#ff9c00','#fe0005','#c90200','#9d0000','#9a009d','#cf00d7','#ff00f7','#fdcafe']\n",
    "# dbz_map, dbz_norm = from_levels_and_colors(clevs, ccols)\n",
    "\n",
    "# # Make the plot:\n",
    "\n",
    "# # dbz_contours = ax.contourf(interp_field_2d.coords['XLONG'],\n",
    "# #                            interp_field_2d.coords['XLAT'],\n",
    "# #                            to_np(interp_field_2d),\n",
    "# #                            levels=dbz_levels,\n",
    "# #                            cmap=dbz_map,\n",
    "# #                            norm=dbz_norm,\n",
    "# #                            extend=\"max\")\n",
    "\n",
    "# # f1_dbz_pcolors = ax1.pcolormesh(interp_field_2d.coords['XLONG'],\n",
    "# #                                 interp_field_2d.coords['XLAT'],\n",
    "# #                                 to_np(interp_field_2d),\n",
    "# #                                 cmap=dbz_map,\n",
    "# #                                 norm=dbz_norm,\n",
    "# #                                 transform=dat_crs_proj)\n",
    "\n",
    "# plot_level = 0\n",
    "\n",
    "# f1_dbz_pcolors = ax1.pcolormesh(interp_field.coords['XLONG'],\n",
    "#                                 interp_field.coords['XLAT'],\n",
    "#                                 to_np(interp_field[plot_level,:,:]),\n",
    "#                                 cmap=dbz_map,\n",
    "#                                 norm=dbz_norm,\n",
    "#                                 transform=dat_crs)\n",
    "\n",
    "# # Add Tiawan counties:\n",
    "# shp_3 = cfeature.ShapelyFeature(shpreader.Reader('./TWN_shp/TWN_CITY').geometries(), crs.PlateCarree())\n",
    "# ax1.add_feature(shp_3, facecolor='none', edgecolor='black', linewidth=1.2)\n",
    "\n",
    "# # Add the color bar\n",
    "# # cb_dbz = fig.colorbar(f1_dbz_pcolors, ax=ax1, fraction=0.04)\n",
    "# cb_dbz = fig.colorbar(f1_dbz_pcolors, ticks=clevs[1:17], fraction=0.04)\n",
    "# cb_dbz.ax.tick_params(labelsize=14)\n",
    "\n",
    "# # Set axes:\n",
    "# fig_tit = ax1.set_title('Reflectivity (dBZ) ' + str(interp_levels[plot_level]) + 'km ' + wrf_valid_datetime.values, fontsize=24)\n",
    "# # ax1.set_xlabel('Lon', fontsize=18)\n",
    "# # ax1.set_ylabel('Lat', fontsize=18)\n",
    "# # ax1.labelsize = 18\n",
    "\n",
    "# ax1_gl = ax1.gridlines(draw_labels=True)\n",
    "# ax1_gl.xlabels_top = False\n",
    "# ax1_gl.ylabels_right = False\n",
    "\n",
    "# # Save figure:\n",
    "# # fig_name = './wrfoutdbz_' + str(interp_levels) + '_' + interp_field['Time'].dt.strftime('%Y-%m-%d_%H:%M:%S').values\n",
    "# # plt.savefig(fig_name, transparent=False, edgecolor='white', bbox_inches=\"tight\", dpi=300)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 304,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/anaconda3/lib/python3.8/site-packages/ipykernel/ipkernel.py:287: DeprecationWarning: `should_run_async` will not call `transform_cell` automatically in the future. Please pass the result to `transformed_cell` argument and any exception that happen during thetransform in `preprocessing_exc_tuple` in IPython 7.17 and above.\n",
      "  and should_run_async(code)\n"
     ]
    }
   ],
   "source": [
    "# print(type(interp_field_2d))\n",
    "# print(interp_field_2d)\n",
    "# print(interp_field_2d['XLONG'].values[0,:])\n",
    "# print(interp_field_2d['XLAT'].values[:,0])\n",
    "# print(np.array(interp_field_2d['XLONG'].values.min()))\n",
    "# print(np.array(interp_field_2d['XLAT'].values.min()))\n",
    "# print(pyart.config.get_metadata('origin_altitude'))\n",
    "# print(interp_field_2d.values.shape)\n",
    "# print(distance([23.5,120],[23.5,130]))\n",
    "\n",
    "# print(str(interp_levels[0]))\n",
    "# print(interp_field_2d['Time'].dt.strftime('%Y-%m-%d_%H:%M:%S').values)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 305,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/anaconda3/lib/python3.8/site-packages/ipykernel/ipkernel.py:287: DeprecationWarning: `should_run_async` will not call `transform_cell` automatically in the future. Please pass the result to `transformed_cell` argument and any exception that happen during thetransform in `preprocessing_exc_tuple` in IPython 7.17 and above.\n",
      "  and should_run_async(code)\n"
     ]
    }
   ],
   "source": [
    "# Convert to Pyart grid object:\n",
    "\n",
    "fields = {}\n",
    "fields['reflectivity'] = {'data': interp_field.values, '_FillValue': -9999.0}\n",
    "# print(fields['reflectivity'])\n",
    "\n",
    "time = pyart.config.get_metadata('grid_time')\n",
    "\n",
    "time['data'] = np.array([0])\n",
    "time['units'] = 'seconds since ' + interp_field['Time'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')\n",
    "\n",
    "# grid origin location dictionaries\n",
    "origin_latitude = pyart.config.get_metadata('origin_latitude')\n",
    "# origin_latitude['data'] = interp_field_2d['XLAT'].values.min()\n",
    "origin_latitude['data'] = [interp_field['XLAT'].values[0,0]]\n",
    "\n",
    "origin_longitude = pyart.config.get_metadata('origin_longitude')\n",
    "# origin_longitude['data'] = interp_field_2d['XLONG'].values.min()\n",
    "origin_longitude['data'] = [interp_field['XLONG'].values[0,0]]\n",
    "\n",
    "origin_altitude = pyart.config.get_metadata('origin_altitude')\n",
    "# origin_altitude['data'] = [interp_levels]\n",
    "# origin_altitude['units'] = 'hPa'\n",
    "origin_altitude['data'] = [0]\n",
    "origin_altitude['units'] = 'm'\n",
    "\n",
    "x = pyart.config.get_metadata('x')\n",
    "y = pyart.config.get_metadata('y')\n",
    "z = pyart.config.get_metadata('z')\n",
    "\n",
    "tmp_x = []\n",
    "for lon in interp_field['XLONG'].values[0,:]:\n",
    "    tmp_x.append(distance([interp_field['XLAT'].values[0,0],interp_field['XLONG'].values[0,0]],[interp_field['XLAT'].values[0,0],lon]))\n",
    "\n",
    "x['data'] = np.array(tmp_x) * 1000\n",
    "    \n",
    "tmp_y = []\n",
    "for lat in interp_field['XLAT'].values[:,0]:\n",
    "    tmp_y.append(distance([interp_field['XLAT'].values[0,0],interp_field['XLONG'].values[0,0]],[lat,interp_field['XLONG'].values[0,0]]))\n",
    "\n",
    "y['data'] = np.array(tmp_y) * 1000\n",
    "\n",
    "z['data'] = interp_levels * 1000\n",
    "z['units'] = 'm'\n",
    "\n",
    "# print(x)\n",
    "# print(z)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 306,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/anaconda3/lib/python3.8/site-packages/ipykernel/ipkernel.py:287: DeprecationWarning: `should_run_async` will not call `transform_cell` automatically in the future. Please pass the result to `transformed_cell` argument and any exception that happen during thetransform in `preprocessing_exc_tuple` in IPython 7.17 and above.\n",
      "  and should_run_async(code)\n"
     ]
    }
   ],
   "source": [
    "# metadata dictionary\n",
    "metadata={}\n",
    "metadata['original_container'] = 'RadialSet'\n",
    "metadata['site_name'] = 'N/A'\n",
    "metadata['radar_name'] = 'WRF-Output'\n",
    "\n",
    "# create radar dictionaries\n",
    "radar_latitude = pyart.config.get_metadata('radar_latitude')\n",
    "radar_latitude['data'] = [origin_latitude['data']]\n",
    "\n",
    "# print(radar_latitude['data'])\n",
    "# print(type(radar_latitude['data']))\n",
    "\n",
    "radar_longitude = pyart.config.get_metadata('radar_longitude')\n",
    "radar_longitude['data'] = [origin_longitude['data']]\n",
    "\n",
    "radar_altitude = pyart.config.get_metadata('radar_altitude')\n",
    "radar_altitude['data'] = [z['data']]\n",
    "\n",
    "radar_time = pyart.config.get_metadata('radar_time')\n",
    "radar_time['data'] = np.array([0])\n",
    "radar_time['units'] = 'seconds since ' + interp_field['Time'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')\n",
    "\n",
    "radar_name = pyart.config.get_metadata('radar_name')\n",
    "radar_name['data'] = np.array(['WRF-Output'])\n",
    "\n",
    "# projection = kwargs.pop('grid_projection', None)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 307,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/anaconda3/lib/python3.8/site-packages/ipykernel/ipkernel.py:287: DeprecationWarning: `should_run_async` will not call `transform_cell` automatically in the future. Please pass the result to `transformed_cell` argument and any exception that happen during thetransform in `preprocessing_exc_tuple` in IPython 7.17 and above.\n",
      "  and should_run_async(code)\n",
      "/usr/local/anaconda3/lib/python3.8/site-packages/pyart/io/cfradial.py:706: UserWarning: Warning, converting non-array to array:origin_latitude\n",
      "  warnings.warn(\"Warning, converting non-array to array:%s\" % name)\n",
      "/usr/local/anaconda3/lib/python3.8/site-packages/pyart/io/cfradial.py:706: UserWarning: Warning, converting non-array to array:origin_longitude\n",
      "  warnings.warn(\"Warning, converting non-array to array:%s\" % name)\n",
      "/usr/local/anaconda3/lib/python3.8/site-packages/pyart/io/cfradial.py:706: UserWarning: Warning, converting non-array to array:origin_altitude\n",
      "  warnings.warn(\"Warning, converting non-array to array:%s\" % name)\n",
      "/usr/local/anaconda3/lib/python3.8/site-packages/pyart/io/cfradial.py:706: UserWarning: Warning, converting non-array to array:radar_latitude\n",
      "  warnings.warn(\"Warning, converting non-array to array:%s\" % name)\n",
      "/usr/local/anaconda3/lib/python3.8/site-packages/pyart/io/cfradial.py:706: UserWarning: Warning, converting non-array to array:radar_longitude\n",
      "  warnings.warn(\"Warning, converting non-array to array:%s\" % name)\n",
      "/usr/local/anaconda3/lib/python3.8/site-packages/pyart/io/cfradial.py:706: UserWarning: Warning, converting non-array to array:radar_altitude\n",
      "  warnings.warn(\"Warning, converting non-array to array:%s\" % name)\n"
     ]
    },
    {
     "ename": "ValueError",
     "evalue": "input operand has more dimensions than allowed by the axis remapping",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mValueError\u001b[0m                                Traceback (most recent call last)",
      "\u001b[0;32msrc/netCDF4/_netCDF4.pyx\u001b[0m in \u001b[0;36mnetCDF4._netCDF4.Variable.__setitem__\u001b[0;34m()\u001b[0m\n",
      "\u001b[0;31mValueError\u001b[0m: cannot reshape array of size 31 into shape (1,)",
      "\nDuring handling of the above exception, another exception occurred:\n",
      "\u001b[0;31mValueError\u001b[0m                                Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-307-80c896c3e647>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m     18\u001b[0m \u001b[0;31m# pyart_grid_file.write(filename=output_filename)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     19\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 20\u001b[0;31m \u001b[0mpyart\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mio\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mwrite_grid\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0moutput_filename\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mpyart_grid_file\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;32m/usr/local/anaconda3/lib/python3.8/site-packages/pyart/io/grid_io.py\u001b[0m in \u001b[0;36mwrite_grid\u001b[0;34m(filename, grid, format, write_proj_coord_sys, proj_coord_sys, arm_time_variables, arm_alt_lat_lon_variables, write_point_x_y_z, write_point_lon_lat_alt)\u001b[0m\n\u001b[1;32m    262\u001b[0m         \u001b[0mattr\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mgetattr\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mgrid\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mattr_name\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    263\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0mattr\u001b[0m \u001b[0;32mis\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 264\u001b[0;31m             \u001b[0m_create_ncvar\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mattr\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mdset\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mattr_name\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m(\u001b[0m\u001b[0;34m'nradar'\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    265\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    266\u001b[0m     \u001b[0;32mif\u001b[0m \u001b[0mgrid\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mradar_name\u001b[0m \u001b[0;32mis\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m/usr/local/anaconda3/lib/python3.8/site-packages/pyart/io/cfradial.py\u001b[0m in \u001b[0;36m_create_ncvar\u001b[0;34m(dic, dataset, name, dimensions)\u001b[0m\n\u001b[1;32m    778\u001b[0m             \u001b[0mncvar\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m...\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m:\u001b[0m\u001b[0mdata\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mshape\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m-\u001b[0m\u001b[0;36m1\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mdata\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    779\u001b[0m     \u001b[0;32melse\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 780\u001b[0;31m         \u001b[0mncvar\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mdata\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    781\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    782\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32msrc/netCDF4/_netCDF4.pyx\u001b[0m in \u001b[0;36mnetCDF4._netCDF4.Variable.__setitem__\u001b[0;34m()\u001b[0m\n",
      "\u001b[0;32m<__array_function__ internals>\u001b[0m in \u001b[0;36mbroadcast_to\u001b[0;34m(*args, **kwargs)\u001b[0m\n",
      "\u001b[0;32m/usr/local/anaconda3/lib/python3.8/site-packages/numpy/lib/stride_tricks.py\u001b[0m in \u001b[0;36mbroadcast_to\u001b[0;34m(array, shape, subok)\u001b[0m\n\u001b[1;32m    409\u001b[0m            [1, 2, 3]])\n\u001b[1;32m    410\u001b[0m     \"\"\"\n\u001b[0;32m--> 411\u001b[0;31m     \u001b[0;32mreturn\u001b[0m \u001b[0m_broadcast_to\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0marray\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mshape\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0msubok\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0msubok\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mreadonly\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;32mTrue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    412\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    413\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m/usr/local/anaconda3/lib/python3.8/site-packages/numpy/lib/stride_tricks.py\u001b[0m in \u001b[0;36m_broadcast_to\u001b[0;34m(array, shape, subok, readonly)\u001b[0m\n\u001b[1;32m    346\u001b[0m                          'negative')\n\u001b[1;32m    347\u001b[0m     \u001b[0mextras\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34m[\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 348\u001b[0;31m     it = np.nditer(\n\u001b[0m\u001b[1;32m    349\u001b[0m         \u001b[0;34m(\u001b[0m\u001b[0marray\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mflags\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'multi_index'\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m'refs_ok'\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m'zerosize_ok'\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m+\u001b[0m \u001b[0mextras\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    350\u001b[0m         op_flags=['readonly'], itershape=shape, order='C')\n",
      "\u001b[0;31mValueError\u001b[0m: input operand has more dimensions than allowed by the axis remapping"
     ]
    }
   ],
   "source": [
    "# Make and Write out to Pyart grid object:\n",
    "\n",
    "output_filename = './Grid_obj/grid_' + output_grid_obj_num + '.nc'\n",
    "\n",
    "# print(fields)\n",
    "# print(fields['reflectivity'])\n",
    "\n",
    "pyart_grid_file = pyart.core.Grid(time, fields, metadata,\n",
    "                                  origin_latitude, origin_longitude, origin_altitude, x, y, z,\n",
    "                                  radar_latitude=radar_latitude, radar_longitude=radar_longitude,\n",
    "                                  radar_altitude=radar_altitude, radar_name=radar_name,\n",
    "                                  radar_time=radar_time, projection=None\n",
    "                                 )\n",
    "                                #.write(filename=output_filename)\n",
    "\n",
    "# print(pyart_grid_file.z)\n",
    "# pyart_grid_file.write(filename=output_filename, format='NETCDF4')\n",
    "# pyart_grid_file.write(filename=output_filename)\n",
    "\n",
    "pyart.io.write_grid(output_filename, pyart_grid_file)"
   ]
  }
 ],
 "metadata": {
  "anaconda-cloud": {},
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}
