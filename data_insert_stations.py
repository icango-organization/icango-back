# system setting
import os
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "icango.settings")
django.setup()

from information.models import Station

# insert data : stations
with open('data_stations_200313.csv') as csv_stations:
    rows = csv.reader(csv_stations)

    for n, row in enumerate(rows):
        if n == 0:
            pass
        else:
            Station.objects.create(
                RAIL_OPR_ISTT_CD = row[0],
                RAIL_OPR_ISTT_NM = row[1],
                LN_CD            = row[2],
                LN_NM            = row[3],
                STIN_CD          = row[4],
                STIN_NM          = row[5]
            )