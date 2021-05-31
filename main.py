from datetime import datetime, timedelta
from src.ecmwf.get_tp import download_precipitation
from src.ecmwf.daily_tp import calculate_precipitation
from src.ecmwf import get_othervars


if __name__ == '__main__':
    issue_year = 2021
    issue_month = 2
    issue_day = 28

    download_precipitation(issue_year, issue_month, issue_day)
    calculate_precipitation(issue_year, issue_month, issue_day)
    get_othervars.download_variables(issue_year, issue_month, issue_day)


    