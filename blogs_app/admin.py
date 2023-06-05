from django.contrib import admin
from django.core.paginator import Paginator
from . import models


class ArticleSettings(admin.ModelAdmin):
    list_display = ("title", "created_at")
    list_per_page = 10


admin.site.register(models.UserAccount)
admin.site.register(models.Articles, ArticleSettings)
admin.site.register(models.ImagesTitle)
admin.site.register(models.Categories)
admin.site.register(models.Comments)
admin.site.register(models.WatchListCategories)
