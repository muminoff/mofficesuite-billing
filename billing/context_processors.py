from django.core.urlresolvers import resolve
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _ 


def sidebar(request):
    if request.user.is_authenticated and request.user.is_crew:
        menus = OrderedDict([
            ('services_page', {'title': 'Services', 'icon': 'cloud'}),
            ('account_page', {'title': 'Account', 'icon': 'profile-male'}),
            ('billing_page', {'title': 'Billing', 'icon': 'wallet'}),
            # ('support_page', {'title': 'Support', 'icon': 'support'}),
            ('security_page', {'title': 'Security', 'icon': 'lock'}),
            ('notifications_page', {'title': 'Notifications', 'icon': 'megaphone'}),
            ('settings_page', {'title': 'Settings', 'icon': 'adjustments'}),
            ])
    else:
        menus = OrderedDict([
            ('services_page', {'title': 'Services', 'icon': 'cloud'}),
            ('account_page', {'title': 'Account', 'icon': 'profile-male'}),
            ('billing_page', {'title': 'Billing', 'icon': 'wallet'}),
            # ('support_page', {'title': 'Support', 'icon': 'support'}),
            ('security_page', {'title': 'Security', 'icon': 'lock'}),
            ('notifications_page', {'title': 'Notifications', 'icon': 'megaphone'}),
            ('settings_page', {'title': 'Settings', 'icon': 'adjustments'}),
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
