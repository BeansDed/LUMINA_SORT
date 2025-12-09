"""
Public views - Home and public gallery.
"""
from django.shortcuts import render
from ..models import AestheticRecipe, ArtPiece


def home(request):
    """Landing page with recent art and popular recipes."""
    recent_art = ArtPiece.objects.filter(
        is_public=True, 
        processed_image__isnull=False
    )[:6]
    popular_recipes = AestheticRecipe.objects.filter(is_public=True)[:5]
    
    return render(request, 'editor/home.html', {
        'recent_art': recent_art,
        'popular_recipes': popular_recipes,
    })


def public_gallery(request):
    """Public gallery of shared art pieces."""
    art_pieces = ArtPiece.objects.filter(
        is_public=True, 
        processed_image__isnull=False
    )
    return render(request, 'editor/public_gallery.html', {'art_pieces': art_pieces})
