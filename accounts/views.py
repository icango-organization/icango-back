from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets    import ModelViewSet
from accounts.models import Feedback

from accounts.serializers import FeedbackSerializer

class FeedbackViewSet(ModelViewSet):
    serializer_class = FeedbackSerializer

    def get_queryset(self):

        # test
        user = 'test'

        queryset = Feedback.objects.filter(account=user)

        return queryset

    def create(self, request):

        # test
        user = 'test'

        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)

            return Response({'message': 'Feedback Created'})
        
        return Response({'message': 'Feedback Creation Failed'})
    
    def update(self, request):

        # test
        user = 'test'

        feedback = Feedback.objects.get(id=request.data['id'])
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(feedback=feedback)

            return Response({'message': 'Feedback Updated'})
        
        return Response({'message': 'Feedback Update Failed'})