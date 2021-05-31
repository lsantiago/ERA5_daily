from datetime import datetime, timedelta
from src.ecmwf.get_tp import download_precipitation
from src.ecmwf.daily_tp import calculate_precipitation


if __name__ == '__main__':
    issue_year = 2021
    issue_month = 1
    issue_day = 31

    download_precipitation(issue_year, issue_month, issue_day)
    calculate_precipitation(issue_year, issue_month, issue_day)



    