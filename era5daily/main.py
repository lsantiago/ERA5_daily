from datetime import datetime, timedelta
from era5daily import download
from util import *

import click

@click.command()
@click.option("-y", "--year", type=click.INT)
@click.option("-m", "--month", type=click.INT)
@click.option("-d", "--day", type=click.INT)
def main(year, month, day):
    if year is None:
        year = datetime.today().year
    if month is None:
        month = datetime.today().month
    if day is None:
        day = datetime.today().day

    try:
        issue_date = datetime(year=year, month=month, day=day)
    except ValueError:
        print(f'Incorrect date')
        raise click.Abort()

    download(issue_date)
    fix_download(issue_date)

if __name__ == '__main__':
    main()


                                                                                                   