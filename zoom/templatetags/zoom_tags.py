from django import template
from ..models import ZoomMeeting
import datetime
from django.utils import timezone

register = template.Library()

@register.filter
def add_hour(value, arg):
    return value + datetime.timedelta(minutes=arg)

@register.simple_tag
def same_today(date):
    if not date:
        return False
    return date.date() == timezone.now().date()

@register.simple_tag
def compare_date(date, arg):
    if not date and not arg:
        return False
    print(arg)
    return date.date() == datetime.datetime.strptime(arg,'Y-m-dTH:M:S.000Z').date()

