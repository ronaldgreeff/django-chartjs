from charts.models import *
from rest_framework import serializers


# class EntrySerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = Entry
# 		fields = '__all__'


class DataSetSerializer(serializers.Serializer):

	data = serializers.SerializerMethodField()

	def get_data(self, obj):

		labels = [d.key for d in obj.entry_set.all()]
		data = [d.value for d in obj.entry_set.all()]
		label = obj.title
		selector = '{}{}'.format(obj.id, obj.title.lower().replace(' ', '_'))

		return {
			'selector': selector,
			'labels': labels,
			'datasets': [{
				'label': label,
				'data': data
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