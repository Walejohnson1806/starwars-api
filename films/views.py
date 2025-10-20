import traceback
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Count
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Film, Comment
from .serializers import FilmListSerializer, FilmDetailSerializer, CommentSerializer
from .swapi_service import SWAPIService



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema_view(
    list=extend_schema(
        description="Get list of all Star Wars films with comment counts, sorted by release date",
        responses={200: FilmListSerializer(many=True)}
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific film",
        responses={200: FilmDetailSerializer}
    ),
)
class FilmViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing Star Wars films
    """
    queryset = Film.objects.annotate(
        comment_count=Count('comments')
    ).order_by('release_date')
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FilmListSerializer
        return FilmDetailSerializer
    
    @extend_schema(
        description="Sync films from SWAPI",
        responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}}
    )
    @action(detail=False, methods=['post'])
    def sync(self, request):
        """
        Sync films from SWAPI
        """
        try:
            swapi_service = SWAPIService()
            films_synced = swapi_service.sync_films()
            return Response({
                'message': f'Successfully synced {films_synced} films from SWAPI'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': f'Failed to sync films: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema_view(
    create=extend_schema(
        description="Add a comment to a film (max 500 characters)",
        request=CommentSerializer,
        responses={201: CommentSerializer}
    ),
    list=extend_schema(
        description="Get all comments for a specific film, sorted by creation time",
        responses={200: CommentSerializer(many=True)}
    ),
)
class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comments on films
    """
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post']
    
    def get_queryset(self):
        """
        Filter comments by film_id from URL
        """
        film_id = self.kwargs.get('film_pk')
        return Comment.objects.filter(film_id=film_id).order_by('created_at')
    
    def create(self, request, *args, **kwargs):
        """
        Create a new comment for a film
        """
        film_id = self.kwargs.get('film_pk')
        film = get_object_or_404(Film, id=film_id)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            film=film,
            ip_address=self.get_client_ip(request)
        )
        
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip