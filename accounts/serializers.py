import uuid, datetime

from rest_framework import serializers

from .models         import Account, Feedback, FeedbackImage
from icango.settings import (
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_STORAGE_BUCKET_NAME, AWS_S3_CUSTOM_DOMAIN
)

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
    
    def create(self, validated_data):
        instance = Account.objects.create(
            username   = validated_data.get('username'),
            password   = validated_data.get('password'),
            is_active  = True,
            last_login = datetime.datetime.now() 
        )
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
    
    def update(self, instance, validated_data):
        instance.last_login = datetime.datetime.now()
        instance.save()

        return instance

class FeedbackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FeedbackImage
        fields = ['id', 'image_path']

    def create(self, validated_data):
        feedback = validated_data.pop('feedback')
        image   = FeedbackImage.objects.create(
            feedback   = feedback,
            image_path = validated_data.get('image_path')         
        )

        return image

class FeedbackSerializer(serializers.ModelSerializer):
    feedbackimage_set = FeedbackImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Feedback
        exclude = ['account']
    
    def create(self, validated_data):
        user                  = validated_data.pop("user")
        request_images_create = validated_data.pop('request_images_create')

        # Feedback Create
        feedback         = super().create(validated_data)
        feedback.account = user
        feedback.save()

        # FeedbackImage
        images = []

        # FeedbackImage Create
        if request_images_create:            
            for image in request_images_create:
                image_path = (
                    AWS_S3_CUSTOM_DOMAIN
                    + "feedback"
                    + "/" + str(feedback.id)
                    + "/" + str(uuid.uuid4())
                )
                image = FeedbackImage.objects.create(
                    feedback    = feedback,
                    image_path = image_path
                )
                images.append(image)

        return [feedback, images]

    def update(self, feedback, validated_data):
        request_images_create = validated_data.pop('request_images_create')
        request_images_delete = validated_data.pop('request_images_delete')

        # Feedback Create
        feedback = super().update(feedback, validated_data)

        # FeedbackImage
        images = []

        # FeedbackImage Create
        if request_images_create:            
            for image in request_images_create:
                image_path = (
                    AWS_S3_CUSTOM_DOMAIN
                    + "feedback"
                    + "/" + str(feedback.id)
                    + "/" + str(uuid.uuid4())
                )
                image = FeedbackImage.objects.create(
                    feedback   = feedback,
                    image_path = image_path
                )
                images.append(image)

        # FeedbackImage Delete
        if request_images_delete:
            pks = [image.get("id") for image in request_images_delete]
            FeedbackImage.objects.filter(pk__in=pks).delete()

        return [feedback, images]