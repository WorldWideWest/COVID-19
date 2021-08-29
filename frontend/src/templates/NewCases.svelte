<script>
    import { covid } from "../stores/covidStore";
	import * as d3 from 'd3';
    import { onMount } from "svelte";
    
    let el;
    let data = [];

    $:{
        data = [...$covid],
        render(data)
    }
    
    const render = data => {
        const width = 1000;
        const height = 400;
        
        // Defining the Chart area

        const margin = {top: 40, right: 70, bottom: 50, left: 90}
        const innerWidth = width - margin.left - margin.right;
        const innerHeight = height - margin.top - margin.bottom;


        const svg = d3.select(el).append("svg")
            .attr("preserveAspectRatio", "xMinYMin meet")
            .attr("viewBox", "0 0 960 400");

        const xValue = d => new Date(d.date);
        const yValue = d => +d.new_cases;

        // Defining the Scales
        const xScale = d3.scaleTime()
            .domain(d3.extent(data, xValue))
            .range([0, innerWidth])
            .nice();
        
        const yScale = d3.scaleLinear()
            .domain(d3.extent(data, yValue))
            .range([innerHeight, 0]);

        const g = svg.append("g")
            .attr("transform", `translate(${ margin.left }, ${ margin.top })`);
        
        // Defining the Axis
        const xAxis = d3.axisBottom(xScale);
        xAxis.tickSize(-innerHeight).tickPadding(20);

        const yAxis = d3.axisLeft(yScale);
        yAxis.tickSize(-innerWidth).tickPadding(20)

        // Grouping the yAxis
        const yAxisGroup = g.append("g").call(yAxis);
        yAxisGroup.selectAll(".domain").remove();
            
        yAxisGroup.append('text')
            .text("Number of new Cases")
            .attr("transform", `rotate(-90)`)
            .attr("fill", "black")
            .attr("x", -innerHeight / 2)
            .attr("y", -80)
            .attr("class", "y-axis-label")
            .style("text-anchor", "middle")
            .style("font-size", 14);            

        // Grouping the xAxis
        const xAxisGroup = g.append('g').call(xAxis)
            .attr("transform", `translate(0, ${ innerHeight })`)
        xAxisGroup.selectAll(".domain").remove();

        xAxisGroup.append('text')
            .text("Time")
            .attr("fill", "black")
            .attr("class", "x-axis-label")
            .style("font-size", 14)
            .attr("x", innerWidth / 2)
            .attr("y", 50);

        // Title
        g.append('text')
            .text("COVID-19 New Cases per day from March 2020. - Aug 2021.")
            .attr("x", innerWidth / 4)
            .attr("y", -10)
            .attr("class", "title")
            .style("font-size", 20);
            
        // Line chart generator
        const lineGenerator = d3.line()
            .x(d => xScale(xValue(d)))
            .y(d => yScale(yValue(d)))
            .curve(d3.curveBasis);

        g.append("path")
            .attr("class", "line")
            .attr("d", lineGenerator(data))
            .style("fill", "none")
            .style("stroke", "#051014")
            .style("stroke-width", 2)
            .style("stroke-linejoin", "round");
    }


</script>


<div bind:this={el} class="chart"></div>
