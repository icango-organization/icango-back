
from .models      import Feedback, Account
from .serializers import AccountSerializer, FeedbackSerializer
from .utils       import BaseS3

from rest_framework.response              import Response
from rest_framework.viewsets              import ModelViewSet
from rest_framework.decorators            import api_view, permission_classes
from rest_framework.permissions           import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.views       import TokenObtainPairView
from rest_framework_simplejwt.exceptions  import InvalidToken, TokenError

class SignUpView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user = Account.objects.filter(username=request.data.get('username')).first()

        if user:
            return Response(
                {
                    "username": [
                        "account with this username already exists."
                    ]
                },
                status = 400
            )

        serializer_user= AccountSerializer(data=request.data)

        if serializer_user.is_valid(raise_exception=True):
            serializer_user.save()

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=201)

class FeedbackViewSet(ModelViewSet):
    serializer_class   = FeedbackSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field       = 'pk'
    s3                 = BaseS3(field="image_path")

    def get_queryset(self):
        queryset = (
            Feedback.objects
            .filter(account=self.request.user)
            .prefetch_related('feedbackimage_set')
        )

        return queryset
    
    def create(self, request):
        request_images_create = request.FILES.getlist("feedbackimage_set_create")

        # DB Create: Feedback, FeedbackImage
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            [feedback, images] = serializer.save(
                user                  = request.user,
                request_images_create = request_images_create
            )

        # S3 Create: FeedbackImage
        self.s3.api_post(
            files    = request_images_create,
            data_set = images
        )

        # Deserialize
        feedback_data = self.get_serializer(feedback, many=False).data

        return Response(feedback_data, status=201)

    def update(self, request, pk):
        request_images_create = request.FILES.getlist("feedbackimage_set_create")
        request_images_delete = request.data.get("feedbackimage_set_delete")

        # DB Update: Feedback, FeedbackImage
        feedback   = Feedback.objects.filter(id=pk).first()
        serializer = self.get_serializer(feedback, data=request.data)

        if not feedback:
            return Response({'detail' : 'Not found'}, status=404)

        if serializer.is_valid(raise_exception=True):
            [feedback, images] = serializer.save(
                request_images_create = request_images_create,
                request_images_delete = request_images_delete,            
            )

        # S3 Create: FeedbackImage
        self.s3.api_post(
            files    = request_images_create,
            data_set = images
        )

        # S3 Delete: FeedbackImage
        self.s3.api_delete(data_urls=request_images_delete)

        # Deserialize
        feedback_data = self.get_serializer(feedback, many=False).data

        return Response(feedback_data, status=200)

    def destroy(self, request, pk):
        # DB Delete: Feedback
        feedback = Feedback.objects.filter(id=pk).first()

        if not feedback:
            return Response({'detail' : 'Not found'}, status=404)
        
        # S3 Delete: FeedbackImage
        self.s3.api_delete(data_folder="feedback", data_folder_id=feedback.id)
        
        # DB Delete: Feedback
        feedback.delete()

        return Response({'detail' : 'Deleted'}, status=200)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def test(request):
    return Response({})

@api_view(['GET'])
@permission_classes([AllowAny])
def permission_classes_allowany(request):
    return Response({}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def permission_classes_isauthenicated(request):
    return Response({}, status=200)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def permission_classes_isadminuser(request):
    return Response({}, status=200)