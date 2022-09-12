from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('item/<int:id>/', views.ProductPageView.as_view(), name='product'),
    path('cart/', views.CartPageView.as_view(), name='cart'),
    
    path('config/', views.stripe_config),
    path('create-checkout-session/<int:price>/<int:qty>/<str:cur>/', views.create_checkout_session),

    path('add-to-cart/', views.add_to_cart),
    path('delete-product-to-cart/', views.delete_product_to_cart),
    path('delete-to-cart/', views.delete_to_cart),
]