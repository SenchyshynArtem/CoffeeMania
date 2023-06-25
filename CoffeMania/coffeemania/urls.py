
from django.contrib import admin
from django.urls import path 
from user_interface.views import show_contact_page, show_main_page
from shop.views import show_shop, show_product
from basket.views import *
from user_profile.views import show_user_profile, editing_profile
from django.conf.urls.static import static
from ordering.views import ordering
from authenticate.views import *
from . import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('', show_main_page, name = 'main_page'),
    path('menu/', show_shop, name = 'menu_page'),
    path('contact/', show_contact_page, name = 'contact_page'),
    path('basket/', show_basket, name = 'basket_page'),
    path('menu/<product_pk>', show_product, name = 'product'),
    path('delete_from_basket', delete_from_basket, name = 'delete_from_basket'),
    path('registration/', show_registration, name = 'reg_page'),
    path('login/', show_login, name = 'login_page'),
    path('user_reg/', register_user, name='register'),
    path('user_log/', login_user, name='login'),
    path('change_amount/', change_amount, name='change_amount'),
    path('user_profile/', show_user_profile, name='user_profile'),
    path('editing_profile/', editing_profile, name='editing_profile'),
    path('ordering/', ordering, name='ordering'),
    path('update_basket_counter/', update_basket_counter, name='updater_count')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)