from rest_framework import serializers
from .models import Film, Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model
    """
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_name', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_content(self, value):
        """Ensure comment doesn't exceed 500 characters"""
        if len(value) > 500:
            raise serializers.ValidationError(
                "Comment cannot exceed 500 characters."
            )
        return value


class FilmListSerializer(serializers.ModelSerializer):
    """
    Serializer for Film list view with comment count
    """
    comment_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Film
        fields = ['id', 'title', 'release_date', 'comment_count']


class FilmDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Film with all information
    """
    comment_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Film
        fields = [
            'id', 
            'title', 
            'episode_id',
            'opening_crawl',
            'director',
            'producer',
            'release_date', 
            'comment_count',
            'comments'
        ]