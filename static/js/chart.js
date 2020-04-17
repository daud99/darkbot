    $.get('{% url "adminpanel:doughnutchart" %}', function(data) {
            var ctx = document.getElementById('agentSearchDoughnut');
            var myChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                        datasets: [{
                            data: data.l,
                            backgroundColor: [
                                "purple","red","orange","green","blue"
                            ]
                        }],

                        // These labels appear in the legend and in the tooltips when hovering different arcs
                        labels: data.labels
                    }
            });
                    });

    {#    polar chart stuff below #}

        $.get('{% url "adminpanel:polarchart" %}', function(data) {
            var ctx = document.getElementById('polarChart');
            var myChart = new Chart(ctx, {
                type: 'polarArea',
                data: {
                        datasets: [{
                            data: data.data,
                            backgroundColor: [
                                "purple","red","orange"
                            ]
                        }],

                        // These labels appear in the legend and in the tooltips when hovering different arcs
                        labels: data.labels
                    }
            });
                    });

    {#    histogram chart stuff bottom #}

    $.get('{% url "adminpanel:histogramchart" %}', function(data) {
            var ctx = document.getElementById('histogramChart');
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