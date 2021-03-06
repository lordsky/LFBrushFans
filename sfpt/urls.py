"""LFBrushFans URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import kuaishou_admin.urls
import kuaishou_app.urls
import home.urls
from backManage import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(kuaishou_admin.urls)),
    url(r'^app/', include(kuaishou_app.urls)),
    url(r'^home/', include(home.urls)),


    url(r'^proManage',views.proManage),
    url(r'^showProject',views.showProject),
    url(r'^changeProject',views.changeProManage),
    url(r'^deleteProject',views.deleteProject),
    url(r'^taocanManage',views.taocanManage),
    url(r'^showTaocan',views.showTaocan),
    url(r'^changeTaocan',views.changeTaocan),
    url(r'^deleteTaocan',views.deleteTaocan),
    url(r'^login_admin',views.login_houtai),
    url(r'^index',views.index),
    url(r'^showAll',views.ShowAll),
    url(r'^showGold',views.show_gold_money),
    url(r'^setGold',views.set_gold_money),
    url(r'^delGold',views.del_gold_money),
]

"""
django_debug_tool_bar配置
当DEBUG=True 时生效
"""

from django.conf import settings
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
