# django-chartjs
A Django + charts.js implementation

The background to this project was the need to provide 200+ users, split into "members" and "admins", with various graphs. For performance reasons, a query is performed as specified intervals and calculations stored in a separate database.

As such, the model is pretty simple - a DataSet and an Entry (an Entry having a many-to-one relationship with a DataSet). Each Entry is essentially a datapoint in a DataSet to be graphed.

DataSets are serialized into the correct graph format (as required by ChartJS), with chart options and colour schemes added as an easily amended mapping.

It's assumed that all admin-graphs should be visible to all admins, and all member-graphs to members. Each DataSet is therefore automatically added to the REST API (split into members and admins) and also made available as context variables.
