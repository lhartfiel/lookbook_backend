from rest_framework import serializers, viewsets
from django.shortcuts import render
from taggit.serializers import TagListSerializerField, TaggitSerializer
from .models import Style, Image


# Serializers define the API representation.
class ImageSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="get_type_display")
    view = serializers.CharField(source="get_view_display")
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = "__all__"

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url
        return None


class StyleSerializer(TaggitSerializer, serializers.ModelSerializer):
    style_image = ImageSerializer(many=True, read_only=True)
    tags = TagListSerializerField()
    length = serializers.CharField(source="get_length_display")
    maintenance = serializers.CharField(source="get_maintenance_display")
    texture = serializers.CharField(source="get_texture_display")
    thickness = serializers.CharField(source="get_thickness_display")

    class Meta:
        model = Style
        fields = "__all__"
