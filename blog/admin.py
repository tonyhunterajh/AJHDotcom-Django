from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'date_posted', 'status')
    list_filter = ('author', 'date_posted', 'date_created', 'status')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'date_posted'
    ordering = ('status', 'date_posted')
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_date', 'approved_comment')
    list_filter = ('author', 'created_date', 'text')
    search_fields = ('text',)
    date_hierarchy = 'created_date'
    ordering = ('approved_comment', 'created_date')