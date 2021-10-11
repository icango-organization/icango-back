from .models         import Feedback, FeedbackImage
from icango.settings import \
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_STORAGE_BUCKET_NAME, AWS_S3_CUSTOM_DOMAIN

from rest_framework import serializers

class FeedbackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackImage
        fields = ['img_path']
        read_only_fields = ['id']

    def create(self, validated_data):
        feedback = validated_data.pop('feedback')
        image    = FeedbackImage.objects.create(
            feedback=feedback,
            img_path=validated_data['img_path']
        )
        
        return image

class FeedbackSerializer(serializers.ModelSerializer):
    feedbackimage_set = FeedbackImageSerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'

    def create(self, validated_data):
        user     = validated_data.pop('user')
        feedback = Feedback.objects.create(
            account = user,
            tag = validated_data['tag'],
            title = validated_data['title'],
            content = validated_data['content']
        )

        return feedback
    
    def update(self, feedback, validated_data):
        feedback.tag     = validated_data['tag']
        feedback.title   = validated_data['title']
        feedback.content = validated_data['content']
        feedback.save()

        return feedback