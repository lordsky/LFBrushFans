# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PayListModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('order_id', models.CharField(max_length=200, verbose_name='订单号')),
                ('ddh', models.CharField(max_length=100, default='', verbose_name='支付平台订单号')),
                ('money', models.DecimalField(default=Decimal('0.0'), verbose_name='支付金额', max_digits=19, decimal_places=10)),
                ('pay_list_date', models.DateTimeField(auto_now_add=True)),
                ('order_type', models.IntegerField(verbose_name='订单类型', choices=[(0, '积分充值'), (1, '开通会员')])),
                ('pay_type', models.CharField(max_length=100, verbose_name='支付类型')),
                ('remark', models.TextField(default='', verbose_name='说明')),
                ('status', models.IntegerField(default=3, verbose_name='订单状态', choices=[(1, '成功'), (2, '失败'), (3, '等待付款')])),
                ('client', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
