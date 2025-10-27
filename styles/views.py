from django.shortcuts import render
from rest_framework import viewsets
from .models import Style, Image
from .serializers import StyleSerializer, ImageSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .vector_search import VectorSearchService


@api_view(['POST'])
@permission_classes([AllowAny])
def search_styles(request):
    """
    Search styles using natural language query
    """
    query = request.data.get('query', '')

    if not query:
        return Response({'error': 'Query is required'}, status=400)

    try:
        # Try vector search first, fall back to text search
        try:
            vector_service = VectorSearchService()
            search_results = vector_service.search_styles(query, top_k=10)

            if search_results:
                # Get the actual Style objects
                style_ids = [result['style_id'] for result in search_results]
                styles = Style.objects.filter(id__in=style_ids)
                search_method = "vector"
            else:
                raise Exception("No vector results")

        except Exception as vector_error:
            # Fall back to text-based search
            from django.db.models import Q
            styles = Style.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(stylist_name__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
            search_method = "text"

        # Serialize the results
        serializer = StyleSerializer(styles, many=True)

        return Response({
            'query': query,
            'results': serializer.data,
            'search_method': search_method,
            'message': f'Found {len(styles)} matching styles using {search_method} search'
        })

    except Exception as e:
        return Response({
            'error': f'Search failed: {str(e)}'
        }, status=500)


# ViewSets define the view behavior.
class StyleViewSet(viewsets.ModelViewSet):
    """
    Generic viewset for each Style
    """

    queryset = Style.objects.all()
    serializer_class = StyleSerializer
