import boto3, uuid, botocore
from rest_framework.serializers import Serializer

from .models         import Account, Feedback, FeedbackImage
from .serializers    import FeedbackImageSerializer, FeedbackSerializer

from rest_framework.response    import Response
from rest_framework.viewsets    import ModelViewSet
from rest_framework.decorators  import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from icango.settings import \
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_STORAGE_BUCKET_NAME, AWS_S3_CUSTOM_DOMAIN

# # Test
# user = Account.objects.get(username="test")

@api_view(['POST'])
@permission_classes([AllowAny])
def test(request):
    return Response({})

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
        s3_client = boto3.client(
            's3',
            region_name = AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        feedbackimage_created = request.FILES.getlist('feedbackimage_created')
        images_for_serializer = []

        if len(feedbackimage_created) != 0:
            for image in feedbackimage_created:
                img_uuid = str(uuid.uuid4())
                s3_client.upload_fileobj(
                    image,
                    AWS_STORAGE_BUCKET_NAME,
                    img_uuid,
                    ExtraArgs = {
                        'ContentType' : image.content_type
                    }
                )
                images_for_serializer.append({'img_path' :  AWS_S3_CUSTOM_DOMAIN + "/" + img_uuid})
            
            serializer_feedbackimage = FeedbackImageSerializer(data=images_for_serializer, many=True)

            if serializer_feedbackimage.is_valid(raise_exception=True):
                serializer_feedbackimage.save(feedback=feedback)
        
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
        s3_client = boto3.client(
            's3',
            region_name = AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        feedbackimage_created = request.FILES.getlist('feedbackimage_created')
        serializer_for_images = []

        if len(feedbackimage_created) != 0:
            for image in feedbackimage_created:
                img_uuid = str(uuid.uuid4())
                s3_client.upload_fileobj(
                    image,
                    AWS_STORAGE_BUCKET_NAME,
                    img_uuid,
                    ExtraArgs = {
                        'ContentType' : image.content_type
                    }
                )
                serializer_for_images.append({'img_path' :  AWS_S3_CUSTOM_DOMAIN + "/" + img_uuid})
            
            serializer_feedbackimage = FeedbackImageSerializer(data=serializer_for_images, many=True)

            if serializer_feedbackimage.is_valid(raise_exception=True):
                serializer_feedbackimage.save(feedback=feedback)

        # FeedbackImage Delete
        feedbackimage_deleted = request.data.get('feedbackimage_deleted')

        if feedbackimage_deleted != None:
            feedbackimage_deleted = [image.get('id') for image in feedbackimage_deleted]
            FeedbackImage.objects.filter(pk__in=feedbackimage_deleted).delete()

        # Deserialize
        feedback_data = FeedbackSerializer(feedback, many=False).data

        return Response(feedback_data, status=200)

    def destroy(self, request, pk):
        feedback = Feedback.objects.filter(id=pk).first()

        if feedback == None:
            return Response({'message' : 'Feedback Does Not Exists'}, status=400)

        feedback.delete()

        return Response({'message' : 'Feedback Deleted'}, status=200)