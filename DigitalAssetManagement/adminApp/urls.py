from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('user-login/', views.UserLoginView.as_view(), name='login_page'),
    path('', views.UserLoginView.as_view(), name='login_page'),
    path('user-logout/', views.LogoutView.as_view(), name='logout_page'),
    path('user-register/', views.UserRegisterView.as_view(), name='user_register'),
    path('my-asset-list/', views.ProductView.as_view(), name='my_asset_list'),
    path('asset-list/', views.AllAssetView.as_view(), name='asset_list'),
    path('block-chain/', views.BlockChainView.as_view(), name='blockk_chain_list'),
    path('block-chain/<int:pk>/', views.BlockChainView.as_view(), name='asset_block_chain_list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
