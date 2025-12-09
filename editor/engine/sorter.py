"""
Core PixelSorter class - deterministic pixel manipulation.
"""
import numpy as np
from PIL import Image
from typing import Literal

from .color_utils import (
    calculate_luminosity, get_sort_key, 
    create_mask, find_intervals
)


class PixelSorter:
    """
    Main pixel sorting engine.
    Converts images to NumPy arrays and applies sorting algorithms.
    """
    
    def __init__(self, image: Image.Image):
        """Initialize with a PIL Image."""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        self.original_image = image
        self.pixel_array = np.array(image, dtype=np.float64) / 255.0
        self.height, self.width, self.channels = self.pixel_array.shape
    
    def _sort_interval(self, pixels: np.ndarray, sort_by: str, reverse: bool = False) -> np.ndarray:
        """Sort a slice of pixels by specified key."""
        if len(pixels) <= 1:
            return pixels
        
        sort_keys = get_sort_key(pixels, sort_by)
        indices = np.argsort(sort_keys)
        
        if reverse:
            indices = indices[::-1]
        
        return pixels[indices]
    
    def _process_vertical(self, result: np.ndarray, threshold_low: float, 
                          threshold_high: float, sort_by: str, reverse: bool) -> np.ndarray:
        """Process columns for vertical sorting."""
        for x in range(self.width):
            column = result[:, x, :]
            luminosity = calculate_luminosity(column)
            mask = create_mask(luminosity, threshold_low, threshold_high)
            
            for start, end in find_intervals(mask):
                if end - start > 1:
                    result[start:end, x, :] = self._sort_interval(
                        column[start:end], sort_by, reverse
                    )
        return result
    
    def _process_horizontal(self, result: np.ndarray, threshold_low: float,
                            threshold_high: float, sort_by: str, reverse: bool) -> np.ndarray:
        """Process rows for horizontal sorting."""
        for y in range(self.height):
            row = result[y, :, :]
            luminosity = calculate_luminosity(row)
            mask = create_mask(luminosity, threshold_low, threshold_high)
            
            for start, end in find_intervals(mask):
                if end - start > 1:
                    result[y, start:end, :] = self._sort_interval(
                        row[start:end], sort_by, reverse
                    )
        return result
    
    def sort(
        self,
        threshold_low: float = 0.25,
        threshold_high: float = 0.80,
        sort_direction: Literal['H', 'V'] = 'V',
        sort_by: Literal['L', 'H', 'S', 'R', 'G', 'B'] = 'L',
        reverse_sort: bool = False
    ) -> np.ndarray:
        """
        Apply pixel sorting to the image.
        
        Args:
            threshold_low: Lower brightness threshold (0-1)
            threshold_high: Upper brightness threshold (0-1)
            sort_direction: 'H' horizontal, 'V' vertical
            sort_by: Sorting criterion
            reverse_sort: Descending order if True
        Returns:
            Sorted pixel array (H, W, RGB) with values in [0, 1]
        """
        result = self.pixel_array.copy()
        
        if sort_direction == 'V':
            return self._process_vertical(result, threshold_low, threshold_high, sort_by, reverse_sort)
        return self._process_horizontal(result, threshold_low, threshold_high, sort_by, reverse_sort)
    
    def to_image(self, pixel_array: np.ndarray) -> Image.Image:
        """Convert pixel array back to PIL Image."""
        clipped = np.clip(pixel_array * 255, 0, 255).astype(np.uint8)
        return Image.fromarray(clipped, mode='RGB')
