from charts.models import *
from rest_framework import serializers


background_colours = [
    '#3e95cd',
    '#8e5ea2',
    '#3cba9f',
    '#e8c3b9',
    '#c45850',
]

# selector = '{}{}'.format(obj.id, obj.title.lower().replace(' ', '_'))

class DataSetSerializer(serializers.Serializer):

    dataset_label = serializers.CharField()
    entries = serializers.SerializerMethodField()

    def get_entries(self, obj):

        keys = []
        values = []
        for entry in obj.entries.all():
            keys.append(entry.key)
            values.append(entry.value)

        return {
            'keys': keys,
            'values': values
        }


class ChartSerializer(serializers.Serializer):

    chart_title = serializers.CharField()
    chart_type = serializers.CharField()
    datasets = DataSetSerializer(many=True)

    def to_representation(self, obj):

        def get_labels(datasets):

            l = []
            for d in datasets:
                for k in d['entries']['keys']:
                    if not k in l:
                        l.append(k)
            return l

        def get_datasets(datasets):

            return [{
                'label': dataset['dataset_label'],
                'data': dataset['entries']['values'],
            } for dataset in data['datasets']]


        data = super(ChartSerializer, self).to_representation(obj)

        chart_type = data['chart_type']

        proto_chart = {
            'type': chart_type,
            'data': {
                'labels': get_labels(data['datasets']),
                'datasets': get_datasets(data['datasets']),
            },
            'options': {
                'title': {
                    'display': True,
                    'text': data['chart_title'],
                }
            }
        }


        def set_additional_parameters(chart_type, proto_chart):

            # chart_options = proto_chart['options']
            chart_datasets = proto_chart['data']['datasets']

            if (chart_type == 'bar' or chart_type == 'horizontalBar') and len(proto_chart['data']['datasets']) == 1:

                proto_chart['options'].update({'legend': {'display': False}})

                for chart_dataset in chart_datasets:
                    chart_dataset.update(
                        {'backgroundColor': background_colours[:len(chart_dataset['data'])]}
                    )

            else:

                for chart_dataset in chart_datasets:
                    chart_dataset.update(
                        {'backgroundColor': background_colours[chart_datasets.index(chart_dataset)]}
                    )

            return proto_chart


        return set_additional_parameters(chart_type, proto_chart)