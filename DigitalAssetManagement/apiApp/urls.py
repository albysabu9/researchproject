from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('users/login/', views.userLoginView.as_view(), name='token_obtain_pair'),
    path('users/register/', views.registerView, name='register'),
    path('assets/<int:pk>/', views.ProductListCreateView.as_view(), name='asset_lst_view'),
    path('assets/', views.ProductListCreateView.as_view(), name='asset_lst_view'),
    path('bids/', views.BidApiView.as_view(), name='bid_view'),
    path('bids/<int:pk>/', views.BidApiView.as_view(), name='bid_view'),
    path('block-chain/<int:pk>/', views.BlockChainView.as_view(), name='block_chain_view'),
    path('block-chain/', views.BlockChainView.as_view(), name='block_chain_view'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
