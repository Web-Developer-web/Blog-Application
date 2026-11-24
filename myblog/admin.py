from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "status",
        "is_featured",
        "views_count",
        "published_at",
        "created_at",
    )
    list_filter = ("status", "is_featured", "category", "created_at", "published_at")
    search_fields = ("title", "short_description", "content", "tags")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("views_count", "created_at", "updated_at")
    list_editable = ("status", "is_featured")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)