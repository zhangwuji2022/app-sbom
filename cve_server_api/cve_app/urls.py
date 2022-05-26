#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/5/11 9:25
# @Author : zhu_it2019@126.com
# @File : urls.py
# @Software: PyCharm
# Description:


from django.urls import path

from .views import CveOriginUpstreamView

urlpatterns = [

    # http://{{host}}/api/v1/component-report
    path(r'v1/component-report', CveOriginUpstreamView.as_view(), name='cve_origin_upstream'),  # 获取cve_id

]
