from django.http import HttpResponse
from django.conf import settings
from wsgiref.util import FileWrapper

from utility.decorator import catch_exception


def get_csrf_cookie(request):
    from django.middleware.csrf import get_token
    get_token(request)
    return HttpResponse()


def down_load_file(request, url):
    if settings.MEDIA_ROOT is not None:
        url = settings.MEDIA_ROOT + '/' + url
    f = open(url, 'rb')
    name = url.split('/')[-1:][0]
    response = HttpResponse(FileWrapper(f), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % name
    return response


@catch_exception
def check_version(request):
    version = request.POST.get('version', None)
    request.session['version'] = version
    print 'accept version:{}'.format(version)
    return HttpResponse()