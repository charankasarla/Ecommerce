from django.urls import path
from .views import ProductListCreateView, LogoutView, ProductRetrieveUpdateDestroyView, BuyProductView, UserRegistrationView, BoughtProductListView,UserLoginView,ProductSearchView,ProductSortView,ProductFilterView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-retrieve-update-destroy'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('products/search/', ProductSearchView.as_view(), name='product-search'),
    path('products/sort/', ProductSortView.as_view(), name='product-sort'),
    path('products/filter/', ProductFilterView.as_view(), name='product-filter'),
    path('products/buy/<int:product_id>/', BuyProductView.as_view(), name='buy-product'),
    path('products/bought', BoughtProductListView.as_view(), name='bought'),
    path('logout/', LogoutView.as_view(), name='logout'),


]
