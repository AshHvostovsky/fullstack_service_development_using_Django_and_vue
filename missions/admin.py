from django.contrib import admin

from missions.models import *

# Register your models here.
@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'launch_date', 'outcome', 'description', 'space_program__id', 'mission_type__id']

@admin.register(SpaceProgram)
class SpaceProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'description']

@admin.register(MissionType)
class MissionTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(LaunchSite)
class LaunchSiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']

@admin.register(SpaceCraft)
class SpaceCraftAdmin(admin.ModelAdmin):
    list_display = ['name', 'manufacturer', 'launch_site__id', 'mission__id']




