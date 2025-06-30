from django import template
from django.utils.timesince import timesince
from django.utils.timezone import now

register = template.Library()

@register.filter(name="time_delta")
def time_delta(value):
    if not value:
        return ""
    
    delta = now() - value
    seconds = delta.total_seconds()

    if seconds < 60:
        return "Just now."
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes}m ago."
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours}h ago."
    elif seconds < 604800:
        days = int(seconds // 86400)
        return f"{days}d ago."
    else:
        return value.strftime("%b %d") 