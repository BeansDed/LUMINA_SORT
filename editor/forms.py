"""
LUMINA_SORT Forms
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AestheticRecipe, ArtPiece


class SignUpForm(UserCreationForm):
    """User registration form."""
    email = forms.EmailField(max_length=254, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ImageUploadForm(forms.Form):
    """Form for uploading images to process."""
    image = forms.ImageField(
        label='Select Image',
        help_text='Upload a photograph to transform'
    )
    title = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Untitled'})
    )


class ProcessingForm(forms.Form):
    """Form for setting pixel sorting parameters."""
    DIRECTION_CHOICES = [
        ('V', 'Vertical'),
        ('H', 'Horizontal'),
    ]
    
    SORT_BY_CHOICES = [
        ('L', 'Luminosity'),
        ('H', 'Hue'),
        ('S', 'Saturation'),
        ('R', 'Red Channel'),
        ('G', 'Green Channel'),
        ('B', 'Blue Channel'),
    ]
    
    threshold_low = forms.FloatField(
        min_value=0.0,
        max_value=1.0,
        initial=0.25,
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '0',
            'max': '1',
            'step': '0.01',
            'class': 'slider'
        }),
        label='Threshold Low'
    )
    
    threshold_high = forms.FloatField(
        min_value=0.0,
        max_value=1.0,
        initial=0.80,
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '0',
            'max': '1',
            'step': '0.01',
            'class': 'slider'
        }),
        label='Threshold High'
    )
    
    sort_direction = forms.ChoiceField(
        choices=DIRECTION_CHOICES,
        initial='V',
        widget=forms.RadioSelect(attrs={'class': 'radio-group'})
    )
    
    sort_by = forms.ChoiceField(
        choices=SORT_BY_CHOICES,
        initial='L',
        widget=forms.Select(attrs={'class': 'select-input'})
    )
    
    reverse_sort = forms.BooleanField(
        required=False,
        initial=False,
        label='Reverse Sort Order'
    )
    
    recipe = forms.ModelChoiceField(
        queryset=AestheticRecipe.objects.filter(is_public=True),
        required=False,
        empty_label="-- Use Custom Settings --",
        label='Or Use a Recipe'
    )


class RecipeForm(forms.ModelForm):
    """Form for creating/editing recipes."""
    
    class Meta:
        model = AestheticRecipe
        fields = [
            'name', 'description', 'threshold_low', 'threshold_high',
            'sort_direction', 'sort_by', 'reverse_sort', 'is_public'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Cyberpunk Melt'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the visual effect...'}),
            'threshold_low': forms.NumberInput(attrs={
                'type': 'range', 'min': '0', 'max': '1', 'step': '0.01', 'class': 'slider'
            }),
            'threshold_high': forms.NumberInput(attrs={
                'type': 'range', 'min': '0', 'max': '1', 'step': '0.01', 'class': 'slider'
            }),
            'sort_direction': forms.RadioSelect(),
            'sort_by': forms.Select(attrs={'class': 'select-input'}),
        }
