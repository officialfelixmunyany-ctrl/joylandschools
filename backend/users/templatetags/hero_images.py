from django import template
from django.conf import settings
import os

register = template.Library()

@register.simple_tag
def hero_images(limit=3):
    """Return up to `limit` image paths found in static/images/hero/ as relative static paths.
    Use by dropping images into `static/images/hero/`.
    """
    images = []
    static_dirs = getattr(settings, 'STATICFILES_DIRS', [])
    candidates = []
    # check STATICFILES_DIRS first
    for d in static_dirs:
        candidates.append(os.path.join(d, 'images', 'hero'))
    # fallback to project static
    project_static = os.path.join(getattr(settings,'BASE_DIR','.'),'static','images','hero')
    candidates.append(project_static)

    for folder in candidates:
        if os.path.isdir(folder):
            for fname in sorted(os.listdir(folder)):
                if fname.lower().endswith(('.jpg','.jpeg','.png','.webp')):
                    images.append('images/hero/' + fname)
                    if len(images) >= int(limit):
                        break
        if len(images) >= int(limit):
            break
    return images
