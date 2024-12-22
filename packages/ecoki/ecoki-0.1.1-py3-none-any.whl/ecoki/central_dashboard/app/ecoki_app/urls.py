"""ecoki_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


### DEC
from django.views.generic.base import TemplateView
from ecoki_app import views as views
import django_plotly_dash

#admin.site.index_template = 'app_admin.html'
#admin.autodiscover()

urlpatterns = [
    ### DEC
    # Home
    path('', views.view_base),
    #path('django_plotly_dash/', include('django_plotly_dash.urls')),


    # Login und Account
    path('admin/', admin.site.urls),
    path('login/', views.view_login),
    path('logout/', views.view_logout),

    # Projekte
    path('active/', include('ecoki_dashboard_active.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

