function renderDonutGraph(div_id,dat){
	var ctx = document.getElementById(div_id).getContext("2d");

	// var data = [
	//     {
	//         value: 300,
	//         color:"#F7464A",
	//         highlight: "#FF5A5E",
	//         label: "Red"
	//     },
	//     {
	//         value: 50,
	//         color: "#46BFBD",
	//         highlight: "#5AD3D1",
	//         label: "Green"
	//     },
	//     {
	//         value: 100,
	//         color: "#FDB45C",
	//         highlight: "#FFC870",
	//         label: "Yellow"
	//     },
	// ]

	data=dat

	var options={
	    //Boolean - Whether we should show a stroke on each segment
	    segmentShowStroke : true,

	    //String - The colour of each segment stroke
	    segmentStrokeColor : "#eee",

	    //Number - The width of each segment stroke
	    segmentStrokeWidth : 2,

	    //Number - The percentage of the chart that we cut out of the middle
	    percentageInnerCutout : 50, // This is 0 for Pie charts

	    //Number - Amount of animation steps
	    animationSteps : 100,

	    //String - Animation easing effect
	    animationEasing : "easeOutBounce",

	    //Boolean - Whether we animate the rotation of the Doughnut
	    animateRotate : true,

	    //Boolean - Whether we animate scaling the Doughnut from the centre
	    animateScale : false,

	    // String - Template string for single tooltips
    	tooltipTemplate: "<%if (label){%><%=label%>: <%}%><%= value %>",

	    //String - A legend template
	    legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"

	}

	var myChart = new Chart(ctx).Doughnut(data,options);
	// var legend = myChart.generateLegend();
	// document.getElementById("subredLegend").innerHTML = legend;
}

function renderBarGraph(div_id,dat,labs){
	var ctx = document.getElementById(div_id).getContext("2d");

	var data = {
    // labels: ['January', "February", "March", "April", "May", "June", "July"],
    labels: labs,
    datasets: [
        {
            label: "My First dataset",
            fillColor: "#720733",
            strokeColor: "rgba(220,220,220,0.8)",
            highlightFill: "#AB0C4D",
            highlightStroke: "rgba(220,220,220,1)",
            // data: [65, 59, 80, 81, 56, 55, 40],
            data: dat
        }
        ]
	};

	var options={
	    //Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
	    scaleBeginAtZero : true,

	    //Boolean - Whether grid lines are shown across the chart
	    scaleShowGridLines : true,

	    //String - Colour of the grid lines
	    scaleGridLineColor : "rgba(0,0,0,.05)",

	    //Number - Width of the grid lines
	    scaleGridLineWidth : 1,

	    //Boolean - Whether to show horizontal lines (except X axis)
	    scaleShowHorizontalLines: false,

	    //Boolean - Whether to show vertical lines (except Y axis)
	    scaleShowVerticalLines: false,

	    //Boolean - If there is a stroke on each bar
	    barShowStroke : true,

	    //Number - Pixel width of the bar stroke
	    barStrokeWidth : 1,

	    //Number - Spacing between each of the X value sets
	    barValueSpacing : 10,

	    //Number - Spacing between data sets within X values
	    barDatasetSpacing : 30,

	    //String - A legend template
	    legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].fillColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"

	}

	var myChart = new Chart(ctx).Bar(data,options);
	// var legend = myChart.generateLegend();
	// document.getElementById("subredLegend").innerHTML = legend;
}