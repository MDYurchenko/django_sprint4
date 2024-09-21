from django.contrib import admin
from .models import Post, Category, Location, Comment

admin.site.register(Comment)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date',
        'category',
        'author',
        'location',
        'is_published',
        'created_at'
    )
    list_editable = (
        'category',
        'author',
        'location',
        'is_published'
    )
    search_fields = ('title',
                     'text',)
    list_filter = ('category',
                   'author',
                   'location',
                   'is_published',
                   'pub_date',
                   'created_at'
                   )
    list_display_links = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'is_published',
        'created_at'
    )
    list_editable = (
        'slug',
        'is_published',
    )
    search_fields = ('title',
                     'description',
                     )
    list_filter = (
        'is_published',
    )
    list_display_links = ('title',)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('name',
                     )
    list_filter = (
        'is_published',
    )
    list_display_links = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Location, LocationAdmin)

admin.site.empty_value_display = 'Не задано'
