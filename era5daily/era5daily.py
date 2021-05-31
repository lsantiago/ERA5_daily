import cdsapi
from datetime import datetime, timedelta
import os

import time, sys
from netCDF4 import Dataset, date2num, num2date
import numpy as np


def download(issue_date):
    issue_year = issue_date.year
    issue_month = issue_date.month
    issue_day = issue_date.day

    download_precipitation(issue_year, issue_month, issue_day)
    calculate_precipitation(issue_year, issue_month, issue_day)
    download_variables(issue_year, issue_month, issue_day)


def download_precipitation(issue_year, issue_month, issue_day):
    issue_date = datetime(year=issue_year, month=issue_month, day=issue_day)
    next_date = issue_date + timedelta(days=1)
    print('Start download')
    request_precipitation(issue_date)
    request_precipitation(next_date)
    print('Download copleted!')
    print('Merge precipitation')
    merge_precipitation(issue_date, next_date)
    print('Merge completed')


def request_precipitation(date):
    year = str(date.year)
    month = f'{date.month:02.0f}'
    day = f'{date.day:02.0f}'

    c = cdsapi.Client()
    r = c.retrieve(
        'reanalysis-era5-single-levels', {
            'variable': 'total_precipitation',
            'product_type': 'reanalysis',
            'year': year,
            'month': month,
            'day': day,
            "area": "-3.5/-81.5/-5.5/-79",
            'grid': "0.25/0.25",
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00'
            ],
            'format': 'netcdf'
        })
    r.download(f'tp_{year}{month}{day}_temp.nc')

def merge_precipitation(issue_date, next_date):
    ofile = f'tp_{issue_date.year:02.0f}{issue_date.month:02.0f}{issue_date.day:02.0f}-{next_date.year:02.0f}{next_date.month:02.0f}{next_date.day:02.0f}.nc'
    os.system(f'cdo -O -f nc4c -k grid -z zip_4 mergetime *_temp.nc {ofile}')
    os.system('rm *_temp*.nc')

def calculate_precipitation(year, month, day):
    day = int(f'{year}{month:02.0f}{day:02.0f}')  #Example format 20170101
    d = datetime.strptime(str(day), '%Y%m%d')
    f_in = 'tp_%d-%s.nc' % (day, (d + timedelta(days=1)).strftime('%Y%m%d'))
    f_out = 'daily-tp_%d.nc' % day

    time_needed = []
    for i in range(1, 25):
        time_needed.append(d + timedelta(hours=i))

    with Dataset(f_in) as ds_src:
        var_time = ds_src.variables['time']
        time_avail = num2date(var_time[:], var_time.units,
                              calendar=var_time.calendar)

        indices = []
        for tm in time_needed:
            a = np.where(time_avail == tm)[0]
            if len(a) == 0:
                sys.stderr.write('Error: precipitation data is missing/incomplete - %s!\n'
                                 % tm.strftime('%Y%m%d %H:%M:%S'))
                sys.exit(200)
            else:
                print('Found %s' % tm.strftime('%Y%m%d %H:%M:%S'))
                indices.append(a[0])

        var_tp = ds_src.variables['tp']
        tp_values_set = False
        for idx in indices:
            if not tp_values_set:
                data = var_tp[idx, :, :]
                tp_values_set = True
            else:
                data += var_tp[idx, :, :]

        with Dataset(f_out, mode='w', format='NETCDF3_64BIT_OFFSET') as ds_dest:
            # Dimensions
            for name in ['latitude', 'longitude']:
                dim_src = ds_src.dimensions[name]
                ds_dest.createDimension(name, dim_src.size)
                var_src = ds_src.variables[name]
                var_dest = ds_dest.createVariable(name, var_src.datatype, (name,))
                var_dest[:] = var_src[:]
                var_dest.setncattr('units', var_src.units)
                var_dest.setncattr('long_name', var_src.long_name)

            ds_dest.createDimension('time', None)
            var = ds_dest.createVariable('time', np.int32, ('time',))
            time_units = 'hours since 1900-01-01 00:00:00'
            time_cal = 'gregorian'
            var[:] = date2num([d], units=time_units, calendar=time_cal)
            var.setncattr('units', time_units)
            var.setncattr('long_name', 'time')
            var.setncattr('calendar', time_cal)

            # Variables
            var = ds_dest.createVariable(var_tp.name, np.double, var_tp.dimensions)
            var[0, :, :] = data
            var.setncattr('units', var_tp.units)
            var.setncattr('long_name', var_tp.long_name)

            # Attributes
            ds_dest.setncattr('Conventions', 'CF-1.6')
            ds_dest.setncattr('history', '%s %s'
                              % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                 ' '.join(time.tzname)))

            print('Done! Daily total precipitation saved in %s' % f_out)

def download_variables(issue_year, issue_month, issue_day):
    issue_date = datetime(year=issue_year, month=issue_month, day=issue_day)
    next_date = issue_date + timedelta(days=1)
    print('Start download')
    request(issue_date)
    print('Download copleted!')
    mean(issue_date)
    print('Mean completed')


def request(date):
    year = str(date.year)
    month = f'{date.month:02.0f}'
    day = f'{date.day:02.0f}'

    c = cdsapi.Client()
    r = c.retrieve(
        'reanalysis-era5-single-levels', {
            'variable': ['2m_temperature', 'maximum_2m_temperature_since_previous_post_processing', 'minimum_2m_temperature_since_previous_post_processing', 'surface_solar_radiation'],
            'product_type': 'reanalysis',
            'year': year,
            'month': month,
            'day': day,
            "area": "-3.5/-81.5/-5.5/-79",
            'grid': "0.25/0.25",
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00'
            ],
            'format': 'netcdf'
        })
    r.download(f'othervars_{year}{month}{day}_temp.nc')

def mean(issue_date):
    ofile = f'{issue_date.year:02.0f}{issue_date.month:02.0f}{issue_date.day:02.0f}'
    os.system(f'cdo daymean *_temp.nc othervars_{ofile}_temp2.nc')
    os.system(f'cdo -settime,00:00:00 othervars_{ofile}_temp2.nc othervars_{ofile}.nc')
    os.system(f'cdo merge daily-tp_{ofile}.nc othervars_{ofile}.nc {ofile}.nc')
    os.system(f'rm *_temp*.nc')
    os.system(f'rm daily*')
    os.system(f'rm othervars*')
    os.system(f'rm tp*')