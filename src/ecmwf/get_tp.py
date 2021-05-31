#!/usr/bin/env python
"""
Save as get-tp.py, then run "python get-tp.py".
  
Input file : None
Output file: tp_20170101-20170102.nc
"""
import cdsapi
from datetime import datetime, timedelta
import os


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