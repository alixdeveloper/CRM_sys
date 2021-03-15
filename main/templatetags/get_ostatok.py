from django.template import Library


register = Library()


@register.filter(expects_localtime=True)
def get_ostatok(all_ostatok, id):
    return all_ostatok[id-1]
