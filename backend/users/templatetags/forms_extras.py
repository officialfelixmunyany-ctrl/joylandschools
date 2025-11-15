from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(bound_field, css_class):
    """Return the bound field rendered with the given CSS class on the widget.

    Usage in templates:
        {{ form.username|add_class:'form-control' }}

    This keeps templates concise while allowing Bootstrap classes to be applied.
    """
    try:
        return bound_field.as_widget(attrs={'class': css_class})
    except Exception:
        # If something unexpected is passed, fall back to the default rendering
        return bound_field
