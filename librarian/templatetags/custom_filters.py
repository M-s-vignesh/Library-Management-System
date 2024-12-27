from django import template

register = template.Library()

@register.filter(name='input_type')
def input_type(field):
    """Returns the input type of a form field."""
    return field.field.widget.input_type