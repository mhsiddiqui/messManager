from django import template
register = template.Library()

@register.filter(name='dicValue')
def dicValue(dictionary , key=''):
# Will return value for key in dictionary
    try:
        return dictionary[key]
    except KeyError:
        return ' '
