from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag
def ref_html(ref, authors_nmax=None):
    s = ref.html_article(authors_nmax=authors_nmax)
    return mark_safe(s)
