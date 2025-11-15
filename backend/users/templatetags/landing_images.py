"""
Deprecated templatetag: landing_images

This templatetag was previously used to enumerate files in
`static/images/landing/`. The project now uses `hero_images` and a
config-driven approach. Keep this file until you have updated any
templates that still reference `{% landing_images %}`.

To migrate templates, replace:

    {% landing_images %}

with:

    {% load hero_images %}
    {% hero_images 3 as imgs %}

Then use `imgs` as an array of paths fed to `{% static %}`.

This file intentionally contains no runtime code.
"""
