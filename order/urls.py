from . import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('cart', views.CartView)

carts_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
carts_router.register('cart_item', views.CartItemView, basename='cart_item')

urlpatterns = [

    # Cart
    path('cart/<uuid:cart_id>/', views.CartDetail.as_view(), name='cart_detail'),
    path('cart_item/create/', views.CartItemCreate.as_view(), name='cart_item_create'),
    path('update_cart_item_quantity/', views.update_cart_item_quantity,
         name='update_cart_item_quantity'),

    # Checkout & Payment
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('create_checkout_session/<uuid:cart_id>/', views.CreateCheckoutSession.as_view(),
         name='create_checkout_session'),
    path('payment/failed/', views.PaymentFailed.as_view(), name='payment_failed'),

    # Order
    path('order/placed/', views.OrderPlaced.as_view(), name='order_placed'),
    path('order/create/', views.OrderCreate.as_view(), name='order_create'),
    path('order/history/<uuid:customer_id>/', views.OrderList.as_view(), name='order_list'),
    path('order_delivered/update/', views.order_delivered_update, name='order_delivered_update'),

    # Staff
    path('staff/orders/<uuid:staff_id>/', views.OrderStaff.as_view(), name='order_staff'),

    path('api/cart/', include(carts_router.urls)),
]

