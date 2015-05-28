from django import template
from django.contrib.auth.models import Permission

register = template.Library()

@register.filter(name='dicValue')
def dicValue(dictionary,key):
# Will return value for key in dictionary
    try:
        return dictionary[key]
    except KeyError:
        return ' '

@register.filter
def get_navigation(user):
    """Returns list of menu in navigation."""
    permissions = Permission.objects.filter(
        group__id__in=user.groups.values_list('id')).filter(
        content_type__app_label='navigation').order_by('id')
    navigation = list(permissions)
    return navigation


@register.filter
def get_sub_navigation(user, navigation):
    """Returns list of menu in sub navigation."""
    navigation = navigation.title() + "|"
    permissions = Permission.objects.filter(
        group__id__in=user.groups.values_list('id')).filter(
        content_type__app_label='sub_navigation').filter(
        name__startswith=navigation).order_by('id')
    navigations = list(permissions)
    return navigations