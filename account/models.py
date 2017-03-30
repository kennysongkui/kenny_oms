# -×- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    """
    用户管理
    """
    username = models.CharField(max_length=30,verbose_name=u'用户名')
    password = models.CharField(max_length=30,verbose_name=u'密码')

    def __unicode__(self):
        return self.username

    class Meta:
        verbose_name_plural = u'用户信息管理'

class Message(models.Model):
    """
    平台审计信息
    """
    audit_time = models.DateTimeField(auto_now_add=True, verbose_name=u'时间')
    type = models.CharField(max_length=10, verbose_name=u'类型')
    action = models.CharField(max_length=10, verbose_name=u'动作')
    action_ip = models.CharField(max_length=15, verbose_name=u'执行IP')
    content = models.CharField(max_length=50, verbose_name=u'内容')

    class Meta:
        verbose_name_plural = u'审计信息管理'