from . import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers


router = DefaultRouter()
router.register('menu_item', views.MenuItemView)
menu_router = routers.NestedDefaultRouter(router, 'menu_item', lookup='menu_item')
menu_router.register('menu_item', views.MenuItemView, basename='menu_item')
menu_router.register('menu_category', views.MenuCategoryView)
menu_router.register('item_option', views.MenuItemOptionView)
menu_router.register('option_value', views.OptionValueView)


urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('menu/<slug:slug>/', views.MenuCategoryDetail.as_view(), name='menu'),
    path('menu/item/<slug:slug>/', views.MenuItemDetail.as_view(), name='menu_item'),
    path('staff/menu_item/create/', views.StaffCreateMenuItem.as_view(), name='staff_create_menu_item'),
    path('staff/menu_item/update/<int:pk>/', views.StaffUpdateMenuItem.as_view(), name='staff_update_menu_item'),
    path('staff/menu_item/delete/<int:pk>/', views.StaffDeleteMenuItem.as_view(), name='staff_delete_menu_item'),
    path('staff/menu_item/', views.StaffListMenuItem.as_view(), name='staff_list_menu_item'),


    path('api/', include(router.urls)),
    path('api/', include(menu_router.urls)),
]