# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

from .models import HostList, Message
from kenny_oms.mysql import db_operate
from kenny_oms import settings
from .form import HostsListForm

def host_list(request):
    """
    List all Hosts
    :param request:
    :return:
    """
    user = request.user
    host_list = HostList.objects.all().order_by('-status')
    paginator = Paginator(host_list, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        host_list = paginator.page(page)
    except :
        all_host = paginator.page(paginator.num_pages)

    return render(request, 'host_list.html', {'host_list': host_list, 'page': page, 'paginator':paginator})

def host_list_manage(request, id=None):
    if id:
        host_list = get_object_or_404(HostList, pk=id)
        action = 'edit'
        db = db_operate()
        sql = 'select ip from asset_hostlist where id = %s' % (id)
        ret = db.mysql_command(settings.OMS_MYSQL, sql)
    else:
        host_list = HostList()
        action = 'add'
        ret=[]

    if request.method == 'GET':
        delete = request.GET.get('delete')
        id = request.GET.get('id')
        if delete:
            Message.objects.create(type='host', action='manage', action_ip=ret, content='主机下架')
            host_list = get_object_or_404(HostList, pk=id)
            host_list.delete()
            return HttpResponseRedirect(reverse('host_list'))

    if request.method == 'POST':
        form = HostsListForm(request.POST, instance=host_list)
        print request.POST
        operate = request.POST.get('operate')
        if form.is_valid():
            if action == 'add':
                form.save()
                ret.append(form.cleaned_data['ip'])
                Message.objects.create(type='host', action='manage', action_ip=ret, content='主机添加成功')
                return HttpResponseRedirect(reverse('host_list'))
            if operate:
                if operate == "update":
                    form.save()
                    Message.objects.create(type='host', action='manage', action_ip=ret, content='主机信息更新')
                    return HttpResponseRedirect(reverse('host_list'))
                else:
                    pass
    else:
        form = HostsListForm(instance=host_list)

    return render(request, 'host_manage.html',
                  {"form": form,
                   "action": action,
                  })

def record(request):
    message_list = Message.objects.all().order_by('-audi_time')
    paginator = Paginator(message_list, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        message_list = paginator.page(page)
    except:
        all_host = paginator.page(paginator.num_pages)

    return render(request, 'record.html', {'message_list': message_list, 'page': page, 'paginator': paginator})