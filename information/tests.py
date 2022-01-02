import csv

from django.test import TestCase

from rest_framework.test import APIClient

from .models import Station

class StationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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

    def test_station_get_queryset_200(self):
        client = APIClient()

        response = client.get(
            '/information/station?keyword=종로'
        )

        self.assertEqual(
            response.json(),
            [
                {
                    "id": 678,
                    "RAIL_OPR_ISTT_CD": "S1",
                    "RAIL_OPR_ISTT_NM": "서울교통공사(구서울메트로)",
                    "LN_CD": "1",
                    "LN_NM": "1호선",
                    "STIN_CD": "129",
                    "STIN_NM": "종로5가"
                },
                {
                    "id": 679,
                    "RAIL_OPR_ISTT_CD": "S1",
                    "RAIL_OPR_ISTT_NM": "서울교통공사(구서울메트로)",
                    "LN_CD": "1",
                    "LN_NM": "1호선",
                    "STIN_CD": "130",
                    "STIN_NM": "종로3가"
                },
                {
                    "id": 744,
                    "RAIL_OPR_ISTT_CD": "S1",
                    "RAIL_OPR_ISTT_NM": "서울교통공사(구서울메트로)",
                    "LN_CD": "3",
                    "LN_NM": "3호선",
                    "STIN_CD": "329",
                    "STIN_NM": "종로3가"
                },
                {
                    "id": 818,
                    "RAIL_OPR_ISTT_CD": "S5",
                    "RAIL_OPR_ISTT_NM": "서울교통공사(구서울도시철도)",
                    "LN_CD": "5",
                    "LN_NM": "5호선",
                    "STIN_CD": "534",
                    "STIN_NM": "종로3가(탑골공원)"
                }
            ]
        )

        self.assertEqual(
            response.status_code, 200
        )