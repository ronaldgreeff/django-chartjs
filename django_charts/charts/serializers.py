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

        data = super(ChartSerializer, self).to_representation(obj)

        chart_type = data['chart_type']

        if chart_type == 'line' or chart_type == 'radar':

        # IN:
        # OrderedDict([
        #   ('chart_title', 'Line Chart'),
        #   ('chart_type', 'line'),
        #   ('datasets', [
        #       OrderedDict([
        #           ('dataset_label', 'Africa'),
        #           ('entries', {'keys': ['January', 'February', 'March'], 'values': [10, 40, 30]})]
        #           ),
        #       OrderedDict([
        #           ('dataset_label', 'Asia'),
        #           ('entries', {'keys': ['January', 'February', 'March'], 'values': [5, 20, 35]})
        #           ])
        #       ])
        #   ])

        # OUT:
        # type: 'line',
        # data: {
        #     labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'Sept', 'Oct', 'Nov', 'Dec'],
        #     datasets: [{
        #         label: 'Africa',
        #         backgroundColor: '#3e95cd',
        #         borderColor: '#3e95cd',
        #         data: [2, 4, 8, 16, 32, 64, 128, 64, 32, 16, 8, 4],
        #         fill: false,
        #     }, {
        #         label: 'Asia',
        #         backgroundColor: '#8e5ea2',
        #         borderColor: '#8e5ea2',
        #         data: [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144],
        #         fill: false,
        #     }]

            x = []
            for d in data['datasets']:
                for i in d['entries']['keys']:
                    x.append(i)
            labels = set(x)

            chart_data = {
                # 'selector': ,
                'type': chart_type,
                'data': {
                    'labels': labels,
                    'datasets': [{
                        'label': dataset['dataset_label'],
                        'data': dataset['entries']['values'],
                    } for dataset in data['datasets']],
                },
                'options': {
                    'title': {
                        'display': True,
                        'text': data['chart_title'],
                    }
                }
            }

        else:

        # IN:
        # OrderedDict([
        #   ('chart_title', 'Bar Chart'),
        #   ('chart_type', 'bar'),
        #   ('datasets', [
        #       OrderedDict([
        #           ('dataset_label', 'Population'),
        #           ('entries', {'keys': ['Africa', 'Asia', 'Europe'], 'values': [10, 40, 30]})])])])

        # OUT:
        # type: 'bar',
        # data: {
        #     labels: ['Africa', 'Asia', 'Europe'],
        #     datasets: [{
        #         label: 'Population',
        #         backgroundColor: ['#3e95cd', '#8e5ea2', '#3cba9f'],
        #         data: [10, 40, 30]
        #     }]
        # },
        # options: {
        #   legend: { display: false },
        #   title: {
        #     display: true,
        #     text: 'Predicted world population (millions) in 2050'
        #   }
        # }

            if len(data['datasets']) == 1:

                print(type(data['datasets']))

                chart_data = {
                    'type': chart_type,
                    'data': {
                        'labels': data['datasets'][0]['entries']['keys'],
                        'datasets': [{
                            'label': data['datasets'][0]['dataset_label'],
                            'data': data['datasets'][0]['entries']['values'],
                        }]
                    },
                    'options': {
                    'title': {
                        'display': True,
                        'text': data['chart_title'],
                        }
                    }
                }

        return chart_data


        # chart_data = {
        #   # 'selector': data['data']['data'].pop('selector'),
        #   'type': data['_type'],
        #   'chart_data': data['data'].pop('data'),
        # }

    #   return chart_data