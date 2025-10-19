from rest_framework import serializers, viewsets
from taggit.serializers import TagListSerializerField, TaggitSerializer
from .models import Style, Image


# Serializers define the API representation.
class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = "__all__"


class StyleSerializer(TaggitSerializer, serializers.ModelSerializer):
    style_image = ImageSerializer(many=True, read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Style
        fields = "__all__"
