from django import template


register = template.Library()


@register.inclusion_tag('list_cats.html')
def show_categories():
    return {}
