from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from hashids import Hashids

from kuaishou_admin.models import Order, Client

# Create your views here.


encrypt = Hashids()


class LoginView(View):
    '''登陆'''

    def post(self, request):
        # return HttpResponse("login success")
        # 处理注册数据
        user_name = request.POST.get("user_name")
        password = request.POST.get("pwd")

        # 认证用户
        user = authenticate(username=user_name, password=password)
        if user is None:
            return JsonResponse(data={"msg": "密码或用户名错误"})

        # 保存用户登陆session信息
        login(request, user)
        # 跳转到主页
        return JsonResponse(data={"msg": '保存用户状态成功，可以跳转'})


class LogoutView(View):
    '''退出'''

    def post(self, request):
        logout(request)
        return JsonResponse(data={"msg": "退出成功"})


class RealOrdersView(View):
    '''实时订单查询'''

    def post(self, request):
        '''实时订单，返回30条数据'''

        return HttpResponse("订单查询成功")


class OptionSearchView(View):
    '''下拉框搜索'''

    def post(self, request):
        # 获取查询订单的类型(默认是所有订单类型)
        order_type = request.POST.get("order_status")  # 默认是未开始状态
        # 获取查询订单的详情类别(默认是所有项目类型)
        detail_pro = request.POST.get("project")
        # 0 - '所有项目', 1 - '刷粉订单', 2 - '套餐订单', 3 - '播放订单', 4 - '双击订单'
        if detail_pro == "所有项目":

            orders = Order.objects.filter(status=order_type).all()

        else:
            orders = Order.objects.filter(project__pro_name__exact=detail_pro, status=order_type).all()

        result = []
        if orders:
            for order in orders:
                content = order.to_dict()
                order_id = order.order_id_num
                # 把这个id加密
                hash_order_id = encrypt.encode(order_id)
                content['user_id'] = hash_order_id
                result.append(content)

        return JsonResponse(data={"msg": result})


class EnterSearchView(View):
    '''输入框搜索 order'''

    def post(self, request):
        kuaishou_id = request.POST.get('kuaishou_id', None)
        hs_order_id = request.POST.get('order_id', None)

        if kuaishou_id is not None:
            orders = Order.objects.filter(kuaishou_id=kuaishou_id).all().order_by('-create_time_order')

            message = []
            if orders is not None:
                for order in orders:
                    order_dict = order.to_dict()
                    order_id = order_dict['order_id']
                    order_id_new = encrypt.encode(order_id)
                    order_dict['order_id'] = order_id_new
                    message.append(order_dict)
                return JsonResponse(data={'msg': message})

        elif hs_order_id is not None:
            order_id = encrypt.decode(hs_order_id)
            orders = Order.objects.all().filter(order_id=order_id).order_by('-create_time_order')

            message = []
            if orders is not None:
                for order in orders:
                    order_dict = order.to_dict()
                    order_id = order_dict['order_id']
                    order_id_new = encrypt.encode(order_id)
                    order_dict['order_id'] = order_id_new
                    message.append(order_dict)
                return JsonResponse(data={'msg': message})
        else:
            return JsonResponse(data={'msg': False})


class UserSearchView(View):
    '''用户名字/id 搜索'''

    def post(self, request):
        '''搜索功能'''
        user_id = request.POST.get("user_id", None)
        user_name = request.POST.get("user_name")

        if user_id is not None:
            orders = Order.objects.filter(client__wechat_id__exact=user_id).all()
        else:
            orders = Order.objects.filter(client__name__exact=user_name).all()

        result = []
        if orders:
            for order in orders:
                content = order.to_dict()
                order_id = order.order_id_num
                # 把这个id加密
                hash_order_id = encrypt.encode(order_id)
                content['user_id'] = hash_order_id
                result.append(content)

        return JsonResponse(data={"msg": result})



class ModifyStatusView(View):
    '''修改订单状态'''

    def post(self, request):
        order_status = request.POST.get('order_status')
        order_id = request.POST.get('order_id')
        order = Order.objects.filter(order_id=order_id).first()
        if order is None:
            return JsonResponse({'result': False})
        else:
            order.order_status = order_status
            order.save(update_fields=['status'])

        return JsonResponse({'result': True})



class ModifyGoldView(View):
    '''修改金币'''

    def post(self, request):
        # 获取用户的id,和需要修改的金币数
        user_id = request.POST.get("user_id")
        gold_num = request.POST.get("gold_num")

        user = Client.objects.filter(user_id=user_id).first()

        if user is not None:
            user.gold = gold_num
            user.save(update_filed=['gold'])
            return JsonResponse(data={"gold_status": True})

        else:
            return JsonResponse(data={"gold_status": False})


class UserListView(View):
    '''用户列表'''

    def post(self, request):
        users = Client.objects.all()
        content = []
        if users is not None:
            for user in users:
                result = user.to_dict()
                content.append(result)
        else:
            return JsonResponse(data={"msg": "没有查到用户信息"})

        return JsonResponse(data={"msg": content})
