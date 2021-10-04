from .models      import Account, Feedback, FeedbackImage
from .serializers import FeedbackImageSerializer, FeedbackSerializer

from rest_framework.response    import Response
from rest_framework.viewsets    import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

# Test
user = Account.objects.get(username="jyeon")

class FeedbackViewSet(ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = \
            Feedback.objects.filter(account=user)\
            .prefetch_related('feedbackimage_set')

        return queryset

    def create(self, request):
        # Feedback Create
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            feedback = serializer.save(user=user)

        # FeedbackImage Create
        images_created = request.data.get("feedbackimage_created")

        if images_created != None:
            serializer_images = FeedbackImageSerializer(data=images_created, many=True)

            if serializer_images.is_valid(raise_exception=True):
                serializer_images.save(feedback=feedback)
        
        # Deserialize
        feedback_data = FeedbackSerializer(feedback, many=False).data

        return Response(feedback_data, status=201)

    def update(self, request, pk):
        # Feedback Update
        feedback   = Feedback.objects.filter(id=pk).first()
        serializer = self.get_serializer(feedback, data=request.data)

        if feedback == None:
            return Response({'message' : 'Feedback Does Not Exists'}, status=400)

        if serializer.is_valid(raise_exception=True):
            feedback = serializer.save()     

        # FeedbackImage Create
        images_created = request.data.get("feedbackimage_created")

        if images_created != None:
            serializer_images = FeedbackImageSerializer(data=images_created, many=True)

            if serializer_images.is_valid(raise_exception=True):
                serializer_images.save(feedback=feedback)

        # FeedbackImage Delete
        images_deleted = request.data.get('feedbackimage_deleted')

        if images_deleted != None:
            images_deleted = [image.get('id') for image in images_deleted]
            FeedbackImage.objects.filter(pk__in=images_deleted).delete()

        # Deserialize
        feedback_data = FeedbackSerializer(feedback, many=False).data

        return Response(feedback_data, status=200)

    def destroy(self, request, pk):
        feedback = Feedback.objects.filter(id=pk).first()

        if feedback == None:
            return Response({'message' : 'Feedback Does Not Exists'}, status=400)

        feedback.delete()

        return Response({'message' : 'Feedback Deleted'}, status=200)