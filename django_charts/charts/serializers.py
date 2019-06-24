from charts.models import *
from rest_framework import serializers


standard_settings = {
    'colour_swatch': [
        'rgb(62,149,205)',
        'rgb(142,94,162)',
        'rgb(60,186,159)',
        'rgb(232,195,185)',
        'rgb(196,88,80)',
    ],
    'gradients': {
        'backgroundColor': 0.2,
        'borderColor': 1,
    },
    'datasets': {
        'borderWidth': 1,
    },
    'charts': {
        'radar': {
            'fill': True,
            # 'pointBorderColor': add_gradient(swatch, 0.2), # Should call the function here, but can't
            # 'pointBackgroundColor': add_gradient(swatch, 1)
        }
    }
}


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

                chart_options.update({'legend': {'display': False}})

            return proto_chart


        def set_dataset_params(proto_chart):

            def add_gradient(rgb_str, v=1):
                return '{},{}{}'.format(rgb_str[:-1], v, rgb_str[-1:])


            def apply_colours(chart_dataset):

                if chart_type in ('bar', 'horizontalBar') and len(chart_datasets) == 1:

                    swatches = standard_settings['colour_swatch'][:len(chart_dataset['data'])]

                    gradiated_swatches = {gradient_type[0]: [add_gradient(swatch, gradient_type[1]) for swatch in swatches]
                        for gradient_type in standard_settings['gradients'].items()}

                    chart_dataset.update(gradiated_swatches)

                else:

                    swatch = standard_settings['colour_swatch'][chart_datasets.index(chart_dataset)]

                    gradiated_swatch = {gradient_type[0]: add_gradient(swatch, gradient_type[1])
                        for gradient_type in standard_settings['gradients'].items()}

                    chart_dataset.update(gradiated_swatch)


            def apply_standard_settings(chart_dataset):
                chart_dataset.update(standard_settings['datasets'])


            def apply_additional_chart_settings(chart_dataset):
                additional_chart_settings = standard_settings['charts'].get(chart_type)
                if additional_chart_settings:
                    chart_dataset.update(additional_chart_settings)



            chart_type = proto_chart['type']
            chart_datasets = proto_chart['data']['datasets']


            for chart_dataset in chart_datasets:

                apply_colours(chart_dataset)

                apply_standard_settings(chart_dataset)

                apply_additional_chart_settings(chart_dataset)


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