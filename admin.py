# blog/admin.py

from django.contrib import admin
from .models import Post, Category, Comment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Number of empty forms to display

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}  # If you have a slug field
    inlines = [CommentInline]  # Display comments inline in the post admin

# Register the models with the admin site
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)