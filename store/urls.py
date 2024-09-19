from django.urls import path, include
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.ProductList.as_view(), name='products'),
    path('product_detail/<int:id>/<slug>', views.post_detail, name='post_detail'),
    # favorite products url
    path('add-to-favorite/<int:id>/<slug>', views.add_to_favorite, name='add_to_favorite'),
    path('favorite-list', views.favorite_products, name='favorite_products'),
    path('remove-favorite/<int:id>/<slug>', views.remove_favorite, name='remove_favorite'),

    # contact us

    path('contact-us', views.contact_us, name='contact_us'),

    # Search

    path('product-search/', views.product_search, name='product_search'),
]