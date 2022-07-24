from django.contrib import admin

from .models import Profile, Skill, Message


admin.site.register(Profile)
admin.site.register(Message)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)