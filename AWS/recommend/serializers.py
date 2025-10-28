from rest_framework import serializers

from .models import OutfitRecommendation


class OutfitRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutfitRecommendation
        fields = [
            "id",
            "rec_1",
            "rec_2",
            "rec_3",
            "explanation",
            "image_url",
            "is_bookmarked",
            "created_at",
        ]
