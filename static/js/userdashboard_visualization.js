$(document).ready(function(){
    console.log('aaaa');
     $.get("doughnutchart", function(data) {
            var ctx = document.getElementById('agentSearchDoughnut');
            var myChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                        datasets: [{
                            data: data.l,
                            backgroundColor: [
                                "red","green"
                            ]
                        }],

                        // These labels appear in the legend and in the tooltips when hovering different arcs
                        labels: data.labels
                    }
            });
                    });

          $.get("daychart", function(data) {
            var ctx = document.getElementById('dayChart');
            var myChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                        datasets: [{
                            data: data.l,
                            backgroundColor: [
                                "red","green"
                            ]
                        }],

                        // These labels appear in the legend and in the tooltips when hovering different arcs
                        labels: data.labels
                    }
            });
                    });
          $.get("histogramchart", function(data) {
            var ctx = document.getElementById('myChart');
            var myChart = new Chart(ctx, {
                            type: 'bar',
                            data: {
                                labels: data.labels,
                                datasets: [{
                                    label: '# of Searches W.R.T Types',
                                    data: data.data,
                                    backgroundColor: [
                                        'rgba(255, 99, 132, 0.2)',
                                        'rgba(54, 162, 235, 0.2)',
                                        'yellow',
                                        'rgba(75, 192, 192, 0.2)',
                                        'rgba(153, 102, 255, 0.2)',
                                        'rgba(255, 159, 64, 0.2)'
                                    ],
                                    borderColor: [
                                        'rgba(255, 99, 132, 1)',
                                        'rgba(54, 162, 235, 1)',
                                        'rgba(255, 206, 86, 1)',
                                        'rgba(75, 192, 192, 1)',
                                        'rgba(153, 102, 255, 1)',
                                        'rgba(255, 159, 64, 1)'
                                    ],
                                    borderWidth: 1
                                }]
                            },
                            options: {
                                scales: {
                                    yAxes: [{
                                        ticks: {
                                            beginAtZero: true
                                        }
                                    }]
                                }
                            }
                        });
                    });

});