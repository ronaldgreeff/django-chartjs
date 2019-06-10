from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets, generics

# from django.views.generic import View
from django_filters import rest_framework as filters

from charts.models import *
from charts.serializers import *

import json


class DataSetViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = DataSet.objects.prefetch_related('entry_set').all()
    serializer_class = DataSetSerializer
    # filter_backends = (filters.DjangoFilterBackend)

    def list(self, request, *args, **kwargs):

        response = super(DataSetViewSet, self).list(request, *args, **kwargs)

        response.data = {'{}{}'.format(
            result.pop('id'), result.pop('title').lower().replace(' ', '_')
            ): result for result in response.data}

        return response


class ChartViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Chart.objects.all()
    serializer_class = ChartSerializer


class AdminGraphView(TemplateView):
    template_name = 'charts/graph.html'

    def get_context_data(self):
        context = super(AdminGraphView, self).get_context_data()
        context['endpoint'] = json.dumps('data')

        return context
