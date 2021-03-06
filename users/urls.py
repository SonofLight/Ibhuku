from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from users.views import create_user_acccount, user_activation_sent,  confirm_activation_link, resend_activation_link, reset_activation_sent_confirmed_account

urlpatterns = [
    url(r'^$', RedirectView.as_view(
        url=reverse_lazy('users:register')), name='index'),
    url(r'^register/$', create_user_acccount, name='register'),
    url(r'^register/activation/$', user_activation_sent, name='activation-sent'),
    url(r'^activation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        confirm_activation_link, name='activate'),
    url(r'^reset/$', resend_activation_link, name='activation-reset'),
    url(r'^reset/confirm/$', reset_activation_sent_confirmed_account,
        name='activation-exists'),
]
