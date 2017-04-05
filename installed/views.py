# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

from asset.models import HostList, Message
from .models import SystemInstall, InstallRecord
from cobbler_api import CobblerAPI
from kenny_oms import settings
from form import SystemInstallForm
from kenny_oms.mysql import db_operate


def system_install(request):
    """
    1,Add Some Info to cabbler system
    2,remote starting up
    3.screen put in system install process
    :param request:
    :return:
    """

    cobbler  = CobblerAPI(url=settings.Cobbler_API['url'], user=settings.Cobbler_API['user'], password=settings.Cobbler_API['password'])
    if request.method == 'GET':
        ip = request.GET.get('ip')
        hostname = request.GET.get('host')
        mac_add = request.GET.get('mac')
        version = request.GET.get('ver')
        profile = request.GET.get('profile')
        ret = cobbler.add_system(hostname=hostname, ip_add=ip, mac_add=mac_add,profile=profile)
        if ret['result']:
            data = SystemInstall.objects.filter(ip=ip)
            install_date = str(data[0]).split('--')[1].strip()
            InstallRecord.objects.create(ip=ip, system_version=profile, install_date=install_date)
            HostList.objects.filter(ip=ip).update(status='已使用')
            SystemInstall.objects.filter(ip=ip).delete()
            Message.objects.create(type='system', action='install', action_i=ip, content='主机信息添加至cobber，进入安装模式')
        return HttpResponseRedirect(reverse('install_list'))

def system_install_list(request):
    """
    list all waiting for the host operating system is installed.
    :param request:
    :return:
    """
    user = request.user

    result = HostList.objects.filter(status='待装机')
    install_list = []
    for i in range(len(result)):
        ip = str(result[i]).split('-')[0]
        hostname = str(result[i]).split('-')[1].strip()
        ret = SystemInstall.objects.filter(ip=ip)
        if ret:
            message = ip + ' 已经在待安装列表'

    all_system_list = SystemInstall.objects.all().order_by('-install_date')

    paginator = Paginator(all_system_list, 10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_system_list = paginator.page(page)
    except :
        all_system_list = paginator.page(paginator.num_pages)

    return render(request, 'install_list.html', {'all_system_list': all_system_list})

def system_install_managed(request, id=None):
    """
    Management host to be installed.
    :param request:
    :param id:
    :return:
    """
    user = request.user

    if  id:
        system_install = get_object_or_404(SystemInstall, pk=id)
        action = 'edit'
    else:
        system_install = SystemInstall()
        action = 'add'

    if request.method == 'POST':
        operate = request.POST.get('operate')
        form  = SystemInstallForm(request.POST, instance=system_install)
        if form.is_valid():
            if action == 'add':
                form.save()
                ret = form.cleaned_data['ip']
                Message.objects.create(type='system', action='install',action_ip=ret, content='主机信息已添加(macadd,system_version)，准备装机')
                return HttpResponseRedirect(reverse('install_list'))
            if operate:
                if operate == 'update':
                    form.save()
                    db = db_operate()
                    sql = 'select ip from installed_systeminstall where id = %s' %(id)
                    ret = db.mysql_command(settings.OMS_MYSQL,sql)
                    Message.objects.create(type='system',action='install', action_ip='ret',content='主机信息已更新(macadd,system_version),准备装机')
                    return HttpResponseRedirect(reverse('install_list'))
                else:
                    pass

    else:
        form = SystemInstallForm(instance=system_install)
        action = 'add'

    return render(request, 'install_manage.html',
                  {"form": form,
                    'action': action
                    })

def system_install_record(request):
    """
    List all operating system installation records
    :param request:
    :return:
    """
    user = request.user

    record = InstallRecord.objects.all().order_by('-install_date')
    paginator = Paginator(record, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        record = paginator.page(page)
    except:
        record = paginator.page(paginator.num_pages)

    return render(request, 'install_record_list.html', {'record': record, 'page': page, 'paginator': paginator})