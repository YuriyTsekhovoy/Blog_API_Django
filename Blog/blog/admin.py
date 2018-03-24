from django.contrib import admin
from .models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["author", "title", "created_date", "published_date"]
    list_display_links = ["title", ]
    #list_editable = ["title"]
    #list_filter = ["updated", "timestamp"]
#
    search_fields = ["author", "title", "text"]

    class Meta:
        model = Post




admin.site.register(Post, PostModelAdmin)