"""badge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static

from registration.backends.simple.views import RegistrationView

from main.views import HomePage, ModelView, badge_list, UserForm

urlpatterns = [
    url(r'^$', login_required(HomePage.as_view()), name="homepage"),
    url(r'^models/(?P<model_id>[0-9]+)$',
        login_required(ModelView.as_view()), name="model.view"),
    url(r'^badges', login_required(badge_list), name="badges"),

    url(r'^logout$', auth_views.logout, {'next_page': '/'}),
    url(r'^accounts/register/$',
        RegistrationView.as_view(form_class=UserForm),
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
