from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.index_page', name='index_page'),
    url(r'^login/$', 'core.views.login_page', name='login_page'),
    url(r'^logout/$', 'core.views.logout_page', name='logout_page'),
    url(r'^signup/$', 'core.views.signup_page', name='signup_page'),
    url(r'^forgot-password/$', 'core.views.forgot_password_page', name='forgot_password_page'),
    url(r'^reset-password/$', 'core.views.reset_page', name='reset_page'),
    url(r'^activate/$', 'core.views.activate_page', name='activate_page'),
    url(r'^deactivate/$', 'core.views.deactivate_page', name='deactivate_page'),
    url(r'^services/$', 'core.views.services_page', name='services_page'),
    url(r'^services/add/$', 'core.views.service_add_page', name='service_add_page'),
    url(r'^service/(?P<hostname>.+)/$', 'core.views.service_edit_page', name='service_edit_page'),
    url(r'^service/(?P<hostname>.+)/delete/$', 'core.views.service_delete_page', name='service_delete_page'),
    url(r'^account/$', 'core.views.account_page', name='account_page'),
    url(r'^billing/$', 'core.views.billing_page', name='billing_page'),
    url(r'^settings/$', 'core.views.settings_page', name='settings_page'),
    url(r'^feedback/$', 'core.views.feedback_page', name='feedback_page'),
    url(r'^payment/$', 'core.views.payment_page', name='payment_page'),
    url(r'^security/$', 'core.views.security_page', name='security_page'),
    url(r'^notifications/$', 'core.views.notifications_page', name='notifications_page'),
    url(r'^invoice/$', 'core.views.invoice_page', name='invoice_page'),
)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#                             url(r'^__debug__/', include(debug_toolbar.urls)),
#                             )
