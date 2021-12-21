from .models      import Station
from .serializers import StationSerializer

from rest_framework.response    import Response
from rest_framework.viewsets    import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

class StationViewSet(ModelViewSet):
    serializer_class = StationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        keyword  = self.request.query_params.get('keyword')
        queryset = Station.objects.filter(STIN_NM__icontains=keyword).order_by('STIN_CD')

        return queryset