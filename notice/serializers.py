from rest_framework import serializers

from .models import Notice, NoticeAdmin


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


class NoticeAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeAdmin
        fields = "__all__"


class NoticeAdminCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeAdmin
        fields = [
            "subject",
            "content",
            "view",
        ]


class NoticeAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            "subject",
            "content",
            "view",
        ]
