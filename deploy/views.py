# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from saltapi import SaltAPI
from kenny_oms import settings
from asset.models import Message
from asset.models import HostList
from kenny_oms.mysql import db_operate

def salt_key_list(request):
    """
    List all key
    :param request:
    :return:
    """

    user = request.user
    sapi = SaltAPI(url=settings.SALT_API['url'], username=settings.SALT_API['user'],
                   password=settings.SALT_API['password'])
    minions, minions_pre = sapi.list_all_key()

    return render(request, 'salt_key_list.html', {'all_minions': minions, 'all_minions_pre': minions_pre})

def salt_accept_key(request):
    """
    accept salt minions key
    :param request:
    :return:
    """

    node_name = request.GET.get('node_name')
    sapi = SaltAPI(url=settings.SALT_API['url'], username=settings.SALT_API['user'],
                   password=settings.SALT_API['password'])
    ret = spai.accept_key(node_name)
    Message.objects.create(type='salt', action='key', action_ip= node_name, content='saltstack accept node key')
    return HttpResponseRedirect(reverse('key_list'))

def salt_delete_key(request):
    """
    delete salt minions key
    :param request:
    :return:
    """
    node_name = request.GET.get('node_name')
    sapi = SaltAPI(url=settings.SALT_API['url'], username=settings.SALT_API['user'],
                   password=settings.SALT_API['password'])
    ret = sapi.delete_key(node_name)
    Message.objects.create(type='salt', action='key', action_ip=node_name, content='saltstack delete node key')
    return HttpResponseRedirect(reverse('key_list'))

def module_deploy(request):
    """
    deploy (nginx/php/mysql..etc) module
    :param request:
    :return:
    """

    ret = []
    jid = []
    user = request.user
    if request.method == 'POST':
        action = request.get_full_path().split('=')[1]
        if action == 'deploy':
            tgt = request.POST.get('tgt')
            arg = request.POST.getlist('module')
            tgtcheck = HostList.objects.filter(hostname=tgt)
        if tgtcheck:
            Message.objects.create(type='salt', action='deploy', action_ip=tgt,
                                   content='saltstack %s module deploy' % (arg))
            sapi = SaltAPI(url=settings.SALT_API['url'], username=settings.SALT_API['user'],
                           password=settings.SALT_API['password'])
            db = db_operate()

            if 'sysinit' in arg:
                obj = sapi.async_deploy(tgt, arg[-1])
                sql = "instert INTO salt_returns VALUES(%s) " % obj
                print sql
                jid.append(obj)
                arg.remove('sysinit')
                if arg:
                    for i in arg:
                        obj = sapi.async_deploy(tgt, i)
                        jid.append(obj)

            else:
                for i in arg:
                    obj = sapi.async_deploy(tgt, i)
                    sql = "insert INTO salt_returns VALUES(%s) " % obj
                    db.mysql_command(settings.OMS_MYSQL, sql)
                    jid.append(obj)
                    msg = '%s deploy %s module success,jid is %s' % (tgt, i, obj)
                    ret.append(msg)
        else:
            ret = '目标主机不对，请重新输入'

    return render(request, 'salt_module_deploy.html', {'ret': ret})

def remote_execution(request):
    """
    remote command execution
    :param request:
    :return:
    """

    ret = ''
    tgtcheck = ''
    danger = ('rm', 'reboot', 'init ', 'shutdown', 'll')
    user = request.user
    if request.method == 'POST':
        action = request.get_full_path().split('=')[1]
        if action == 'exec':
            tgt = request.POST.get('tgt')
            arg = request.POST.get('arg')
            tgtcheck = HostList.objects.filter(hostname=tgt)
            argcheck = arg not in danger
            if tgtcheck and argcheck:
                sapi = SaltAPI(url=settings.SALT_API['url'], username=settings.SALT_API['user'],
                               password=settings.SALT_API['password'])
                ret = sapi.remote_execution(tgt, 'cmd.run', arg)
            elif not tgtcheck:
                ret = '目标主机不正群，请重新输入'
            elif not argcheck:
                ret = '命令很危险。'
        Message.objects.create(type='slat',action='execution', action_ip=tgt,
                               content='saltstack execution command: %s '% (arg))
    return render(request, 'salt_remote_execution.html', {'ret': ret})