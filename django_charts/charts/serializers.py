from charts.models import *
from rest_framework import serializers


background_colours = [
	'#3e95cd',
	'#8e5ea2',
	'#3cba9f',
	'#e8c3b9',
	'#c45850',
]


class DataSetSerializer(serializers.Serializer):

	data = serializers.SerializerMethodField()

	def get_data(self, obj):

		label = obj.title
		selector = '{}{}'.format(obj.id, obj.title.lower().replace(' ', '_'))


		labels = [d.key for d in obj.entry_set.all()]
		data_points = [d.value for d in obj.entry_set.all()]
		backgroundColor = background_colours[(obj.id-1)]

		# generate a list of dicts (datasets) here
		datasets = {}

		return {
			'selector': selector,
			'labels': labels,
			'datasets': [{ # this list needs to be dynamic and include backgroundColor
				'label': label,
				'data': data_points,
				'backgroundColor': backgroundColor,
			}]
		}

class ChartSerializer(serializers.Serializer):

	_type = serializers.CharField()
	data = DataSetSerializer()

	def to_representation(self, obj):

		data = super(ChartSerializer, self).to_representation(obj)

		chart_data = {
			'selector': data['data']['data'].pop('selector'),
			'type': data['_type'],
			'chart_data': data['data'].pop('data'),
		}

		return chart_data