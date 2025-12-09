"""
Gallery views - User's personal gallery management.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import ArtPiece


@login_required
def gallery(request):
    """User's personal gallery."""
    art_pieces = ArtPiece.objects.filter(user=request.user)
    return render(request, 'editor/gallery.html', {'art_pieces': art_pieces})


@login_required
def delete_art(request, art_id):
    """Delete an art piece."""
    art_piece = get_object_or_404(ArtPiece, id=art_id, user=request.user)
    if request.method == 'POST':
        art_piece.delete()
        messages.success(request, 'Art piece deleted.')
    return redirect('gallery')


@login_required
def toggle_public(request, art_id):
    """Toggle public visibility of art piece."""
    art_piece = get_object_or_404(ArtPiece, id=art_id, user=request.user)
    art_piece.is_public = not art_piece.is_public
    art_piece.save()
    return redirect('gallery')
