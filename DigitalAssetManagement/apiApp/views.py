from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from apiApp import models, serializers
from rest_framework import status
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from apiApp.serializers import getJWTTokenSerializer, UserSerializerWithToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from apiApp.blockchain import Blockchain, BlockChainTypes
####### User register page#####
# user login view with jwt token




class userLoginView(TokenObtainPairView):
    serializer_class = getJWTTokenSerializer


# user registration view
@api_view(["POST"])
def registerView(request):
    data = request.data
    if data["password"] != data["checkpassword"]:
        print("ehererere i amma")
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if data["name"] and len(data["name"].split(" ")) == 2:
        user_obj = User.objects.create(
            username=data["username"],
            email=data["email"],
            first_name = data["name"].split(" ")[0],
            last_name = data["name"].split(" ")[1],
            password=make_password(data["password"]),
        )
    elif data["name"] and len(data["name"].split(" ")) >2:
        user_obj = User.objects.create(
            username=data["username"],
            email=data["email"],
            first_name = data["name"].split(" ")[-1],
            last_name = data["name"].split(" ")[0],
            password=make_password(data["password"]),
        )
    else:    
        user_obj = User.objects.create(
            username=data["username"],
            email=data["email"],
            first_name = data["name"],
            password=make_password(data["password"]),
        )
    serialized_data = UserSerializerWithToken(user_obj, many=False)
    if serialized_data.is_valid:
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)
    else:
        print(serialized_data.errors)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductListCreateView(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
     mixins.DestroyModelMixin, generics.GenericAPIView
):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProductSerializer
    queryset = models.ProductModel.objects.all()
    
    def list(self, request, pk=None, *args, **kwargs):
        from django.db.models import Prefetch
        if not pk:
            queryset = models.ProductModel.objects.prefetch_related('bidmodel_set').all()
            self.serializer_class = serializers.ProductListSerializer
        else:
            queryset = models.ProductModel.objects.filter(p_owner__id=pk).prefetch_related('bidmodel_set').all()
            self.serializer_class = serializers.ProductListSerializer
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def get(self, request, pk=None, *args, **kwargs):
        return self.list(request, pk, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def put(self, request, pk=None, *args, **kwargs):
        try:
            asset_obj = self.queryset.get(id=pk)
            asset_obj.p_owner = User.objects.get(id=request.POST.get('user_id'))
            try:
                asset_obj.save(update_fields=['p_owner'])
            except Exception as e:
                print(e)

            models.BidModel.objects.filter(product=asset_obj).delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":e}, status=status.HTTP_400_BAD_REQUEST)


class BidApiView(
    mixins.ListModelMixin, mixins.CreateModelMixin, 
    mixins.DestroyModelMixin, 
    mixins.UpdateModelMixin,
      generics.GenericAPIView
    ):
    serializer_class = serializers.CreateBidSerializer
    queryset = models.BidModel.objects.all()

    def get(self, request, pk=None, *args, **kwargs):
        return self.list(request, pk, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs) 


class BlockChainView(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin,
    generics.GenericAPIView):

    serializer_class = serializers.BlockChainSerializer
    queryset = models.BlockChainModel.objects.select_related('product').all()

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            self.queryset = models.BlockChainModel.objects.filter(product__id=pk).select_related('product')
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)