document.addEventListener("DOMContentLoaded", function() {
    // Get the div where the data is stored
    var dataDiv = document.getElementById('data');
    if(dataDiv) {
        // Get the data using `getAttribute`
        var records = JSON.parse(dataDiv.getAttribute('data-records'));
        // Your existing code that uses the records goes here...

    } else {
        console.log("dataDiv is null. Div with id 'data' not found.")
    }
});


// Get the div where the data is stored
var dataDiv = document.getElementById('data');
// Get the data using `getAttribute`
var records = JSON.parse(dataDiv.getAttribute('data-records'));

// Count the number of records per category
var counts = {};
records.forEach(function(record) {
    if (!(record.category in counts)) {
        counts[record.category] = 0;
    }
    counts[record.category]++;
});

// Convert the counts to an array of objects
var data = Object.keys(counts).map(function(category) {
    return {
        category: category,
        count: counts[category]
    };
});

// Set the dimensions of the chart
var width = 500;
var height = 500;

// Create the SVG element
var svg = d3.select("#bar-chart")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

// Create the x scale
var x = d3.scaleBand()
    .range([0, width])
    .domain(data.map(function(d) { return d.category; }))
    .padding(0.1);

// Create the y scale
var y = d3.scaleLinear()
    .range([height, 0])
    .domain([0, d3.max(data, function(d) { return d.count; })]);

// Add the bars
svg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", function(d) { return x(d.category); })
    .attr("width", x.bandwidth())
    .attr("y", function(d) { return y(d.count); })
    .attr("height", function(d) { return height - y(d.count); });

// Add the x axis
svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

// Add the y axis
svg.append("g")
    .call(d3.axisLeft(y));