# LUMINA_SORT: Algorithmic Editorial Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-5.0+-green)

**LUMINA_SORT** is a Django-based image manipulation engine that transforms photography into glitch-style digital art using deterministic pixel sorting instead of generative AI.

The engine rearranges pixel data using luminosity, hue, saturation, and RGB-based sort keys so the same inputs and parameters produce repeatable results.

---

## Features

- **Algorithmic pixel sorting** — horizontal or vertical interval sorting
- **Threshold masking** — target shadows, midtones, highlights, or custom ranges
- **Multiple sort criteria** — luminosity, hue, saturation, and RGB channels
- **Recipe system** — save and reuse processing configurations
- **User gallery** — store original and processed images
- **Export presets** — portrait and story-friendly output sizes
- **No generative AI** — effects come from deterministic image-processing logic

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 5 / Python |
| Processing | NumPy + Pillow |
| Database | SQLite for development, PostgreSQL-ready for production |
| Frontend | HTML5 + CSS3 |

---

## How It Works

The core engine treats an image as a three-dimensional NumPy array:

```python
image_array.shape  # (height, width, rgb_channels)
```

A simplified processing pipeline is:

1. Calculate a luminosity or color-based value for each pixel.
2. Build a threshold mask.
3. Find contiguous intervals that match the mask.
4. Sort pixels inside each interval.
5. Reconstruct the image with the sorted slices.

Example luminosity calculation:

```text
L = 0.299R + 0.587G + 0.114B
```

Example threshold mask:

```python
mask = (luminosity >= threshold_low) & (luminosity <= threshold_high)
```

Example deterministic sort:

```python
indices = np.argsort(sort_keys)
sorted_pixels = pixels[indices]
```

---

## Run Locally

### Requirements

- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/BeansDed/LUMINA_SORT.git
cd LUMINA_SORT

python -m venv venv
```

Activate the environment:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

Install dependencies and start Django:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

---

## Usage

1. Sign in or create an account.
2. Upload an image.
3. Pick a saved recipe or configure custom thresholds and sorting options.
4. Process the image.
5. Save or export the result.
6. Reuse successful settings as recipes.

---

## Production Configuration

Typical environment variables:

```bash
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgres://user:pass@host:5432/dbname
```

Keep real secrets out of version control and configure them through your deployment environment.

---

## Core Idea

LUMINA_SORT explores how traditional algorithms can produce visually complex results without relying on a neural network. The project combines image processing, deterministic sorting, web application development, and reusable creative workflows.
