"""
Export utilities for social media formats.
"""
from PIL import Image
from .sorter import PixelSorter


def crop_for_instagram(image: Image.Image, aspect_ratio: str) -> Image.Image:
    """
    Crop/resize image for Instagram formats.
    
    Args:
        image: PIL Image to process
        aspect_ratio: 'story' (9:16) or 'post' (4:5)
    Returns:
        Cropped and resized PIL Image
    """
    width, height = image.size
    
    if aspect_ratio == 'story':
        target_ratio = 9 / 16
        target_size = (1080, 1920)
    else:
        target_ratio = 4 / 5
        target_size = (1080, 1350)
    
    current_ratio = width / height
    
    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        image = image.crop((left, 0, left + new_width, height))
    elif current_ratio < target_ratio:
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        image = image.crop((0, top, width, top + new_height))
    
    return image.resize(target_size, Image.Resampling.LANCZOS)


def process_image(
    image: Image.Image,
    threshold_low: float = 0.25,
    threshold_high: float = 0.80,
    sort_direction: str = 'V',
    sort_by: str = 'L',
    reverse_sort: bool = False
) -> Image.Image:
    """
    Main processing function - applies pixel sorting.
    
    Args:
        image: PIL Image to process
        threshold_low: Lower brightness threshold (0-1)
        threshold_high: Upper brightness threshold (0-1)
        sort_direction: 'H' or 'V'
        sort_by: Sorting criterion
        reverse_sort: Descending order
    Returns:
        Processed PIL Image
    """
    sorter = PixelSorter(image)
    sorted_array = sorter.sort(
        threshold_low=threshold_low,
        threshold_high=threshold_high,
        sort_direction=sort_direction,
        sort_by=sort_by,
        reverse_sort=reverse_sort
    )
    return sorter.to_image(sorted_array)
