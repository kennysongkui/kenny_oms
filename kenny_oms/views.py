# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required()
def index(request):
    return reduce(render, 'index.html')