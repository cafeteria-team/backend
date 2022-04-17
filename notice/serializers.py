from rest_framework import serializers

from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"


class NoticeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            "subject",
            "content",
            "view",
        ]


class NoticeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            "subject",
            "content",
            "view",
        ]
