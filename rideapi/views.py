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


class SpectacularView(SpectacularSwaggerView):

    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        return Response(
            data={
                'view_logs': (settings.DEBUG and False),
                'title': self.title,
                'dist': self._swagger_ui_dist(),
                'favicon_href': self._swagger_ui_favicon(),
                'schema_url': self._get_schema_url(request),
                'settings': self._dump(spectacular_settings.SWAGGER_UI_SETTINGS),
                'oauth2_config': self._dump(spectacular_settings.SWAGGER_UI_OAUTH2_CONFIG),
                'template_name_js': self.template_name_js,
                'csrf_header_name': self._get_csrf_header_name(),
                'schema_auth_names': self._dump(self._get_schema_auth_names()),
            },
            template_name=self.template_name,
        )
