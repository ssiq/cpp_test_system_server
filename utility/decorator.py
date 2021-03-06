# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import render

from utility.constant_value import compatible_version
from utility_funciton import generate_error_response


def check_login(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            return JsonResponse(generate_error_response('please login'))
    return wrapper


def check_version_compatible(func):
    def wrapper(request, *args, **kwargs):
        print 'check the version of the plugin'
        version = request.session.get('version', None)
        r = JsonResponse(generate_error_response('the plugin is not the newest plugin, please update'))
        compatible = True
        if version is not None:
            vs = version.split('.')
            ls = compatible_version[0].split('.')
            for i in xrange(min(len(vs), len(ls))):
                if ls[i] > vs[i]:
                    compatible = False
            if compatible:
                if len(ls) <= len(vs):
                    r = func(request, *args, **kwargs)
        return r
    return wrapper


def check_permission(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return func(request, *args, **kwargs)
        else:
            return JsonResponse(generate_error_response('you don\'t have this permission'))
    return wrapper


def catch_exception(func):
    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception, e:
            print e
            return JsonResponse(generate_error_response(e.message))
    return wrapper


def web_check_login(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            title = u'没有登录'
            return render(request, 'user/unlogin.html', locals())
    return wrapper