from django.template import Library
import datetime
from django.utils import timezone

register = Library()


@register.filter(expects_localtime=True)
def parse_iso_days(value):
    start = value.create_date
    end = value.complete_date
    result = end-start
    return result.days
