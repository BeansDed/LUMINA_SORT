# LUMINA_SORT: Algorithmic Editorial Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-5.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**LUMINA_SORT** is a Django-based image manipulation engine that transforms standard photography into high-fashion, glitch-aesthetic digital art.

Unlike modern AI filters that "guess" pixels, LUMINA_SORT uses **deterministic sorting algorithms** to physically rearrange the pixel data of an image based on luminosity, hue, and saturation values. It is designed for creative developers and digital artists who want precise control over the chaos.

---

## 📸 Features

- **Algorithmic Sorting**: Implements custom sorting logic to "melt" pixels in vertical or horizontal intervals
- **Threshold Masking**: Users can define specific "mask" ranges (e.g., "only sort the highlights" or "only sort the shadows")
- **Recipe Database**: A SQLite/PostgreSQL backend that stores parameter combinations, allowing users to save and reuse their favorite "glitch settings"
- **Social Optimization**: Auto-resizing for Instagram Story (9:16) and Portrait Post (4:5) formats
- **User Gallery**: Personal galleries with public/private visibility controls

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | Django 5.0 (Python) |
| **Processing** | NumPy & Pillow (PIL) — No AI/Neural Networks |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) |
| **Frontend** | HTML5 / CSS3 — Minimal black/white aesthetic |

---

## 🧮 How It Works (The Math)

The core engine treats an image as a **3-Dimensional NumPy array** `(Height, Width, RGB Channels)`.

```
Image → np.array(image) → shape: (H, W, 3)
```

### The Algorithm:

1. **Calculate Luminosity Mask**
   ```
   L = 0.299R + 0.587G + 0.114B
   ```

2. **Create Threshold Mask**
   ```python
   mask = (luminosity >= threshold_low) & (luminosity <= threshold_high)
   ```

3. **Find Contiguous Intervals**
   - Scan each row (horizontal) or column (vertical)
   - Identify sequences of pixels that fall within the mask

4. **Sort Intervals**
   ```python
   indices = np.argsort(sort_keys)  # Deterministic sorting
   sorted_pixels = pixels[indices]
   ```

5. **Reconstruct Image**
   - Place sorted slices back into the original array
   - This creates the signature "melting" or "streaking" effect

### Sorting Criteria:
- **Luminosity** (brightness)
- **Hue** (color wheel position)
- **Saturation** (color intensity)
- **Individual RGB channels**

---

## 🚀 Setup

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/lumina_sort.git
cd lumina_sort

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## 📁 Project Structure

```
lumina_sort/
├── lumina_sort/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── editor/               # Main application
│   ├── models.py         # AestheticRecipe, ArtPiece
│   ├── views.py          # Upload, Process, Gallery views
│   ├── pixel_sorter.py   # Core sorting engine
│   ├── forms.py
│   └── urls.py
├── templates/            # HTML templates
│   ├── base.html
│   └── editor/
├── static/
│   └── css/
│       └── style.css     # Minimal B&W aesthetic
├── media/                # User uploads (gitignored)
│   ├── originals/
│   ├── processed/
│   └── exports/
├── manage.py
├── requirements.txt
└── README.md
```

---

## 📊 Database Schema

### AestheticRecipe
Stores reusable sorting configurations.

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField | Recipe name (e.g., "Cyberpunk Melt") |
| `threshold_low` | FloatField | Lower brightness bound (0-1) |
| `threshold_high` | FloatField | Upper brightness bound (0-1) |
| `sort_direction` | CharField | 'H' (Horizontal) or 'V' (Vertical) |
| `sort_by` | CharField | L/H/S/R/G/B |
| `times_used` | IntegerField | Usage counter |
| `is_public` | BooleanField | Visibility flag |

### ArtPiece
Stores user uploads and processed results.

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | Owner reference |
| `original_image` | ImageField | Source photograph |
| `processed_image` | ImageField | Sorted result |
| `export_story` | ImageField | 9:16 export |
| `export_post` | ImageField | 4:5 export |
| `recipe_used` | ForeignKey | Applied recipe (nullable) |

---

## 🎨 Usage

1. **Sign Up / Login** to create an account
2. **Upload** any photograph
3. **Configure** sorting parameters:
   - Choose a pre-made recipe, OR
   - Set custom thresholds, direction, and sort criteria
4. **Process** the image
5. **Export** for Instagram Story or Post
6. **Save** your settings as a new recipe for reuse

---

## 🔧 Configuration

### Environment Variables (Production)

```bash
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgres://user:pass@host:5432/dbname
```

### PostgreSQL (Production)

Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lumina_sort',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 📜 License

MIT License — See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ✨ Credits

Built with pure algorithmic mathematics. No AI. No neural networks. Just deterministic pixel manipulation.

**LUMINA_SORT** — *Where mathematics meets fashion.*
