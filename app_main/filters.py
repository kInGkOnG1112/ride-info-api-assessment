import operator
from functools import reduce

from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


def search_result(queryset, search, orm_lookups):

    search_terms = search.split()
    if not search_terms:
        return queryset

    or_queries = [
        Q(**{orm_lookup + '__icontains': term})
        for term in search_terms
        for orm_lookup in orm_lookups
    ]
    combined_query = reduce(operator.or_, or_queries)

    return queryset.filter(combined_query)


class UserProfileFilter(BaseFilterBackend):
    def get_schema_operation_parameters(self, view):
        parameters = []
        if view.action == 'list':
            parameters = [
                {
                    'name': 'search',
                    'required': False,
                    'in': 'query',
                    'description': 'Search user',
                    'schema': {
                        'type': 'string',
                    },
                }
            ]
        return parameters

    def filter_queryset(self, request, queryset, view):

        queryset = queryset.order_by('-id')
        if view.action == 'list':
            query = request.query_params.get('search', '')
            if query != '':
                orm_lookups = [
                    'user__first_name',
                    'user__last_name',
                    'user__email'
                ]
                queryset = search_result(queryset, query, orm_lookups)

            status = request.query_params.get('status', '')
            if status in ('active', 'inactive'):
                queryset = queryset.filter(
                    status=status
                )

        return queryset


