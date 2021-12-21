import requests
from requests import status_codes
from rest_framework.decorators import action

from .models      import Station
from .serializers import StationSerializer
from icango.settings import API_serviceKey

from rest_framework.response    import Response
from rest_framework.views       import APIView
from rest_framework.viewsets    import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

class StationViewSet(ModelViewSet):
    serializer_class = StationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        keyword  = self.request.query_params.get('keyword')
        queryset = Station.objects.filter(STIN_NM__icontains=keyword).order_by('STIN_CD')

        return queryset

class RouteViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def exittoplatform(self, request):
        data     = request.data
        response = requests.get(
            (
                ("http://openapi.kric.go.kr/openapi/handicapped/stationMovement")
                + ("?serviceKey={serviceKey}")
                + ("&format=JSON")
                + ("&lnCd={lnCd}")
                + ("&stinCd={stinCd}")
                + ("&railOprIsttCd={railOprIsttCd}")
                + ("&nextStinCd={nextStinCd}")
            ).format(
                serviceKey=API_serviceKey,
                lnCd=data.get('lnCd'),
                stinCd=data.get('stinCd'),
                nextStinCd=data.get('nextStinCd'),
                railOprIsttCd=data.get('railOprIsttCd')   
            )
        )

        return Response(response.json(), status=200)

    @action(detail=False, methods=['get'])
    def transfer(self, request):
        data     = request.data

        test = (
            (
                ("http://openapi.kric.go.kr/openapi/handicapped/transferMovement")
                + ("?serviceKey={serviceKey}")
                + ("&format=JSON")
                + ("&stinCd={stinCd}")
                + ("&lnCd={lnCd}")
                + ("&railOprIsttCd={railOprIsttCd}")
                + ("&chthTgtLn={chthTgtLn}")
                + ("&chtnNextStinCd={chtnNextStinCd}")
                + ("&prevStinCd={prevStinCd}")

            ).format(
                serviceKey=API_serviceKey,
                stinCd=data.get('stinCd'),
                lnCd=data.get('lnCd'),
                railOprIsttCd=data.get('railOprIsttCd'),
                chthTgtLn=data.get('chthTgtLn'),
                chtnNextStinCd=data.get('chtnNextStinCd'),
                prevStinCd=data.get('prevStinCd')  
            )
        )

        response = requests.get(
            (
                ("http://openapi.kric.go.kr/openapi/handicapped/transferMovement")
                + ("?serviceKey={serviceKey}")
                + ("&format=JSON")
                + ("&stinCd={stinCd}")
                + ("&lnCd={lnCd}")
                + ("&railOprIsttCd={railOprIsttCd}")
                + ("&chthTgtLn={chthTgtLn}")
                + ("&chtnNextStinCd={chtnNextStinCd}")
                + ("&prevStinCd={prevStinCd}")

            ).format(
                serviceKey=API_serviceKey,
                stinCd=data.get('stinCd'),
                lnCd=data.get('lnCd'),
                railOprIsttCd=data.get('railOprIsttCd'),
                chthTgtLn=data.get('chthTgtLn'),
                chtnNextStinCd=data.get('chtnNextStinCd'),
                prevStinCd=data.get('prevStinCd')  
            )
        )

        return Response(response.json(), status=200)
