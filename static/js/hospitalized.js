// Call Dates Route
d3.json(`/dates`).then(data => {

    // Select & Save Dropdown 
    var dropdown = d3.select("#selDate")

    // For Each Date
    data.forEach(entry => {

        // Append Date Into Dropdown
        dropdown.append('option').attr('value', entry).text(entry).property('value')
    })

    // Create Load Page Function
    function loadPage(date) {

        // Call Route
        d3.json(`/hospitalized/${date}`).then(data => {

            // Empty Array to Hold States
            var bar_states = []

            // For Loop to Push States to Array
            for (var i = 0; i < data.length; i++) {
                bar_states.push(data[i][2])
            }

            // Empty Array to Hold Values
            var bar_hospitalized = []

            // For Loop to Push Values to Array
            for (var i = 0; i < data.length; i++) {
                bar_hospitalized.push(data[i][0])
            }

            // Em,pty Array to Hold Colors
            var bar_color = []

            // For Loop to Push Colors to Array
            for (var i = 0; i < data.length; i++) {
                if (data[i][3] === "R") { bar_color.push("red") } else if (data[i][3] === "D") { bar_color.push("blue") }
            }

            // Create Bar Data
            var barData = [{
                x: bar_hospitalized,
                y: bar_states,
                transforms: [{
                    type: 'sort',
                    target: 'x',
                    order: 'ascending'
                }],
                text: bar_states,
                marker: {
                    color: bar_color
                },
                type: 'bar',
                orientation: 'h'
            }]

            // Create Bar Layout
            var barLayout = {
                font: { color: 'white' },
                yaxis: {
                    autorange: true,
                    type: 'category',
                    title: {
                        text: 'State',
                        font: { color: 'white' }
                    }
                },
                xaxis: {
                    title: {
                        text: 'Number of People',
                        font: { color: 'white' }
                    }
                },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                margin: {
                    l: 100,
                    r: 100,
                    t: 10,
                    b: 50
                }

            }

            // Plot Bar Chart 
            Plotly.newPlot("bar", barData, barLayout, responsive = true)
        })
    }

    // Create Init Function
    function init() {

        // Select & Save Date from Dropdown
        var date = dropdown.property('value', $('#selDate option:last-child').val())

        // Deploy Load Page Function
        loadPage($('#selDate option:last-child').val())

        // On Change
        d3.selectAll("#selDate").on("change", function() {

            // Select & Save Date from Dropdown
            var date = dropdown.property('value')

            // Deploy Load Page Function
            loadPage(date)
        })
    }

    // Deploy Init Function
    init()
        // jQuery CSS
    $(document).ready(function() {
        $('#covid-jumbotron').css("background-color", "black")
        $('#covid-well').css("background-color", "black")
        $('#covid-panel-default').css("background-color", "black")
        $('body').attr('style', 'background-color: black !important')
        $('h1').attr('style', 'color: white !important')
        $('h3').attr('style', 'color: white !important')
        $('h5').attr('style', 'color: white !important')
        $('.color').attr('style', 'color: red !important')
        $('.center').attr('style', 'text-align: center !important')
        $('.panel-title').attr('style', 'color: white !important')
        $('.panel-heading').attr('style', 'background-color: red !important')
    })
})