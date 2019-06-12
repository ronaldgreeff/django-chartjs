from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets, generics

# from django.views.generic import View
from django_filters import rest_framework as filters

from charts.models import *
from charts.serializers import *

import json


def get_selector_title(chart_data_object):
    return '{}{}'.format(chart_data_object.id, chart_data_object.title.lower().replace(' ', '_'))

# Need both serialized data and data.selector from data being serialized - declare once as constant
ADMIN_DATA = Chart.objects.prefetch_related('datasets').filter(chart_group__name='Admin')



class AdminChartViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = ADMIN_DATA
    serializer_class = ChartSerializer


class AdminGraphView(TemplateView):
    template_name = 'charts/graph.html'

    def get_context_data(self):

        context = super(AdminGraphView, self).get_context_data()

        # context['selectors'] = [get_selector_title(chart.data)
        #     for chart in ADMIN_DATA]

        context['endpoint'] = json.dumps('data/admin_data')

        return context