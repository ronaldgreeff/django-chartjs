// var endpoint = "{{ endpoint }}";
// var defaultData = [];
// var labels = [];

// $( document ).ready(function() {
//     console.log( "ready!" );
// });

$.ajax({
    url: endpoint,
    method: "GET",
    dataType: 'json',
    success: function(data){

        var data;

        for (data_set in data) {
            var dataset = data[data_set];

            (function() {
                var ctx = document.getElementById(dataset["selector"]);
                var chart = new Chart(ctx, {
                    type: dataset["type"],
                    data: dataset["chart_data"],
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