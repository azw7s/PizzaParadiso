"""
URL configuration for aa_pizza project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from customer.views import SignUpView
from django.contrib.auth.views import LogoutView
from customer.views import CustomLogin
from menu.views import redirect_to_home


urlpatterns = [
    path('', redirect_to_home),
    path('admin/', admin.site.urls),
    path('', include('customer.urls')),
    path('', include('menu.urls')),
    path('', include('order.urls')),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', CustomLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
