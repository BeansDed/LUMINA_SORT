"""
LUMINA_SORT Admin Configuration
"""
from django.contrib import admin
from .models import AestheticRecipe, ArtPiece


@admin.register(AestheticRecipe)
class AestheticRecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'sort_direction', 'sort_by', 'threshold_low', 'threshold_high', 'times_used', 'is_public', 'creator']
    list_filter = ['sort_direction', 'sort_by', 'is_public']
    search_fields = ['name', 'description']
    readonly_fields = ['times_used', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'creator', 'is_public')
        }),
        ('Sorting Parameters', {
            'fields': ('threshold_low', 'threshold_high', 'sort_direction', 'sort_by', 'reverse_sort')
        }),
        ('Statistics', {
            'fields': ('times_used', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ArtPiece)
class ArtPieceAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'recipe_used', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at', 'recipe_used']
    search_fields = ['title', 'user__username']
    readonly_fields = ['created_at']
    raw_id_fields = ['user', 'recipe_used']
