# django-chartjs
A Django + charts.js implementation

Brief: ~200 members submit quarterly figures. Provide something in return to members in the form of data visualisation / charts
Rationale: Submission every quarter / client already has a standard dataset they extract every quarter, so run preset queries at submission close; process and store the results in database to reduce computing.

# Model:
Chart -< DataSet -< Entry

# View:
ChartSerialiser (ready data before it's sent to database as JSON)
AdminGraphView (retrieve stored data and send to front-end)

# Serializers:
Pre-configured settings for consistancy between generated charts and chart customisation.
`
  ## ChartSerializer(Serializer):
  """ convert data into the format required by chartjs package """
    title, charty_type and data
    to_representation()
    apply specific options based on chart type, colours, standard settings
    generate chart selector
    return chart
`
