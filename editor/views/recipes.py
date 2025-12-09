"""
Recipe views - Create, list, and save recipes.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import AestheticRecipe, ArtPiece
from ..forms import RecipeForm


def recipes_list(request):
    """Public recipes listing."""
    recipes = AestheticRecipe.objects.filter(is_public=True)
    return render(request, 'editor/recipes.html', {'recipes': recipes})


@login_required
def create_recipe(request):
    """Create a new recipe."""
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.creator = request.user
            recipe.save()
            messages.success(request, f'Recipe "{recipe.name}" created!')
            return redirect('recipes')
    else:
        form = RecipeForm()
    return render(request, 'editor/create_recipe.html', {'form': form})


@login_required
def save_as_recipe(request, art_id):
    """Save current art piece settings as a recipe."""
    art_piece = get_object_or_404(ArtPiece, id=art_id, user=request.user)
    params = art_piece.get_effective_params()
    
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.creator = request.user
            recipe.save()
            messages.success(request, f'Recipe "{recipe.name}" saved!')
            return redirect('result', art_id=art_id)
    else:
        initial_data = {
            'threshold_low': params['threshold_low'],
            'threshold_high': params['threshold_high'],
            'sort_direction': params['sort_direction'],
            'sort_by': params['sort_by'],
            'reverse_sort': params['reverse_sort'],
        }
        form = RecipeForm(initial=initial_data)
    
    return render(request, 'editor/save_recipe.html', {
        'form': form,
        'art_piece': art_piece
    })
