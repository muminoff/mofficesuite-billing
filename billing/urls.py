from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', TemplateView.as_view(template_name='base.html')),

    # Examples:
    # url(r'^$', 'billing.views.home', name='home'),
    # url(r'^billing/', include('billing.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'core.views.index_page', name='index_page'),
    url(r'^login/$', 'core.views.login_page', name='login_page'),
    url(r'^logout/$', 'core.views.logout_page', name='logout_page'),
    url(r'^signup/$', 'core.views.signup_page', name='signup_page'),
    url(r'^services/$', 'core.views.services_page', name='services_page'),
    url(r'^account/$', 'core.views.account_page', name='account_page'),
    url(r'^billing/$', 'core.views.billing_page', name='billing_page'),
    url(r'^support/$', 'core.views.support_page', name='support_page'),
    url(r'^feedback/$', 'core.views.feedback_page', name='feedback_page'),
    url(r'^payment/$', 'core.views.payment_page', name='payment_page'),
    url(r'^security/$', 'core.views.security_settings_page', name='security_settings_page'),
    url(r'^service/add/$', 'core.views.service_add_page', name='service_add_page'),
    url(r'^ticket/add/$', 'core.views.ticket_add_page', name='ticket_add_page'),
    url(r'^admin/', include(admin.site.urls)),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
