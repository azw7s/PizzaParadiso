from customer import views
from django.urls import path

urlpatterns = [
    path('customer/<uuid:customer_uuid>/', views.CustomerDetail.as_view(), name='customer_detail'),
    path('customer/update/<uuid:customer_uuid>/', views.UserUpdate.as_view(), name='user_update'),
    path('address/create/', views.AddressCreate.as_view(), name='address_create'),
    path('address/update/<int:pk>/', views.AddressUpdate.as_view(), name='address_update'),
    path('address/update/<uuid:customer_uuid>/checkout/', views.AddressCheckoutList.as_view(),
         name='address_checkout_list'),
    path('address/list/<uuid:customer_uuid>/', views.AddressList.as_view(), name='address_list'),
    path('address/delete/<int:pk>/', views.AddressDelete.as_view(), name='address_delete'),
    path('staff/<uuid:staff_uuid>/', views.StaffView.as_view(), name='staff_view'),

]
