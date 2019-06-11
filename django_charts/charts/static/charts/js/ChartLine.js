$.ajax({
    url: endpoint,
    method: "GET",
    dataType: 'json',
    success: function(data){

        var data;

        for (data_set in data) {
            var selector = data[data_set]['selector'];
            var chart_type = data[data_set]['type'];
            var chart_data = data[data_set]["chart_data"];

            (function() {
                var ctx = document.getElementById(selector);
                var chart = new Chart(ctx, {
                    type: chart_type,
                    data: chart_data,
                });
            })();
        };
    },

    error: function(error_data){
        console.log("error")
        console.log(error_data)
    },
});