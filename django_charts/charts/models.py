from django.db import models


class DataSet(models.Model):
	# chart = models.OneToOneField(Chart, on_delete='CASCADE')
	title = models.CharField(max_length=20)

	def __str__(self):
		return '{}'.format(self.title)


class Entry(models.Model):
	data_set = models.ForeignKey(DataSet, on_delete='CASCADE')
	key = models.CharField(max_length=20)
	value = models.IntegerField()

	def __str__(self):
		return '{}: {} 	{}'.format(self.data_set.title, self.key, self.value)



class ChartType(models.Model):
	LINE = 'line'
	BAR = 'bar'
	RADAR = 'radar'
	DOUGHNUT = 'doughnut'
	PIE = 'pie'
	POLAR = 'polar'
	BUBBLE = 'bubble'
	SCATTER = 'scatter'
	AREA = 'area'
	MIXED = 'mixed'
	CHART_CHOICES = [
		(LINE, 'Line'),
		(BAR, 'Bar'),
		(RADAR, 'Radar'),
		(DOUGHNUT, 'Doughnut'),
		(PIE, 'Pie'),
		(POLAR, 'Polar'),
		(BUBBLE, 'Bubble'),
		(SCATTER, 'Scatter'),
		(AREA, 'Area'),
		(MIXED, 'Mixed'),
	]
	_type = models.CharField(max_length=2, choices=CHART_CHOICES, default=LINE)

	def __str__(self):
		return self._type

class Chart(models.Model):
	type = models.ForeignKey(ChartType, on_delete='CASCADE')
	data = models.ForeignKey(DataSet, on_delete='CASCADE')
	# options

	def __str__(self):
		return '{}: {}'.format(self.type, self.data)