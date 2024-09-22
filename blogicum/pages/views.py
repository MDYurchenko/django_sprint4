from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseServerError


# Вопрос про шаблоны джанго: а они вообще актуальны
# в реальной разработке?? Насколько я понимаю, нормальные
# взрослые приложения через DRF пишут, создавая API?

def about(request: HttpRequest) -> HttpResponse:
    """
    Функция для отображения страницы "О проекте"
    :param request: HttpRequest
    :return: HttpResponse
    """
    return render(request, 'pages/about.html', context=None, status=200)


def rules(request: HttpRequest) -> HttpResponse:
    """
    Функция для отображения страницы "Наши правила"
    :param request: HttpRequest
    :return: HttpResponse
    """
    return render(request, 'pages/rules.html', context=None, status=200)


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    return render(request, 'pages/500.hmtl', status=500)
