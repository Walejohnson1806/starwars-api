from django.db import models
from django.core.validators import MaxLengthValidator


class Film(models.Model):
    """
    Model to store Star Wars film data from SWAPI
    """
    swapi_id = models.IntegerField(unique=True, help_text="ID from SWAPI")
    title = models.CharField(max_length=200)
    episode_id = models.IntegerField()
    opening_crawl = models.TextField()
    director = models.CharField(max_length=100)
    producer = models.CharField(max_length=200)
    release_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['release_date']
        indexes = [
            models.Index(fields=['release_date']),
            models.Index(fields=['swapi_id']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.release_date.year})"
    
    @property
    def comment_count(self):
        """Return the number of comments for this film"""
        return self.comments.count()


class Comment(models.Model):
    """
    Model for user comments on films
    """
    film = models.ForeignKey(
        Film, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    content = models.TextField(
        max_length=500,
        validators=[MaxLengthValidator(500)],
        help_text="Maximum 500 characters"
    )
    author_name = models.CharField(
        max_length=100,
        default="Anonymous"
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['film', 'created_at']),
        ]
    
    def __str__(self):
        return f"Comment by {self.author_name} on {self.film.title}"