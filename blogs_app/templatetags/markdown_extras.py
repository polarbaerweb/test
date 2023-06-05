from django import template
import markdown


register = template.Library()


@register.filter(name="convert_to_html")
def convert_to_html(value):
    return markdown.markdown(value)
