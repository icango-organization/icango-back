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

# # insert data : accounts

# import datetime

# from accounts.models    import Account

# username_list = ["test", "harry potter", "hermione granger", "ron weasley", "gennie weasley", "albus dumbledore"]

# for n, username in enumerate(username_list):
#     Account.objects.create(
#         username = username,
#         kakoid = n,
#         first_name = "first_name",
#         last_name = "last_name",
#         password = "password",
#         email = "email",
#         profile = "profile",
#         is_superuser = 0,
#         is_staff = 0,
#         is_active = 1,
#         is_deleted = 0,
#         date_joined = datetime.datetime.now(),
#         last_login = datetime.datetime.now(),
#         create_at = datetime.datetime.now(),
#         update_at = datetime.datetime.now(),
#         delete_at = datetime.datetime.now()
#     )