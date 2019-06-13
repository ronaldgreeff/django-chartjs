from charts.models import *
from rest_framework import serializers


colour_swatch = [
    'rgb(62,149,205)',
    'rgb(142,94,162)',
    'rgb(60,186,159)',
    'rgb(232,195,185)',
    'rgb(196,88,80)',
]

gradients = {
    'backgroundColor': 0.5,
    'borderColor': 1,
}

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

        proto_chart = {
            'id': obj.id,
            'type': data['chart_type'],
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



        def set_options(proto_chart):

            chart_type = proto_chart['type']
            chart_options = proto_chart['options']

            if (chart_type == 'bar' or chart_type == 'horizontalBar'):

                proto_chart['options'].update({'legend': {'display': False}})

            return proto_chart


        def set_dataset_params(proto_chart):

            def add_gradient(source_str, v=1):
                return '{},{}{}'.format(source_str[:-1], v, source_str[-1:])

            chart_type = proto_chart['type']
            chart_datasets = proto_chart['data']['datasets']

            if len(chart_datasets) == 1:

                for chart_dataset in chart_datasets:

                    swatches = colour_swatch[:len(chart_dataset['data'])]

                    chart_dataset.update({
                        'backgroundColor': [add_gradient(swatch, 0.2) for swatch in swatches],
                        'borderColor': [add_gradient(swatch, 1) for swatch in swatches], })
            else:

                for chart_dataset in chart_datasets:

                    swatch = colour_swatch[chart_datasets.index(chart_dataset)]

                    chart_dataset.update({
                        'backgroundColor': add_gradient(swatch, 0.2),
                        'borderColor': add_gradient(swatch, 1), })

                    if chart_type == 'radar':
                        chart_dataset.update({
                            'fill': True,
                            'pointBorderColor': add_gradient(swatch, 0.2),
                            'pointBackgroundColor': add_gradient(swatch, 1), })

            return proto_chart


        def set_chart_selector(proto_chart):

            proto_chart.update({
                    'selector': '{}{}{}'.format(
                            proto_chart.pop('id'),
                            proto_chart['type'],
                            (proto_chart['options']['title']['text']).replace(' ','').lower(),
                        )
                })

            return proto_chart


        proto_chart = set_options(proto_chart)
        proto_chart = set_dataset_params(proto_chart)

        chart = set_chart_selector(proto_chart)

        return chart