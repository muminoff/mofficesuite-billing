from django.core.urlresolvers import resolve
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _ 


def sidebar(request):
    if request.user.is_authenticated and request.user.is_staff:
        menus = OrderedDict([
            ('services_page', {'title': 'Services', 'icon': 'services'}),
            ])
    else:
        menus = OrderedDict([
            ('services_page', {'title': 'Services', 'icon': 'services'}),
            ('account_page', {'title': 'Account', 'icon': 'user'}),
            ('billing_page', {'title': 'Billing', 'icon': 'bill'}),
            ('support_page', {'title': 'Support', 'icon': 'support'}),
            ])


    try: 
        name = resolve(request.path).url_name
        if name in menus:
            menus[name]['active'] = True 
    except:
        pass

    return {
            'menus': menus,
            }