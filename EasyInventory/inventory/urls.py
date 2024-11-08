from django.urls import path
from . import views

urlpatterns = [
    path('administrator/inventory', views.inventory_list, name='admin_inventory'),
    path('administrator/users', views.user_list, name='admin_users'),
    path('administrator/new_equipment', views.new_equipment, name='new_equipment'),
    path('administrator/check_out', views.checkout_requests, name='checkout_requests'),
    path('administrator/check_in', views.check_in, name='check_in'),
    path('administrator/user_action/<int:user_id>', views.user_action, name='user_action'),  # User actions
    path('user/equipment', views.user_equipment, name='user_equipment'),
    path('user/checkout', views.user_checkout, name='user_checkout'),
]
