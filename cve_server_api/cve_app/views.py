import json
import logging
import re

from common.response_code import params_error, rsp_data, query_error
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from packageurl import PackageURL
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from .models import CveOriginUpstream, CveIssueTemplate, CveVulnCenter

# Create your views here.


logger = logging.getLogger('log')


class GlobalPageNumberPagination(PageNumberPagination):
    def __init__(self):
        super(GlobalPageNumberPagination, self).__init__()
        self.page_size = 20  # 默认每页显示的多少条记录
        self.page_query_param = 'page'  # 默认查询参数名为 page
        self.page_size_query_param = 100  # 前台控制每页显示的最大条数
        self.max_page_size = 300  # 后台控制显示的最大记录条数


class CveOriginUpstreamView(APIView):
    """
    数据库查询操作
    cve_origin_upstream_config_node_cpe
    cve_origin_upstream_config_node
    cve_origin_upstream_config
    cve_origin_upstream
    cve_issue_template
    """

    # pagination_class = GlobalPageNumberPagination  # 分页的序列化
    @swagger_auto_schema(methods=['post'],
                         request_body=openapi.Schema(type=openapi.TYPE_OBJECT, required=['coordinates']),
                         operation_summary='查询CVE',
                         operation_description='''测试用例格式如下：\n
                        {"coordinates":
                          [
                            "pkg:maven/org.apache.xmlgraphics/kernel@4.19.194?arch=x86&pkgName=kernel&platform=java",
                            "pkg:maven/org.apache.ant/netty@4.1.13?arch=x86&pkgName=netty&platform=java"
                          ]
                        }''')
    @action(methods=['post'], detail=False)
    def post(self, request):
        """
        :param request:
        :return: json
        """
        logger.info(f"------------------------------")
        rsp_list = []
        cve_origin_upstream_queryset_list = []
        cve_issue_template_queryset_list = []
        git_packname_param_list = []
        cve_num_lst = []
        try:
            purl_json_str = request.body
            purl_list = (json.loads(purl_json_str.decode())).get("coordinates")
        except Exception as e:
            return params_error(message="coordinates 请求参数格式错误")

        if not purl_list:
            return params_error(message="coordinates 参数错误")

        if not isinstance(purl_list, list):
            return params_error(message="coordinates 请求参数类型错误")

        for purl in purl_list:
            parse_purl = PackageURL.from_string(purl)
            purl_data = parse_purl.to_dict()
            pkg_name = purl_data.get("qualifiers").get("pkgname") if purl_data.get("qualifiers") and purl_data.get(
                "qualifiers").get("pkgname") else purl_data.get("name")

            version = purl_data.get("version", None)
            git_packname_param = f'{pkg_name}=={version}'
            git_packname_param_list.append(git_packname_param)

            # 模糊查询：包含 忽略大小写 ilike '%aaa%'
            try:
                cve_origin_upstream_queryset = CveOriginUpstream.objects.filter(
                    git_packname__icontains=git_packname_param,
                    cve_status__in=[0, 1, 2]).order_by("-cve_id")
                cve_origin_upstream_queryset_list.append(cve_origin_upstream_queryset)
            except Exception as e:
                logger.error(f"cve_origin_upstream--{e}")
                return query_error(message="查询异常")

        for queryset in cve_origin_upstream_queryset_list:
            for row in queryset:
                origin_cve_num = row.cve_num.strip()
                origin_cve_git_packname_list = row.git_packname.strip().split(",")
                origin_cve_git_packname_list = [data.upper() for data in origin_cve_git_packname_list]
                for item in git_packname_param_list:
                    if item.upper() not in origin_cve_git_packname_list:
                        continue
                    else:
                        cve_num_lst.append(origin_cve_num)
                        break
        try:
            cve_issue_template_queryset = CveIssueTemplate.objects.filter(
                cve_num__in=cve_num_lst, issue_status__in=[1, 3]).order_by("-template_id")
            cve_issue_template_queryset_list.append(cve_issue_template_queryset)
        except Exception as e:
            logger.error(f"cve_issue_template--{e}")
            return query_error(message="查询异常")

        for each_git_packname in git_packname_param_list:
            cve_origin_upstream_git_packname = each_git_packname.split("==")[0]
            cve_origin_upstream_version = each_git_packname.split("==")[1]

            for cve_issue_template_queryset in cve_issue_template_queryset_list:
                for row_cve_issue_template in cve_issue_template_queryset:
                    cve_issue_template_num = row_cve_issue_template.cve_num
                    cve_issue_template_owned_component = row_cve_issue_template.owned_component
                    cve_issue_template_owned_version_list = row_cve_issue_template.owned_version.split(",")

                    for cve_issue_template_owned_version in cve_issue_template_owned_version_list:
                        if ((cve_issue_template_owned_version == cve_origin_upstream_version) or
                            self.parse_cve_issue_template_owned_version(cve_origin_upstream_version,
                                                                        cve_issue_template_owned_version)) and \
                                (cve_issue_template_num in cve_num_lst) and \
                                (cve_issue_template_owned_component.upper() ==
                                 cve_origin_upstream_git_packname.upper()):

                            content_dict = {
                                "cve_num": cve_issue_template_num,  # cve编号
                                "owned_component": cve_origin_upstream_git_packname,  # 漏洞归属组件
                                "version": cve_origin_upstream_version,  # 漏洞归属版本
                                "issue_num": row_cve_issue_template.issue_num,  # issue的issue_num
                                "issue_status": row_cve_issue_template.issue_status,  # 1:待分析；3：已分析，待修复
                                "cvss2_score": row_cve_issue_template.nvd_score,  # cvss2.x评分
                                # cvss2.x评分向量
                                "cvss2_vector": f"({row_cve_issue_template.nvd_vector})" if
                                row_cve_issue_template.nvd_vector else "",
                                "cvss3_score": row_cve_issue_template.openeuler_score,  # cvss3.x评分
                                # cvss3.x评分向量
                                "cvss3_vector": f"CVSS:3.1/{row_cve_issue_template.openeuler_vector}" if
                                row_cve_issue_template.openeuler_vector else "",
                                "owner": row_cve_issue_template.owner,  # 仓库地址
                                "cve_url": self.get_cve_url_by_cve_num(cve_issue_template_num),  # cve_url地址
                                # 正则匹配purl地址
                                "purl": [purl_str for purl_str in purl_list if
                                         re.findall(
                                             f"={cve_issue_template_owned_component.upper()}"
                                             f"|{cve_issue_template_owned_component.upper()}@",
                                             purl_str.upper())][0]
                            }
                            rsp_list.append(content_dict)
                            break
                        else:
                            continue

        return rsp_data(data=rsp_list, count=len(rsp_list))

    def parse_cve_issue_template_owned_version(self, cve_origin_upstream_version,
                                               cve_issue_template_owned_version):
        """
        解析 cve_issue_template表 owned_version 字段 含有<符号或其他描述语言的处理
        如：Thunderbird<68.9.0,Firefox<77,andFirefoxESR<68.9.
        """
        if cve_issue_template_owned_version == "all version":
            return True
        if "<" in cve_issue_template_owned_version:
            tmp_list = cve_issue_template_owned_version.split("<")
            version = tmp_list[1]
            if cve_origin_upstream_version <= version:
                return True
            else:
                return False

    def get_cve_url_by_cve_num(self, cve_num):
        """
        根据cve_num获取 cve_vuln_center 表中的cve_url
        """
        try:
            cve_vuln_center_cve_num_queryset = CveVulnCenter.objects.filter(cve_num=cve_num).order_by("-cve_id")
            cve_url = cve_vuln_center_cve_num_queryset[0].cve_url if cve_vuln_center_cve_num_queryset[0] else ""
            return cve_url
        except Exception as e:
            logger.error(f"cve_vuln_center--{e}")
            return ""
