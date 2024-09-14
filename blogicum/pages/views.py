from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


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
