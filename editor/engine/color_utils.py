"""
Color calculation utilities for pixel sorting.
Handles luminosity, hue, and saturation computations.
"""
import numpy as np


def calculate_luminosity(pixels: np.ndarray) -> np.ndarray:
    """
    Calculate perceived luminosity: L = 0.299*R + 0.587*G + 0.114*B
    
    Args:
        pixels: Array with RGB values in [0, 1], shape (..., 3)
    Returns:
        Luminosity values in [0, 1]
    """
    return 0.299 * pixels[..., 0] + 0.587 * pixels[..., 1] + 0.114 * pixels[..., 2]


def calculate_hue(pixels: np.ndarray) -> np.ndarray:
    """
    Calculate hue component from RGB values.
    
    Args:
        pixels: Array with RGB values in [0, 1], shape (..., 3)
    Returns:
        Hue values in [0, 1]
    """
    r, g, b = pixels[..., 0], pixels[..., 1], pixels[..., 2]
    
    max_val = np.maximum(np.maximum(r, g), b)
    min_val = np.minimum(np.minimum(r, g), b)
    delta = max_val - min_val
    
    hue = np.zeros_like(max_val)
    mask = delta > 0
    
    # Red is max
    red_max = mask & (max_val == r)
    hue[red_max] = ((g[red_max] - b[red_max]) / delta[red_max]) % 6
    
    # Green is max
    green_max = mask & (max_val == g)
    hue[green_max] = (b[green_max] - r[green_max]) / delta[green_max] + 2
    
    # Blue is max
    blue_max = mask & (max_val == b)
    hue[blue_max] = (r[blue_max] - g[blue_max]) / delta[blue_max] + 4
    
    return hue / 6.0


def calculate_saturation(pixels: np.ndarray) -> np.ndarray:
    """
    Calculate saturation component from RGB values.
    
    Args:
        pixels: Array with RGB values in [0, 1], shape (..., 3)
    Returns:
        Saturation values in [0, 1]
    """
    max_val = np.max(pixels, axis=-1)
    min_val = np.min(pixels, axis=-1)
    delta = max_val - min_val
    
    saturation = np.zeros_like(max_val)
    mask = max_val > 0
    saturation[mask] = delta[mask] / max_val[mask]
    
    return saturation


def get_sort_key(pixels: np.ndarray, sort_by: str) -> np.ndarray:
    """
    Get values to sort by based on criterion.
    
    Args:
        pixels: Array of shape (N, 3) with RGB values
        sort_by: 'L', 'H', 'S', 'R', 'G', or 'B'
    Returns:
        1D array of sort key values
    """
    sort_map = {
        'L': lambda p: calculate_luminosity(p),
        'H': lambda p: calculate_hue(p),
        'S': lambda p: calculate_saturation(p),
        'R': lambda p: p[:, 0],
        'G': lambda p: p[:, 1],
        'B': lambda p: p[:, 2],
    }
    return sort_map.get(sort_by, sort_map['L'])(pixels)


def create_mask(line: np.ndarray, threshold_low: float, threshold_high: float) -> np.ndarray:
    """
    Create boolean mask for pixels within threshold range.
    
    Args:
        line: 1D array of pixel values
        threshold_low: Lower bound (0-1)
        threshold_high: Upper bound (0-1)
    Returns:
        Boolean mask
    """
    return (line >= threshold_low) & (line <= threshold_high)


def find_intervals(mask: np.ndarray) -> list:
    """
    Find contiguous intervals of True values.
    
    Args:
        mask: Boolean array
    Returns:
        List of (start, end) tuples
    """
    intervals = []
    in_interval = False
    start = 0
    
    for i, val in enumerate(mask):
        if val and not in_interval:
            start = i
            in_interval = True
        elif not val and in_interval:
            intervals.append((start, i))
            in_interval = False
    
    if in_interval:
        intervals.append((start, len(mask)))
    
    return intervals
