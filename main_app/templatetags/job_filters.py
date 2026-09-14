from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def days_ago(value):
    if not value:
        return ''

    today = timezone.localdate()
    days = (today - value).days

    if days == 0:
        return 'Today'
    elif days == 1:
        return '1 day ago'
    else:
        return f'{days} days ago'
