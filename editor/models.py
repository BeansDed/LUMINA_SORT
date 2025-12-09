"""
LUMINA_SORT Database Models
Stores Aesthetic Recipes and Art Pieces
"""
from django.db import models
from django.contrib.auth.models import User


class AestheticRecipe(models.Model):
    """
    Stores the "recipe" - the specific math settings used to generate glitch art.
    Users can save and share their favorite combinations.
    """
    DIRECTION_CHOICES = [
        ('H', 'Horizontal'),
        ('V', 'Vertical'),
    ]
    
    SORT_BY_CHOICES = [
        ('L', 'Luminosity'),
        ('H', 'Hue'),
        ('S', 'Saturation'),
        ('R', 'Red Channel'),
        ('G', 'Green Channel'),
        ('B', 'Blue Channel'),
    ]
    
    name = models.CharField(max_length=100, help_text="e.g., 'Cyberpunk Melt'")
    description = models.TextField(blank=True, help_text="Describe the visual effect")
    
    # Core sorting parameters
    threshold_low = models.FloatField(default=0.25, help_text="Lower brightness threshold (0-1)")
    threshold_high = models.FloatField(default=0.80, help_text="Upper brightness threshold (0-1)")
    sort_direction = models.CharField(max_length=1, choices=DIRECTION_CHOICES, default='V')
    sort_by = models.CharField(max_length=1, choices=SORT_BY_CHOICES, default='L')
    
    # Advanced settings
    interval_random = models.BooleanField(default=False, help_text="Randomize sorting intervals")
    reverse_sort = models.BooleanField(default=False, help_text="Sort in descending order")
    
    # Metadata
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_public = models.BooleanField(default=True, help_text="Allow others to use this recipe")
    times_used = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-times_used', '-created_at']
        verbose_name = "Aesthetic Recipe"
        verbose_name_plural = "Aesthetic Recipes"
    
    def __str__(self):
        return f"{self.name} ({self.get_sort_direction_display()}, {self.get_sort_by_display()})"
    
    def increment_usage(self):
        self.times_used += 1
        self.save(update_fields=['times_used'])


class ArtPiece(models.Model):
    """
    Stores the original and processed images along with the recipe used.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='art_pieces')
    title = models.CharField(max_length=200, blank=True)
    
    # Images
    original_image = models.ImageField(upload_to='originals/')
    processed_image = models.ImageField(upload_to='processed/', blank=True, null=True)
    
    # Export versions
    export_story = models.ImageField(upload_to='exports/story/', blank=True, null=True)  # 9:16
    export_post = models.ImageField(upload_to='exports/post/', blank=True, null=True)    # 4:5
    
    # Recipe used
    recipe_used = models.ForeignKey(
        AestheticRecipe, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='art_pieces'
    )
    
    # Custom parameters (if not using a saved recipe)
    custom_threshold_low = models.FloatField(null=True, blank=True)
    custom_threshold_high = models.FloatField(null=True, blank=True)
    custom_sort_direction = models.CharField(max_length=1, blank=True)
    custom_sort_by = models.CharField(max_length=1, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Art Piece"
        verbose_name_plural = "Art Pieces"
    
    def __str__(self):
        return f"{self.title or 'Untitled'} by {self.user.username}"
    
    def get_effective_params(self):
        """Returns the actual parameters used, whether from recipe or custom."""
        if self.recipe_used:
            return {
                'threshold_low': self.recipe_used.threshold_low,
                'threshold_high': self.recipe_used.threshold_high,
                'sort_direction': self.recipe_used.sort_direction,
                'sort_by': self.recipe_used.sort_by,
                'reverse_sort': self.recipe_used.reverse_sort,
            }
        return {
            'threshold_low': self.custom_threshold_low or 0.25,
            'threshold_high': self.custom_threshold_high or 0.80,
            'sort_direction': self.custom_sort_direction or 'V',
            'sort_by': self.custom_sort_by or 'L',
            'reverse_sort': False,
        }
