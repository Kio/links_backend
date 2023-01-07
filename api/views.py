from django.http import JsonResponse, HttpRequest, HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def csrf(request: HttpRequest) -> HttpResponse:
    return JsonResponse({'csrfToken': get_token(request)})
