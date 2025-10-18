from django.contrib import admin
from .models import Film, Comment


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['title', 'episode_id', 'release_date', 'director', 'comment_count']
    list_filter = ['release_date', 'director']
    search_fields = ['title', 'director', 'opening_crawl']
    readonly_fields = ['swapi_id', 'created', 'updated', 'comment_count']
    ordering = ['release_date']
    
    fieldsets = (
        ('Film Information', {
            'fields': ('title', 'episode_id', 'swapi_id')
        }),
        ('Details', {
            'fields': ('opening_crawl', 'director', 'producer', 'release_date')
        }),
        ('Metadata', {
            'fields': ('comment_count', 'created', 'updated'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'film', 'author_name', 'content_preview', 'created_at']
    list_filter = ['created_at', 'film']
    search_fields = ['content', 'author_name']
    readonly_fields = ['ip_address', 'created_at']
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'