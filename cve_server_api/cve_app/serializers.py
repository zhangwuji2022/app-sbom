#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/5/12 10:37
# @Author : zhu_it2019@126.com
# @File : serializers.py.py
# @Software: PyCharm
# Description: 相关模型序列化器

from rest_framework import serializers

from .models import CveOriginUpstream, CveOriginUpstreamConfig, CveOriginUpstreamConfigNode, \
    CveOriginUpstreamConfigNodeCpe, CveIssueTemplate


class CveOriginUpstreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = CveOriginUpstream
        fields = "__all__"


class CveOriginUpstreamConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CveOriginUpstreamConfig
        fields = "__all__"


class CveOriginUpstreamConfigNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CveOriginUpstreamConfigNode
        fields = "__all__"


class CveOriginUpstreamConfigNodeCpeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CveOriginUpstreamConfigNodeCpe
        fields = ["cpe_id", "cpe_uri"]


class CveIssueTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CveIssueTemplate
        fields = "__all__"
