"""
LUMINA_SORT URL Configuration
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home, public_gallery, signup, gallery, delete_art, toggle_public,
    upload, process, result, export_image, recipes_list, create_recipe, save_as_recipe
)

urlpatterns = [
    # Home
    path('', home, name='home'),
    
    # Authentication
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='editor/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Image workflow
    path('upload/', upload, name='upload'),
    path('process/<int:art_id>/', process, name='process'),
    path('result/<int:art_id>/', result, name='result'),
    path('export/<int:art_id>/<str:format_type>/', export_image, name='export'),
    
    # Gallery
    path('gallery/', gallery, name='gallery'),
    path('gallery/public/', public_gallery, name='public_gallery'),
    path('delete/<int:art_id>/', delete_art, name='delete_art'),
    path('toggle-public/<int:art_id>/', toggle_public, name='toggle_public'),
    
    # Recipes
    path('recipes/', recipes_list, name='recipes'),
    path('recipes/create/', create_recipe, name='create_recipe'),
    path('recipes/save/<int:art_id>/', save_as_recipe, name='save_recipe'),
]
