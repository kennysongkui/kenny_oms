# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class SystemInstall(models.Model):
    """
    装机列表管理
    """
    ip = models.CharField(max_length=20, verbose_name=u'待装机IP')
    hostname = models.CharField(max_length=30, verbose_name=u'主机名')
    macaddress = models.CharField(max_length=50, validators=u'MAC地址')
    system_version = models.CharField(max_length=20, verbose_name=u'操作系统')
    install_date = models.DateTimeField(auto_now_add=True, verbose_name=u'安装时间')
    profile = models.CharField(max_length=50, verbose_name=u'profile文件名')

    def __unicode__(self):
        return u'%s -- %s' %(self.ip, self.install_date)

    class Meta:
        verbose_name_plural = u'装机列表管理'

class InstallRecord(models.Model):
    """
    Server Install Recored
    """
    install_date = models.CharField(max_length=50, verbose_name=u'安装时间')
    ip = models.CharField(max_length=20, verbose_name=u'安装IP')
    system_version = models.CharField(max_length=50, verbose_name=u'安装操作系统版本')

    def __unicode__(self):
        return u'%s - %s' %(self.ip, self.system_version)

    class Meta:
        verbose_name_plural = u'装机记录管理'