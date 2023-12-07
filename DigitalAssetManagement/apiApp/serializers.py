from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator

from apiApp.models import BidModel, BlockChainModel, ProductModel



class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'password']
        # write_only_fields = ['password']
    
    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name


class getJWTTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except Exception as e:
            print(e)
        data["username"] = self.user.username
        data["email"] = self.user.email
        data["is_staff"] = self.user.is_staff
        data["id"] = self.user.id

        return data


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])   
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'token', 'password']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'




class CreateBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = BidModel
        fields = '__all__'

class BidSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    bid_date_formatted = serializers.SerializerMethodField()
    class Meta:
        model = BidModel
        fields = ('id', 'user', 'product', 'price', 'bid_date', 'bid_date_formatted')

    def get_bid_date_formatted(self, obj):
        from django.utils import timezone
        return obj.bid_date.astimezone(timezone.get_current_timezone()).strftime("%d %B %Y %I:%M %p")

class ProductListSerializer(serializers.ModelSerializer):
    bidmodel_set = BidSerializer(many=True)
    owner_name = serializers.SerializerMethodField()
    product_type = serializers.SerializerMethodField()
    class Meta:
        model = ProductModel
        fields = (
            'id', 'p_owner', 'owner_name', 
             'p_name', 'p_desc', 
            'p_img', 'p_price', 'bidmodel_set',
            'product_type'
            )

    def get_owner_name(self, obj):
        return obj.p_owner.username
    
    def get_product_type(self, obj):
        import os
        import mimetypes
        from urllib.parse import urlparse

        try:
            url = obj.p_img.url
            file_path = urlparse(url).path
            file_type, encoding = mimetypes.guess_type(file_path)
            if file_type is None:
                print("The file type is unknown.")
            elif file_type.startswith('text'):
                return 'txt'
            elif file_type == 'application/pdf':
                return 'pdf'
            elif file_type.startswith('image'):
                return 'img'
            elif file_type.startswith('audio'):
                return 'audio'
            else:
                return None
        except Exception as e:
            return None


class BlockChainSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()
    class Meta:
        model = BlockChainModel
        fields = ['id', 'block', 'time_stamp', 'product_details', 'type_of_block', 'block_detail']
    
    def get_product_details(self, obj):
        tt="tt"
        return ProductSerializer(obj.product).data