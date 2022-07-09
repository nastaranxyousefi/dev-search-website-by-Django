from django.contrib import admin

from .models import Profile, Skill


admin.site.register(Profile)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)