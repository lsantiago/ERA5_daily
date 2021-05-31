import os


def get_name(issue_date):
    return f'{issue_date.year}{issue_date.month:02.0f}{issue_date.day:02.0f}'

def change_namevars(name_file):
    '''
    Change name vars
    '''
    f_in = name_file +'.nc'
    f_out = f'{name_file}_changnamevars.nc'

    os.system(f'cdo chname,tp,pre,t2m,tavg,mn2t,tmin,mx2t,tmax,ssr,ssrd,longitude,lon,latitude,lat {f_in} {f_out}')    



def set_missing_value(name_file):
    '''
    Set a new Missing_value
    '''
    f_in = f'{name_file}_changnamevars.nc'
    f_out = f'{name_file}_missingvalues.nc'

    os.system(f'cdo -setmissval,-9999.0 -setmissval,nan {f_in} {f_out}')

def fix_units(name_file):
    '''
    Change units of measurement
    '''
    f_in = f'{name_file}_missingvalues.nc'
    f_out_changeunits = f'{name_file}_changeunits.nc'
    f_out_changenames = f'{name_file}_newnames.nc'
    os.system(f"cdo -expr,'pre=pre*1000;tavg=tavg-273.16;tmin=tmin-273.16;tmax=tmax-273.16;ssrd=ssrd' {f_in} {f_out_changeunits}")
    os.system(f'cdo -setattribute,pre@units="mm/day",ssrd@units="W m-2",tmin@units="C",tmax@units="C",tavg@units="C" {f_out_changeunits} {f_out_changenames}')



def fix_latlon(name_file):
    f_in = f'{name_file}_newnames.nc'
    f_out_fixlatlon = f'{name_file}.nc'
    os.system(f"cdo sellonlatbox,-81.5,-79,-5.5,-3.5 {f_in} {f_out_fixlatlon}")



def fix_time(issue_date):
    pass

def delete_tempfiles():
    os.system(f'rm *_*.nc')


def fix_download(issue_date):
    name_file = get_name(issue_date)
    change_namevars(name_file)
    set_missing_value(name_file)
    fix_units(name_file)
    fix_latlon(name_file)
    delete_tempfiles()
