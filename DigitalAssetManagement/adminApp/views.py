import json
from django.http import HttpResponse, JsonResponse
from django.contrib.sessions.models import Session
from django.shortcuts import redirect, render
from django.views import View
from adminApp import apiCalls, constants
from rest_framework import status
from django.utils.decorators import method_decorator
from apiApp import models
from django.contrib.auth import get_user_model

# Create your views here.
# Create your views here.
def is_loggedIn(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('user'):
            return func(request, *args, **kwargs)
        else:
            return redirect('login_page')
    return wrapper



class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name="user_login.html", context={})

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password_id")
        reqData = {'username':username, 'password':password}
        res = apiCalls.login_api(reqData)
        if res.status_code == status.HTTP_200_OK:
            request.session['refresh_token'] = res.json().get("refresh")
            request.session['access_token'] = res.json().get("access")
            request.session['user'] = {
                "refresh_token":res.json().get("refresh"),
                "access_token":res.json().get("access"),
                "refresh_token":res.json().get("refresh"),
                "is_staff":res.json().get("is_staff"),
                "id":res.json().get("id"),
                "username":res.json().get("username"),

            }
            return redirect('my_asset_list')
        
        return render(request, template_name="user_login.html", context={'message':'please enter valid credentials'})
    

class UserRegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name="user_register.html", context={})

    def post(self, request, *args, **kwargs):
        req_data = {}
        req_data["username"] = request.POST.get("username")
        req_data["name"] = request.POST.get("name")
        req_data["email"] = request.POST.get("email")
        req_data["password"] = request.POST.get("password")
        req_data["checkpassword"] = request.POST.get("checkpassword")

        if req_data["password"] != req_data["checkpassword"]:
            return render(request, template_name="user_register.html", context={'message':'password does not match'})
        res = apiCalls.register_api(req_data)
        if res.status_code == status.HTTP_201_CREATED:
            return redirect('login_page')
        return render(request, template_name="user_register.html", context={})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return redirect('login_page')


@method_decorator(is_loggedIn, name='dispatch')
class ProductView(View):

    def get_file_type(self, path):
        import os
        import mimetypes
        if os.path.isfile(path):
            file_type, encoding = mimetypes.guess_type(path)
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
        return None


    def fetch_product_data(self):
        res = apiCalls.fetch_asset_list_api(
            token=self.request.session.get('user').get("access_token"),
            user_id=self.request.session.get('user').get("id")
            )
        if res.status_code == status.HTTP_403_FORBIDDEN or res.status_code == status.HTTP_401_UNAUTHORIZED:
            return redirect("logout_page")
        if res.status_code != status.HTTP_200_OK:
            raise Exception
        return res.json()
    
    def get_render_details(self):
        res = self.fetch_product_data()
        return res

    def get(self, request, *args, **kwargs):
        res=self.get_render_details()
        return render(
            request, 
            template_name='assets.html', 
            context={"product_lst":res}
            )

    def post(self,request, *args, **kwargs):
        from django.http import HttpResponseBadRequest
        form_data = request.POST

        msg = "something went wrong"
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            res = apiCalls.put_api_call(
                url=f"{constants.UrlConst.API_URL.value}/assets/{request.POST.get('asset_id')}/",
                payload = {
                'user_id':request.POST.get('user_id'),
                }
            )
            tt="tt"
            return redirect("my_asset_list")
        
        elif 'form2-delete' in request.POST:
            tt="TT"
            res=apiCalls.delete_asset_api(form_data.get('p_id'),token=self.request.session.get('user').get("access_token"))
            if res.status_code == status.HTTP_403_FORBIDDEN or res.status_code == status.HTTP_401_UNAUTHORIZED:
                return redirect("logout_page")
            return redirect("my_asset_list")

        else:
            try:
                if request.POST.get("p_id"):
                    product_obj = models.ProductModel.objects.get(id=request.POST.get("p_id"))
                    product_obj.p_name = request.POST.get("p_name")
                    product_obj.p_desc = request.POST.get("p_desc")
                    product_obj.p_price = float(request.POST.get("p_price"))
                    if request.FILES.get("p_img"):
                        product_obj.p_img = request.FILES.get("p_img")
                    product_obj.save()
                else:
                    product_obj = models.ProductModel.objects.create(
                        p_owner = get_user_model().objects.get(id=self.request.session.get('user').get("id")),
                        p_name = request.POST.get("p_name"),
                        p_desc = request.POST.get("p_desc"),
                        p_price = request.POST.get("p_price"),
                        p_img = request.FILES.get("p_img")
                    )
                
            except Exception as e:
                print(e)
            
            return redirect("my_asset_list")


@method_decorator(is_loggedIn, name='dispatch')
class AllAssetView(View):
    def get(self, request, *args, **kwargs):
        res = apiCalls.fetch_all_asset_list_api(
            token=self.request.session.get('user').get("access_token"),
            )
        return render(
            request, 
            template_name='all_assets.html', 
            context={"product_lst":res.json()}
            )
    
    def post(self, request, *args, **kwargs):
        tt="tt"
        req_data = {
            "product":request.POST.get("asset_id"),
            "price":request.POST.get("p_price", 0),
            "user":request.session['user'].get('id'),
            }
        res = apiCalls.post_api_call(
                url=f"{constants.UrlConst.API_URL.value}/bids/",
                payload = req_data
            )
        if res.status_code != status.HTTP_201_CREATED and res.json().get('user') and res.json().get('user')[0] == 'bid model with this user already exists.':
            user_id = req_data['user']
            res = apiCalls.put_api_call(
                url=f"{constants.UrlConst.API_URL.value}/bids/{user_id}/",
                payload = req_data
            )
        return redirect("asset_list")


import requests
import logging
from adminApp.constants import UrlConst
@method_decorator(is_loggedIn, name='dispatch')
class BlockChainView(View):
    def get_drop_down_data(self):
        res = apiCalls.get_api_call(
                url=f"{UrlConst.API_URL.value}/block-chain/"
            )
        res_data = res.json()
        drop_down_set = set((item['product_details']['p_name'], item['product_details']['id']) for item in res_data)
        return drop_down_set


    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            res = apiCalls.get_api_call(
            url=f"{UrlConst.API_URL.value}/block-chain/{pk}/"
            )
        else:
            res = apiCalls.get_api_call(
                url=f"{UrlConst.API_URL.value}/block-chain/"
            )
        res_data = res.json()
        return render(
            request, 
            template_name='blockchain.html', 
            context={"asset_lst":res.json(), 'dropdown_set':self.get_drop_down_data()}
            )