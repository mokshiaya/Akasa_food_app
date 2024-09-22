# food_app/urls.py
from django.contrib import admin
from django.urls import path
from akasa.views import register, user_login, home, browse_items, add_to_cart, view_cart, checkout, order_history, remove_from_cart
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_login, name='login'),
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('browse/', browse_items, name='browse_items'), 
    path('browse/<str:category>/', browse_items, name='browse_items_with_category'),  
    path('add-to-cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('view-cart/', view_cart, name='view_cart'),
    # path('cart/', view_cart, name='view_cart'),  # Add this line
    path('checkout/', checkout, name='checkout'),
    path('order-history/', order_history, name='order_history'),
    path('browse/all/', browse_items, {'category': 'all'}, name='browse_items_all'), 
    path('browse/all/', browse_items, name='browse_items_all'),  
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),


]
