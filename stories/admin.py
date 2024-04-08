from django.contrib import admin
from stories.models import *
# Register your models here.
@admin.register(Editor)
class EditorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')

@admin.register(Stories)
class StoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'editor')