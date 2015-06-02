from django import template
from django.contrib.auth.models import Permission
from ..models import Mess
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.filter(name='dicValue')
def dicValue(dictionary,key):
# Will return value for key in dictionary
    try:
        return dictionary[key]
    except KeyError:
        return ' '

@register.simple_tag(takes_context=True)
def get_mess_name(context):
    if Mess.objects.filter(mess_admin=context.dicts[1]['user']).exists():
        mess = Mess.objects.get(mess_admin=context.dicts[1]['user'])
        mess_name = mess.mess_name
    else:
        mess_name = 'Mess Manager'
    return mess_name


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