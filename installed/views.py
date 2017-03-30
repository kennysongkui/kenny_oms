# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

