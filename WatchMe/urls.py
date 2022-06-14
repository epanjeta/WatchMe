"""WatchMe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path
from watch.views import details_view
from pages.views import home_view, about_view, contact_view
from accounts.views import register_view, login_view, logout, myProfile_view, editProfile_view, editProfilePassword_view
from cart.views import add_to_cart, cart_view, checkout_view, remove_from_cart
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('products/', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', myProfile_view, name='profile'),
    path('profile/edit', editProfile_view, name='edit_profile'),
    path('profile/edit/password', editProfilePassword_view, name='edit_password'),
    path('products/<int:productId>', details_view, name='details'),
    path('add/<int:productId>', add_to_cart, name='add_item'),
    path('cart/', cart_view, name='cart'),
    path('checkout', checkout_view, name='checkout'),
    path('remove/<int:productId>', remove_from_cart, name='remove_item')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
