import datetime
from dateutil.relativedelta import relativedelta
import subprocess
import os


def mkdate(datetime_data, DAY=False, HOUR=False):
    fmt = '%Y%m'
    if (DAY):
        fmt = fmt + '%d'
        if (HOUR):
            fmt = fmt + '%H'
    output = datetime.datetime.strftime(datetime_data, fmt)

    return output


def mkdirectory(AbsolutePATH):
    if not os.path.exists(AbsolutePATH):
        print('Make Directory : ' + AbsolutePATH)
        os.mkdir(AbsolutePATH)


def wget_dwnld(where, ini_datetime, fin_datetime):
    if (where[-1] != '/'):
        where = where + '/'

    nt = (fin_datetime - ini_datetime).days + 1
    #print(nt)

    present = ini_datetime

    NOAA_HOME = 'https://www.ncei.noaa.gov'
    SST_DATA  = 'data/sea-surface-temperature-optimum-interpolation'
    VERSION   = 'v2.1'
    DIR       = 'access/avhrr'
    URL_FIXED = '{}/{}/{}/{}'.format(NOAA_HOME, SST_DATA, VERSION, DIR)
    FNAME_FIXED = 'oisst-avhrr-v02r01'

    for t in range(nt):
        DESTIN = mkdate(present)
        AbsolutePATH = where + DESTIN
        present_str = mkdate(present, DAY=True)
        mkdirectory(AbsolutePATH)

        FILE = '{}.{}.nc'.format(FNAME_FIXED, present_str)
        
        if (not os.path.exists('{}/{}'.format(AbsolutePATH, FILE))):
            #print('{}/{}'.format(AbsolutePATH, FILE))
            URL = '{}/{}/{}'.format(URL_FIXED, DESTIN, FILE)
            CMD = 'wget -P {} {}'.format(AbsolutePATH, URL)
       
            print(CMD)
            subprocess.run(CMD, shell=True)

        else:
            print('{}/{}   EXIST'.format(AbsolutePATH, FILE))

        present = present + datetime.timedelta(days=1)


ini = datetime.datetime(2024,  5, 28)
fin = datetime.datetime(2024,  5, 28)
wget_dwnld('/mnt/jet12/OISST/NetCDF', ini, fin)

