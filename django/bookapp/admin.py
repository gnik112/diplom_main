from django.contrib import admin
from .models import *

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'people_count', 'cost')
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 20

