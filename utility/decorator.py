from django.http import JsonResponse
from utility_funciton import generate_error_response


def check_login(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            return JsonResponse(generate_error_response('please login'))
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
