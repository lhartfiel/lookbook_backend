from django.shortcuts import render
from rest_framework import viewsets
from .models import Style, Image
from .serializers import StyleSerializer, ImageSerializer


# Create your views here.
# ViewSets define the view behavior.
class StyleViewSet(viewsets.ModelViewSet):
    """
    Generic viewset for each Style
    """

    queryset = Style.objects.all()
    serializer_class = StyleSerializer
