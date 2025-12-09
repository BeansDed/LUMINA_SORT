"""
Image processing views - Upload, process, result, export.
"""
import uuid
from io import BytesIO

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.base import ContentFile
from PIL import Image

from ..models import AestheticRecipe, ArtPiece
from ..forms import ImageUploadForm, ProcessingForm
from ..engine import process_image, crop_for_instagram


@login_required
def upload(request):
    """Image upload view."""
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            art_piece = ArtPiece.objects.create(
                user=request.user,
                title=form.cleaned_data.get('title') or 'Untitled',
                original_image=form.cleaned_data['image']
            )
            return redirect('process', art_id=art_piece.id)
    else:
        form = ImageUploadForm()
    return render(request, 'editor/upload.html', {'form': form})


@login_required
def process(request, art_id):
    """Image processing view with parameter controls."""
    art_piece = get_object_or_404(ArtPiece, id=art_id, user=request.user)
    
    if request.method == 'POST':
        form = ProcessingForm(request.POST)
        if form.is_valid():
            params = _extract_params(form, art_piece)
            try:
                _process_and_save(art_piece, params)
                messages.success(request, 'Image processed successfully!')
                return redirect('result', art_id=art_piece.id)
            except Exception as e:
                messages.error(request, f'Processing error: {str(e)}')
    else:
        form = ProcessingForm()
    
    return render(request, 'editor/process.html', {
        'form': form,
        'art_piece': art_piece,
        'recipes': AestheticRecipe.objects.filter(is_public=True)[:10]
    })


def _extract_params(form, art_piece):
    """Extract processing parameters from form or recipe."""
    recipe = form.cleaned_data.get('recipe')
    
    if recipe:
        art_piece.recipe_used = recipe
        recipe.increment_usage()
        return {
            'threshold_low': recipe.threshold_low,
            'threshold_high': recipe.threshold_high,
            'sort_direction': recipe.sort_direction,
            'sort_by': recipe.sort_by,
            'reverse_sort': recipe.reverse_sort,
        }
    
    art_piece.custom_threshold_low = form.cleaned_data['threshold_low']
    art_piece.custom_threshold_high = form.cleaned_data['threshold_high']
    art_piece.custom_sort_direction = form.cleaned_data['sort_direction']
    art_piece.custom_sort_by = form.cleaned_data['sort_by']
    
    return {
        'threshold_low': form.cleaned_data['threshold_low'],
        'threshold_high': form.cleaned_data['threshold_high'],
        'sort_direction': form.cleaned_data['sort_direction'],
        'sort_by': form.cleaned_data['sort_by'],
        'reverse_sort': form.cleaned_data['reverse_sort'],
    }


def _process_and_save(art_piece, params):
    """Process image and save result."""
    with Image.open(art_piece.original_image.path) as img:
        processed = process_image(img, **params)
        
        buffer = BytesIO()
        processed.save(buffer, format='PNG', quality=95)
        buffer.seek(0)
        
        filename = f"processed_{uuid.uuid4().hex[:8]}.png"
        art_piece.processed_image.save(filename, ContentFile(buffer.read()), save=False)
        art_piece.save()


@login_required
def result(request, art_id):
    """Display the processed result."""
    art_piece = get_object_or_404(ArtPiece, id=art_id, user=request.user)
    return render(request, 'editor/result.html', {'art_piece': art_piece})


@login_required
def export_image(request, art_id, format_type):
    """Export image for Instagram formats."""
    art_piece = get_object_or_404(ArtPiece, id=art_id, user=request.user)
    
    if not art_piece.processed_image:
        messages.error(request, 'No processed image to export.')
        return redirect('result', art_id=art_id)
    
    try:
        return _create_export(art_piece, format_type)
    except Exception as e:
        messages.error(request, f'Export error: {str(e)}')
        return redirect('result', art_id=art_id)


def _create_export(art_piece, format_type):
    """Create and return export file."""
    with Image.open(art_piece.processed_image.path) as img:
        cropped = crop_for_instagram(img, format_type)
        field = 'export_story' if format_type == 'story' else 'export_post'
        
        buffer = BytesIO()
        cropped.save(buffer, format='PNG', quality=95)
        buffer.seek(0)
        
        filename = f"export_{format_type}_{uuid.uuid4().hex[:8]}.png"
        getattr(art_piece, field).save(filename, ContentFile(buffer.read()), save=True)
        
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
