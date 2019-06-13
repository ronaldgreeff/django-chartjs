from django.db import models
from django.contrib.auth.models import Group


class Chart(models.Model):
	BAR = 'bar'
	# HORIZONAL = 'horizontalBar',
	PIE = 'pie'
	DOUGHNUT = 'doughnut'
	POLAR = 'polar'
	LINE = 'line'
	RADAR = 'radar'
	CHART_CHOICES = [
		(BAR, 'Bar'),
		# (HORIZONAL, 'HorBar'),
		(PIE, 'Pie'),
		(DOUGHNUT, 'Doughnut'),
		(POLAR, 'Polar'),
		(LINE, 'Line'),
		(RADAR, 'Radar'),
	]
	chart_title = models.CharField(max_length=20, ) # change to chart_title
	chart_type = models.CharField(max_length=10, choices=CHART_CHOICES, default=LINE) # change to chart_type
	chart_group = models.ForeignKey(Group, on_delete='CASCADE') # change to chart_group

	def __str__(self):
		return '{} | ({} {} {})'.format(self.chart_title, self.id, self.chart_type, self.chart_group)


class DataSet(models.Model):
	chart = models.ForeignKey(Chart, on_delete='CASCADE', related_name='datasets')
	dataset_label = models.CharField(max_length=20) # change to dataset_label

	def __str__(self):
		return 'DATASET: {} (CHART: {})'.format(self.dataset_label, self.chart)


class Entry(models.Model):
	data_set = models.ForeignKey(DataSet, on_delete='CASCADE', related_name='entries')
	key = models.CharField(max_length=20)
	value = models.IntegerField()

	def __str__(self):
		return 'K:{}: V:{} 	({})'.format(self.key, self.value, self.data_set)