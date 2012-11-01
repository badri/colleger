from django.conf.urls.defaults import *
from registration.forms import RegistrationForm
from registration.views import register

urlpatterns = patterns('siteprofiles.views',
    url(r'^accounts/register/$', register, {'backend': 'siteprofiles.regbackend.RegBackend','form_class': RegistrationForm}, name='registration_register'),
    url(r'^login/$', 'login_user'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    # todo: why can't this be r'^profile/$' ?
    url(r'^profile/detail', 'view_profile'),
    url(r'^profile/edit/$','edit_profile'),
    url(r'^colleges/add/$', 'add_college'),
    url(r'^colleges/edit/(?P<id>\d+)/$', 'edit_college'),
    url(r'^colleges/detail/(?P<id>\d+)/$', 'view_college'),
    url(r'^company/add/$', 'add_company'),
    url(r'^company/edit/(?P<id>\d+)/$', 'edit_company'),
    url(r'^company/detail/(?P<id>\d+)/$', 'view_company'),
)
