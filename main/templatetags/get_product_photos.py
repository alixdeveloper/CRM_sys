from django.template import Library
import json


register = Library()


@register.filter(expects_localtime=True)
def get_product_photos(product):
    photos = json.loads(product.photo)
    return photos
