# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
import logging

from .models import Produt
from .forms import ProdutForm
from . import common

logger = logging.getLogger('django')


def build_context():
    context = {}
    context['type_list'] = common.type_list
    context['status_list'] = common.status_list
    return context

def index(request):
    context = build_context()

    listData = Produt.objects.all()

    
    context['listData'] = listData

    return render(request, 'product/index.html', context)

def add(request):
    request.encoding = 'utf-8'
    context = build_context()
    if request.method == "POST":
        form = ProdutForm(request.POST)
        if form.is_valid():
             product = form.save(commit=False)
             product.createUser("admin")
             product.save()
        return HttpResponseRedirect('/product')
    else:
        form = ProdutForm()
    context['title'] = "新增"
    context['formUrl'] = "/product/add"
    context['form'] = form
    return render(request, 'product/form.html', context)


def edit(request, pk):
    logger.info("-----------edit product----------"+pk)
    context = build_context()
    obj = Produt.objects.filter(pk=pk).first()
    if not obj:
        return redirect('/product')
    if request.method == "GET":
        form = ProdutForm(instance=obj)
        context['form'] = form
        context['title'] = "编辑"
        context['formUrl'] = "/product/edit/"+pk
        return render(request, 'product/form.html', context)
    else:
        form = ProdutForm(request.POST, instance=obj)
        logger.info("-----------edit product----------")
        logger.info(form)
        if form.is_valid():
            product = form.save(commit=False)
            product.updateUser("admin")
            product.save()
        return redirect('/product')







