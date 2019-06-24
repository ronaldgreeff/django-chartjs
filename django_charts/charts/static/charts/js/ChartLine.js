$.ajax({
    url: endpoint,
    method: "GET",
    dataType: 'json',
    success: function(data){

        var data;

        for (data_set in data) {
            var selector = data[data_set]["selector"];
            var chart_type = data[data_set]["type"];
            var chart_data = data[data_set]["data"];
            var chart_options = data[data_set]["options"];


            (function() {
                var chart = new Chart(document.getElementById(selector), {
                    type: chart_type,
                    data: chart_data,
                    options: chart_options,
                });
            })();
        };
    },

    error: function(error_data){
        console.log("error")
        console.log(error_data)
    },
});