# django-chartjs
A Django + charts.js implementation

Uses a simple model of DataSet, Entry (one DataSet object - many Entry objects), ChartType and Chart (Chart is a mapping table of ChartType + DataSet).

DataSet is serialized into a format easily passed via a context variable to a ChartJS chart object.
