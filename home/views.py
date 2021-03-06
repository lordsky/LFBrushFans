import logging

from django.http import JsonResponse

# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from common.returnMessage import MessageResponse
from utils.views import expired_message

logger = logging.getLogger("django_app")
from kuaishou_admin.models import Project, Order_combo, Client, AdminManagement
expired_message()


@csrf_exempt
def page_shuafen_pay(request):
    return JsonResponse(
        {
            {'status': 200,
             'type': 1,
             'data': {
                 'pay': ''
             }

             },
        }
    )


@csrf_exempt
def home(request):
    return JsonResponse(
        {
            "err": 0,
            "msg": "",
            "data": {
                "topbanner": [
                    {
                        "image": "https://www.apicloud.com/start_page/47/23/472344980350f56a6c9e377d29edc8ca.png",
                        "parms": {
                            "name": "HelpPage"
                        },
                        "type": 2,
                        "verifylogin": False
                    },
                    {
                        "image": "https://www.apicloud.com/start_page/47/23/472344980350f56a6c9e377d29edc8ca.png",
                        "parms": {
                            "name": "AboutMe"
                        },
                        "type": 2,
                        "verifylogin": False
                    }
                ],
                "app": [
                    {
                        "image": "http://oxrm6w8zc.bkt.clouddn.com/indexFans.png",
                        "title": "快手粉丝",
                        "route": "KsFans"
                    },
                    {
                        "title": "快手播放量",
                        "image": "http://oxrm6w8zc.bkt.clouddn.com/indexPlay.png",
                        "route": "KsPlay"
                    },
                    {
                        "title": "快手双击",
                        "image": "http://oxrm6w8zc.bkt.clouddn.com/indexClick.png",
                        "route": "KsDoubleClick"
                    },
                    {
                        "title": "快手直播号",
                        "image": "http://oxrm6w8zc.bkt.clouddn.com/indexAccount.png",
                        "route": "KsAccount"
                    },
                    {
                        "title": "热门套餐",
                        "image": "http://oxrm6w8zc.bkt.clouddn.com/indexHot.png",
                        "route": "ksHotCombo"
                    },
                    {
                        "title": "无水印下载",
                        "image": "http://oxrm6w8zc.bkt.clouddn.com/indexDownload.png",
                        "route": "KsDownload"
                    }
                ]
            }
        }
    )


@csrf_exempt
def shuangji_page(request):
    try:
        clicks = Project.objects.filter(pro_name="双击").all()
    except Exception as e:
        logger.error(e, exc_info=1)
        return JsonResponse(data={"status": 4001, "msg": "数据库查询失败"})
    content = []
    if clicks:
        for fan in clicks:
            content.append(fan.to_dict())

    return JsonResponse(data={"status": 0, "data": content})


@csrf_exempt
def remenTaocan(request):
    if request.method == "GET":
        try:
            taocans = Order_combo.objects.all().prefetch_related('project_detail')
        except Exception as e:
            logger.error(e, exc_info=1)
            return MessageResponse(2001)

        data = []
        for taocan in taocans:
            taocan_msg = {}
            taocan_msg['package_id'] = taocan.id
            taocan_msg['name'] = taocan.name
            taocan_msg['gold'] = taocan.pro_gold

            taocan_msg['detail'] = []
            for detail in taocan.project_detail.all():
                taocan_msg['detail'].append({
                    'project_name': detail.pro_name,
                    'project_num': detail.count_project,
                    'project_id': detail.id,
                })

            data.append(taocan_msg)
        # return render(request,'debug_test/debug_test.html',locals())
        return JsonResponse({"status": 0, "data": data})


@csrf_exempt
def shuafenshi(request):
    try:
        fans = Project.objects.filter(pro_name='粉丝').all()
    except Exception as e:
        logger.error(e, exc_info=1)
        return JsonResponse(data={"status": 4001, "msg": "数据库查询失败"})
    content = []

    if fans:
        for fan in fans:
            content.append(fan.to_dict())

    return JsonResponse(data={"status": 0, "data": content})


@csrf_exempt
def play_home_page(request):
    try:
        fans = Project.objects.filter(pro_name='播放').all()
    except Exception as e:
        logger.error(e, exc_info=1)
        return JsonResponse(data={"status": 4001, "msg": "数据库查询失败"})
    content = []
    if fans:
        for fan in fans:
            content.append(fan.to_dict())

    return JsonResponse(data={"status": 0, "data": content})
