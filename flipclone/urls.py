from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('productDetail<int:product_id>/',views.detail,name='detail'),
    path('cartitems/',views.cart,name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cartitems/remove_product/',views.remove_product,name='remove_product'),
    path("api/search/", views.search_products, name="search_products"),
    path("login/",views.login_page,name="login"),
    path("signup/",views.signup_page,name="signup"),
    path("logout/",views.logout_page,name="logout")
]