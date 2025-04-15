from django.contrib import admin

# Register your models here.
from .models import Suggestion

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('email', 'title', 'submitted_at')
    search_fields = ('email', 'title')