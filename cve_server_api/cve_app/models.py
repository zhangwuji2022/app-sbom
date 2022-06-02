# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CveOriginUpstream(models.Model):
    cve_id = models.BigAutoField(primary_key=True)
    cve_un_ids = models.CharField(unique=True, max_length=256)
    cve_num = models.CharField(max_length=256)
    update_type = models.CharField(max_length=32)
    cve_packname = models.CharField(max_length=2048, blank=True, null=True)
    git_packname = models.CharField(max_length=900, blank=True, null=True)
    cve_title = models.CharField(max_length=1024, blank=True, null=True)
    affect_porduct = models.CharField(max_length=512, blank=True, null=True)
    cnnvd_id = models.CharField(max_length=256, blank=True, null=True)
    cnvd_id = models.CharField(max_length=256, blank=True, null=True)
    published_date = models.CharField(max_length=32, blank=True, null=True)
    vul_status = models.CharField(max_length=64, blank=True, null=True)
    cve_status = models.IntegerField()
    version = models.CharField(max_length=900, blank=True, null=True)
    affected_scope = models.CharField(max_length=512, blank=True, null=True)
    attack_link = models.CharField(max_length=512, blank=True, null=True)
    is_exit = models.IntegerField()
    create_time = models.CharField(max_length=32)
    update_time = models.CharField(max_length=32, blank=True, null=True)
    delete_time = models.CharField(max_length=32, blank=True, null=True)
    credibility_level = models.IntegerField()
    first_per_time = models.CharField(max_length=32)
    first_get_time = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'cve_origin_upstream'
        verbose_name = "cve源数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cve_id


class CveOriginUpstreamConfig(models.Model):
    conf_id = models.BigAutoField(primary_key=True)
    cve_id = models.BigIntegerField()
    nodes = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cve_origin_upstream_config'
        verbose_name = "cve源数据配置"
        verbose_name_plural = verbose_name


class CveOriginUpstreamConfigNode(models.Model):
    node_id = models.BigAutoField(primary_key=True)
    conf_id = models.BigIntegerField()
    operator = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cve_origin_upstream_config_node'
        verbose_name = "cve源数据配置节点"
        verbose_name_plural = verbose_name


class CveOriginUpstreamConfigNodeCpe(models.Model):
    cpe_id = models.BigAutoField(primary_key=True)
    node_id = models.BigIntegerField()
    cpe_uri = models.CharField(max_length=1024, blank=True, null=True)
    cpe_match = models.CharField(max_length=1024, blank=True, null=True)
    vulner_able = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cve_origin_upstream_config_node_cpe'
        verbose_name = "cve源数据配置节点cpe"
        verbose_name_plural = verbose_name


class CveIssueTemplate(models.Model):
    template_id = models.BigAutoField(primary_key=True)
    cve_id = models.BigIntegerField(unique=True)
    cve_num = models.CharField(max_length=256)
    owned_component = models.CharField(max_length=256)
    owned_version = models.CharField(max_length=256)
    nvd_score = models.DecimalField(max_digits=10, decimal_places=1)
    openeuler_score = models.DecimalField(max_digits=10, decimal_places=1)
    nvd_vector = models.CharField(max_length=256)
    openeuler_vector = models.CharField(max_length=256)
    cve_brief = models.CharField(max_length=4096)
    cve_analysis = models.CharField(max_length=4096)
    principle_analysis = models.CharField(max_length=4096)
    affected_version = models.CharField(max_length=256)
    solution = models.CharField(max_length=1024)
    issue_id = models.BigIntegerField()
    issue_num = models.CharField(max_length=64)
    issue_assignee = models.CharField(max_length=128)
    status = models.IntegerField()
    status_name = models.CharField(max_length=128, blank=True, null=True)
    issue_status = models.IntegerField()
    issue_label = models.CharField(max_length=256)
    owner = models.CharField(max_length=128)
    repo = models.CharField(max_length=128)
    title = models.CharField(max_length=512)
    issue_type = models.CharField(max_length=64)
    collaborators = models.CharField(max_length=128, blank=True, null=True)
    milestone = models.CharField(max_length=64, blank=True, null=True)
    program = models.CharField(max_length=64, blank=True, null=True)
    security_hole = models.IntegerField()
    cve_level = models.CharField(max_length=32, blank=True, null=True)
    comment_id = models.BigIntegerField(blank=True, null=True)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    delete_time = models.DateTimeField()
    error_description = models.TextField(blank=True, null=True)
    mt_audit_flag = models.IntegerField()
    sa_audit_flag = models.IntegerField()
    op_audit_flag = models.IntegerField()
    sec_link = models.CharField(max_length=512)
    abi_version = models.CharField(max_length=256)
    plan_started_at = models.CharField(max_length=64, blank=True, null=True)
    deadline = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cve_issue_template'
        unique_together = (('cve_num', 'issue_num'),)
        verbose_name = "cve解析后的数据"
        verbose_name_plural = verbose_name


class CveVulnCenter(models.Model):
    cve_id = models.BigAutoField(primary_key=True)
    cve_num = models.CharField(max_length=256)
    cve_level = models.CharField(max_length=32, blank=True, null=True)
    cve_desc = models.CharField(max_length=8192)
    cve_status = models.IntegerField()
    cve_version = models.CharField(max_length=128)
    repair_time = models.CharField(max_length=32)
    pack_name = models.CharField(max_length=512)
    cve_url = models.CharField(max_length=2048)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    delete_time = models.DateTimeField()
    is_export = models.IntegerField()
    data_source = models.IntegerField()
    cve_detail_url = models.CharField(max_length=1024)
    organizate_id = models.IntegerField()
    first_per_time = models.CharField(max_length=32)
    first_get_time = models.CharField(max_length=32)
    repo_name = models.CharField(max_length=512)

    class Meta:
        managed = False
        db_table = 'cve_vuln_center'
        unique_together = (('cve_num', 'cve_version', 'pack_name', 'organizate_id'),)
        verbose_name = "cve中心表，cve_origin_upstream与issue关联数据"
        verbose_name_plural = verbose_name
