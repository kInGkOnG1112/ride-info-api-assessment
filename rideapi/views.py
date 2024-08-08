from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularSwaggerView
from drf_spectacular.settings import spectacular_settings
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
import json, re
from . import settings


def index(request):
    return redirect('swagger-ui')