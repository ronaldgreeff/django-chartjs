// var endpoint = "{{ endpoint }}";
// var defaultData = [];
// var labels = [];

// $( document ).ready(function() {
//     console.log( "ready!" );
// });

function randomColors() {
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    return "rgba(" + r + "," + g + "," + b + ", 0.5)";
};

function poolColors(a) {
    var pool = [];
    for(i = 0; i < a; i++) {
        pool.push(randomColors());
    };
    return pool;
};

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

            for (i=0; i<chart_data['datasets'].length; i++) {
                var chart_data_datasets = chart_data['datasets'][0];
                var data_len = chart_data_datasets['data'].length;

                console.log(chart_data_datasets, data_len)

                chart_data_datasets.backgroundColor = poolColors(data_len);
                chart_data_datasets.borderColor = poolColors(data_len);
            };

            (function() {
                var ctx = document.getElementById(selector);
                var chart = new Chart(ctx, {
                    type: chart_type,
                    data: chart_data,
                    // backgroundColor: poolColors(dataset["type"].length),
                    // borderColor: poolColors(dataset["type"].length),
                    borderWidth: 1,
                });
            })();
        };
    },

    error: function(error_data){
        console.log("error")
        console.log(error_data)
    },
});

// function setChart1(){
//     var ctx = document.getElementById("LineChart");
//     var myChart = new Chart(ctx, {
//     type: 'line',
//     data: {
//         labels: data['Dataset 1']['data']['labels'],
//         datasets: [{
//             line_label: line_label,
//             data: defaultData,
//             backgroundColor: [
//                 'rgba(255, 99, 132, 0.2)',
//                 'rgba(54, 162, 235, 0.2)',
//                 'rgba(255, 206, 86, 0.2)',
//                 'rgba(75, 192, 192, 0.2)',
//                 'rgba(153, 102, 255, 0.2)',
//                 'rgba(255, 159, 64, 0.2)'
//             ],
//             borderColor: [
//                 'rgba(255,99,132,1)',
//                 'rgba(54, 162, 235, 1)',
//                 'rgba(255, 206, 86, 1)',
//                 'rgba(75, 192, 192, 1)',
//                 'rgba(153, 102, 255, 1)',
//                 'rgba(255, 159, 64, 1)'
//             ],
//             borderWidth: 1
//         }]
//     },
//     options: {
//         scales: {
//             yAxes: [{
//                 ticks: {
//                     beginAtZero:true
//                 }
//             }]
//         }
//     }
// });
// };