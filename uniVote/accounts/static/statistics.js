$(document).ready(function() {


    // variables to hold the graph data
    var raceList = [];
    var candidate;
    var votes;
    var graph;

    // get the graph data
    $(".graphData").each(function(){
        $(this).children(".candidates").each(function(){
            candidate = $(this).text();
        });
        $(this).children(".votes").each(function(){
            votes = Math.floor($(this).text());
        });
        $(this).children(".counter").each(function(){
            graph = Math.floor($(this).text());
        });
        raceList.push({which_graph: graph, which_cand: candidate, num_votes: votes});
    });
    console.log(raceList);




    // make the charts
    $(".myChart").each(function(iter){

        // Get context with jQuery - using jQuery's .get() method.
        var ctx = $(this).get(0).getContext("2d");

        var names = [];
        var numvotes = [];
        for (var i=0; i<raceList.length; i++) {
            if (raceList[i].which_graph === iter) {
                names.push(raceList[i].which_cand);
                numvotes.push(raceList[i].num_votes);
            }
        }
        console.log(numvotes);

        var data = {
            labels: names,
            datasets: [
                {
                    label: "Vote Dataset",
                    fillColor: "rgba(192, 57, 43, 0.8)",
                    strokeColor: "rgba(236,236,236,0.8)",
                    highlightFill: "rgba(192, 57, 43, 0.6)",
                    highlightStroke: "rgba(220,220,220,1)",
                    data: numvotes
                }
            ]
        };


        var options =
        {
            //Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
            scaleBeginAtZero : true,

            //Boolean - Whether grid lines are shown across the chart
            scaleShowGridLines : true,

            //String - Colour of the grid lines
            scaleGridLineColor : "#2980b9",

            //Number - Width of the grid lines
            scaleGridLineWidth : 2,

            //Boolean - If there is a stroke on each bar
            barShowStroke : true,

            //Number - Pixel width of the bar stroke
            barStrokeWidth : 2,

            //Number - Spacing between each of the X value sets
            barValueSpacing : 15,

            //Number - Spacing between data sets within X values
            barDatasetSpacing : 1,

            scaleFontColor: "#2c3e50",

            //String - A legend template
            legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].lineColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"

        }


        // This will get the first returned node in the jQuery collection.
        var myNewChart = new Chart(ctx).Bar(data, options);
    });

});