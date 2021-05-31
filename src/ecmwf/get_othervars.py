#!/usr/bin/env python
"""
Input file : None
Output file: tp_20170101-20170102.nc
"""
import cdsapi
from datetime import datetime, timedelta
import os


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
    ofile = f'othervars_{issue_date.year:02.0f}{issue_date.month:02.0f}{issue_date.day:02.0f}'
    os.system(f'cdo daymean *_temp.nc {ofile}_temp2.nc')
    os.system(f'cdo -settime,00:00:00 {ofile}_temp2.nc {ofile}.nc')
    os.system('rm *_temp*.nc')