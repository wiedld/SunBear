var state_name;
var fuel_names;

// function called by donut arc tip tool
var getKeyByValue = function( value, obj ) {
    for( var prop in obj ) {
        if( obj.hasOwnProperty( prop ) ) {
             if( obj[ prop ] === value )
                 return prop;
        }
    }
}

function updateData(){
        // Updates colors based on changes to data.
        //console.log("updateData() fired with value ",myVariableNames[myVariableIndex]);
        //console.log("the size of myTransitionStack is",myNodes[0].length);
        
         myNodes.transition().duration(200)
                .style("fill",function(d){try{return colorScale(inputScale(+d.energyData[myVariableNames[myVariableIndex]]));}catch(err){return "#aaa";} } );
        //update();

}

var tooltip = d3.select("body")
    .append("div")
    .attr("class","tooltip")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden");

// General function useful for processing strings for display
if (!String.prototype.format) {
        String.prototype.format = function() {
            var str = this.toString();
            if (!arguments.length)
                return str;
            var args = typeof arguments[0],
                args = (("string" == args || "number" == args) ? arguments : arguments[0]);
            for (arg in args)
                str = str.replace(RegExp("\\{" + arg + "\\}", "gi"), args[arg]);
            return str;
        }
}

var tooltipText = "Name: {0}<br>Value: {2}"; // To be used in the str.format(replace1,replace2,replace3) format

var colorScale = d3.scale.linear()
    .interpolate(d3.interpolateHcl)
    
    //.domain([0,0.25,0.5,0.75,1])
    //.range(["purple","blue","green","yellow","red"]);
    
    //.domain([0,0.33,0.66,1])
    //.range(["blue","green","yellow","red"]);
    
    .domain([0,10,20])
    .range(["green","yellow","red"]);

function displayToolTip(d){
        // Show appropriate text in the tooltip.  This will be turned off when 
        tooltip.style("visibility", "visible");
        tooltip.style("top", (event.pageY-50)+"px").style("left",(event.pageX-60)+"px");
        try{
                tooltip.html(tooltipText.format(d.name,d.energyData[myVariableNames[myVariableIndex]]) );
        }
        catch(err){
                tooltip.html(tooltipText.format(d.name,"") );		// Some nodes may not have defined energyData for this value

        }
}

// UNIQUE CODING FOR THE STATES USA MAP /////////////////////////////////////

  // list of what is different for this scripts2 (versus original):
    // changed all references of "county" --> "state".  "counties" --> "states"
    // added the novel functionality below
    // used mbostock's us.json file.  Had to search state_name_dict to get the code used in the map data pass up to the frontend (see make topojson function)
    // RunScenarioUSA -- function name, and flask route name
    // make_topojson_map_usa -- function name, and size of map rendering (ver height=650



function get_map_data_usa(evt){
  evt.preventDefault();
  // console.log("get_map_data js function");

  var data = "yo";
  $.ajax('usa-map-data', {
    type: 'POST',
    data: data,
    contentType: 'application/json',
    success: function(data, status, result){
      fuel_mix = JSON.parse(result.responseText);
      console.log(fuel_mix);
    }
  });
}

var fuel_mix = {};
window.onload = get_map_data_usa;

var state_name_dict = {
  1: ["AL", "Alabama"],
  2: ["AK", "Alaska"],
  4: ["AZ", "Arizona"],
  5: ["AR",, "Arkansas"],
  6: ["CA", "California"],
  8: ["CO", "Colorado"],
  9: ["CT", "Connecticut"],
  10: ["DE", "Delaware"],
  11: ["DC", "District of Washington"],
  12: ["FL", "Florida"],
  13: ["GA", "Georgia"],
  15: ["HI", "Hawaii"],
  16: ["ID", "Indiana"],
  17: ["IL", "Illinois"],
  18: ["IN", "Indiana"],
  19: ["IA", "Iowa"],
  20: ["KS", "Kansas"],
  21: ["KY", "Kentucky"],
  22: ["LA", "Louisiana"],
  23: ["ME", "Maine"],
  24: ["MD", "Maryland"],
  25: ["MA", "Massachusetts"],
  26: ["MI", "Michigan"],
  27: ["MN", "Minnesota"],
  28: ["MS", "Mississippi"],
  29: ["MO", "Missouri"],
  30: ["MT", "Montana"],
  31: ["NE", "Nebraska"],
  32: ["NV", "Nevada"],
  33: ["NH", "New Hampshire"],
  34: ["NJ", "New Jersey"],
  35: ["NM", "New Mexico"],
  36: ["NY", "New York"],
  37: ["NC", "North Carolina"],
  38: ["ND", "North Dakota"],
  39: ["OH", "Ohio"],
  40: ["OK", "Oklahoma"],
  41: ["OR", "Oregon"],
  42: ["PA", "Pennsylvania"],
  44: ["RI", "Rhode Island"],
  45: ["SC", "South Carolina"],
  46: ["SD", "South Dakota"],
  47: ["TN", "Tennessee"],
  48: ["TX", "Texas"],
  49: ["UT", "Utah"],
  50: ["VT", "Vermont"],
  51: ["VA", "Virginia"],
  53: ["WA", "Washington"],
  54: ["WV", "West Virginia"],
  55: ["WI", "Wisconsin"],
  56: ["WY", "Wyoming"]
};





///////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////
//  SLIDERS, with src js script import in html DOM, before this js file


var set_slider_values = function(data_list,state_name){

    // make the sliders

    // var axis = d3.svg.axis().orient("top").ticks(5);

    fuel_names = ["gas", "coal", "solar", "wind", "nuclear", "hydro", "other"];
    var slider_elements = ["#slider0", "#slider1", "#slider2", "#slider3", "#slider4", "#slider5", "#slider6"];

    $.each(slider_elements, function(idx, slider_element){
        d3.select(slider_element).call(d3.slider()
          .value(data_list[idx])
          .on("slide", function(evt, value){
            slide_event(value, fuel_names, idx, data_list);
            }
          )
        );
    });


    // show the starting values in the html
    for (var i = 0; i<7; i++){
      d3.select('#slider'+i+'text').text(data_list[i]);
    }
};


    // what happens when the sliders are changed by the user.
    var slide_event = function(value, fuel_names, index, data_list){
        value = Math.round(value);
        // update_percentages() for all fuels, to sum to 100%
        data_list = update_percentages(value,index, data_list);

        for (var i = 0; i<7; i++){
          // need to empty sliders, to then re-render
          $('#slider'+i+'').empty();
          // change values in the fuel_mix dict
          fuel_mix[state_name][fuel_names[i]] = data_list[i];
        }
        //re-render sliders
        set_slider_values(data_list,state_name);

        //update the donut
        $('#fuel-donut').empty();
        make_donut(data_list);
    };

    // PERCENTAGES -
    var update_percentages = function(value, index, data_list){
          // update percentages based on amt slider changed
          var amt_changed = value - data_list[index];
          data_list[index] = value;  // this single slider value went up

          for (var i = 0; i<7; i++){
            if (i != index){
              // scale amt to change by original.
              // so if coal 75% of total, but user made 4% increase in solar,  then coal gets decreased by 75% of 4% (=3%).
              var adjuster = Math.round(amt_changed * (data_list[i]/100));
              data_list[i] = data_list[i] - adjuster;
            }
          }
          // console.log(data_list);
          return data_list;
    };



//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////
// TOPOJSON -- COUNTY MAP  ///////////////////////////////////////////////


var make_topojson_map_usa = function(){

    // MAKE THE SVG

      // define variables, to use later.
      var width = 800,
          height = 700,
          centered;

      // creates the svg object and adds to the body in the DOM.
      var svg = d3.select("#topomap").append("svg")
          .attr("width", width)
          .attr("height", height);

      // adds a rect to the svg, and adds an event listener
      svg.append("rect")
          .attr("class", "background")
          .attr("width", width)
          .attr("height", height)
          .on("click", clicked);


  // MAKE AN IDEA OF A MAP

      // "projection" -- how to display this svg vector data.
      //  geo.albersUSA is like a dictionary of how to translate geojson vector numbers?
      var projection = d3.geo.albersUsa()
          .scale(1070)
          .translate([width / 2, height / 2]);

      // d3.geo.path maps geocoordinates to svg.
      // .projection() links the projection var to the geo.path
      var path = d3.geo.path()
          .projection(projection);
      // so when we later refer to "path" attr, we have a path dict which matches the project dict from geo.albersUsa?


      // adds a DOM object "g" to the svg. and assigns to var g
      // we can now add to the svg by referring to g
      var g = svg.append("g");


  // GIVE THE MAP DATA TO DRAW

      // take the json data
      d3.json("/static/maps/us.json", function(error, us) {
        // append another "g" DOM element to the already present (bigger) g? Making a child?
        g.append("g")
          // each new "g" has the property "id", as taken from the json object "states"?
          //.on("mouseover", function() {d3.select(this).style("cursor","zoom-in");})
          .attr("id", "states")
          // select all "path" properties from witin the svg object g,
          .selectAll("path")
          // and assign the topojson vector info to the "path" attr of the g object
            .data(topojson.feature(us, us.objects.states).features)
          .enter().append("path")
            .attr("d", path)
            
            // add event listener
            //.on("mouseover", console.log("BOOP"))
            //.on("mouseover", displayToolTip)
	    //.on("mousemove", displayToolTip)
            //.on("mouseout", function(){return tooltip.style("visibility", "hidden");})
            .on("click", clicked);
            //.on("click", console.log("BOOP"));


        // to the g object, also add the path association with the borders.
        // unclear how it knows this is the borders
        g.append("path")
            .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
            .attr("id", "state-borders")
            .on("mouseover", console.log("BOOP"))
            //.on("mouseover", displayToolTip)
	    .on("mousemove", displayToolTip)
            .attr("d", path);
      });
      
      d3.json("static/data/state_val.json",function(d) { d3.map().set(d.id, +d.val); })
      



    //JS INTERACTIVITY

      // js function.  for moving the clicked state to the center
      function clicked(d) {

        var x, y, k;

            // if clicking on a state (d)
            if (d && centered !== d) {
              var centroid = path.centroid(d);
              x = centroid[0];
              y = centroid[1];
              k = 4;
              centered = d;

              // get the id of the state, which == state name, and should match db info!!!
                state_name = state_name_dict[d.id][0];

              // location-name  state_name_dict[d.id][1]
                $('#location-name').text(state_name_dict[d.id][1]);

              //get fuel_mix info, place into list.
                var v0 = fuel_mix[state_name]["gas"],
                    v1 = fuel_mix[state_name]["coal"],
                    v2 = fuel_mix[state_name]["solar"],
                    v3 = fuel_mix[state_name]["wind"],
                    v4 = fuel_mix[state_name]["nuclear"],
                    v5 = fuel_mix[state_name]["hydro"],
                    v6 = fuel_mix[state_name]["other"];
                var data_list = [v0,v1,v2,v3,v4,v5,v6];

              // display the c3 donut, with state-specific data.
                //  empty old
                  $('#fuel-donut').empty();
                //  make new
                  make_donut(data_list);

              // display the d3 sliders, with state-specific data.
                // make visible
                  $('#slider-wrapper').css('visibility','visible');
                // get ride of old sliders & values.
                  $('#slider0').empty();
                  $('#slider1').empty();
                  $('#slider2').empty();
                  $('#slider3').empty();
                  $('#slider4').empty();
                  $('#slider5').empty();
                  $('#slider6').empty();
                // re-make sliders with new values
                  set_slider_values(data_list, state_name);

              // input the scenario results.  Note: this div is hidden, and the variable does not exist, until after the scenario is run!
                  var exists = false;
                  try {
                      eval(scenario_result);
                      exists = true;
                  } catch(e) {
                      exists = false;
                  }
                  if (exists){
                    $('#display-results').attr("class",scenario_result[state_name][0]).text(scenario_result[state_name][1]);
                  }


            } else {
              x = width / (2.5);
              y = height / (2.5);
              k = 1;
              centered = null;
              $('#fuel-donut').empty();
              $('#location-name').empty();
              $('#slider-wrapper').css('visibility','hidden');
              // hide/remove the scenario results.  Note: the variable does not exist, until after the scenario is run!
                  var exists = false;
                  try {
                      eval(scenario_result);
                      exists = true;
                  } catch(e) {
                      exists = false;
                  }
                  if (exists){
                        $('#display-results').attr("class","none").empty();
                  }

            }         // closes if/else for the clicked evt function

            // bind all the clicked paths to the class .active
            g.selectAll("path")
                .classed("active", centered && function(d) { return d === centered; });

            g.transition()
                .duration(750)
                .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
                .style("stroke-width", 1.5 / k + "px");
      }

};

make_topojson_map_usa();

d3.json("static/data/state_val.json", readJson);

function readJson(collection) {
        // Collection represents the Javascript Object Array from the JSOn
        // Each element is an object with name, latitude, longitude, and type properties
        
        // Using Javascript's .Map() as we will process and then discard the collection
        // Data is saved into the global variable myData
        myData = collection.map(function(d,i,thisObject){
                var myItem = {};
                //myItem.name = d.name.replace("#","_");  // Note that "#" is illegal for use in an id, and so is replaced with "_"
                myItem.nodeInfo = d;
                myItem.LatLng = new L.LatLng( + d.latitude, d.longitude);
                return myItem;
        });

        collection = null; // Garbage collection
        placeNodes();	   // Now that myData is prepped, go ahead and place 
        
}



////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
// DONUT CHART /////////////////////////////////////////////////////////////

  var make_donut = function(data0){

    // MAKE THE IDEA OF THE SVG

        var width = 170,
            height = 170,
            outerRadius = Math.min(width, height) * .5 - 10,
            innerRadius = outerRadius * .6;


    // MAKE THE DATA, to feed into the svg
        var n = 7,
            data;


    // MAKE THE STYLE:  color, shape (arc), and divide arc into data sections(pie)
    // note:  arc not added to svg yet!
        var color = d3.scale.category10();
        var arc = d3.svg.arc();
        var pie = d3.layout.pie()
            .sort(null);


    // ADD SVG TO THE BODY
        var svg = d3.select("#fuel-donut").append("svg")
            .attr("width", width)
            .attr("height", height);

    // make the tip tool
      //tip = d3.tip().attr('class', 'd3-tip').html(function(d) {
      //  var label = getKeyByValue(d.data,fuel_mix[state_name]);
      //  return label+": "+d.data+"%";
      //});
      //svg.call(tip);


    // ADD DATA TO EACH ARC
        svg.selectAll(".arc")
            .data(arcs(data0))
          // ADD ARC TO THE SVG
          .enter().append("g")
            .attr("class", "arc")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
            //.on('mouseover', tip.show)
            //.on('mouseout', tip.hide)
          // MAKE THE VISUAL PATH be the color(i) and data(d)
          .append("path")
            .attr("fill", function(d, i) { return color(i); })
            .attr("d", arc);


    // ARCS function
        function arcs(data0) {
          // defines the arc based on pie of data0.
          var arcs0 = pie(data0),
              i = -1,
              arc;
          // set the color of arc0 (for data0)
          while (++i < n) {
            arc = arcs0[i];
            arc.innerRadius = innerRadius;
            arc.outerRadius = outerRadius;
          }
          return arcs0;
        }


  };




////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////
  // SCENARIO RESULT -- EVENT HANDLING /////////////////////////////


function runScenarioUSA(evt){
  evt.preventDefault();
  console.log("runScenario js function");

  $.ajax('scenario-result-usa', {
    type: 'POST',
    data: JSON.stringify(fuel_mix),
    contentType: 'application/json',
    success: function(data, status, result){
      scenario_result = JSON.parse(result.responseText);
      console.log(scenario_result);
      $('#instructions').empty();
      $('#display-results').css('visibility','visible');
      $('#see-results').css('visibility','visible');
      $('#display-results').attr("class",scenario_result[state_name][0]).text(scenario_result[state_name][1]);

    }
  });

}

$('#submit').on("click", runScenarioUSA);




//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////
  // C3 donut ////////////////////////////////////////////////////


  // TODO:  take the interact "mouseover" functionality of the c3 donut below, and add to the d3 element used above.

      // var make_donut = function(){
      //       var chart = c3.generate({
      //         data: {
      //             columns: [
      //                 ['Natural gas', 30],
      //                 ['data2', 120],
      //             ],
      //             type : 'donut',
      //             onclick: function (d, i) { console.log("onclick", d, i); },
      //             onmouseover: function (d, i) { console.log("onmouseover", d, i); },
      //             onmouseout: function (d, i) { console.log("onmouseout", d, i); }
      //         },
      //         donut: {
      //             title: "Fuel Mix in County"
      //         },
      //         bindto: document.getElementById('fuel-donut')
      //       });

      //       setTimeout(function () {
      //           chart.load({
      //               columns: [
      //                   ["setosa", 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.3, 0.2, 0.2, 0.1, 0.2, 0.2, 0.1, 0.1, 0.2, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2, 0.4, 0.2, 0.5, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.6, 0.4, 0.3, 0.2, 0.2, 0.2, 0.2],
      //                   ["versicolor", 1.4, 1.5, 1.5, 1.3, 1.5, 1.3, 1.6, 1.0, 1.3, 1.4, 1.0, 1.5, 1.0, 1.4, 1.3, 1.4, 1.5, 1.0, 1.5, 1.1, 1.8, 1.3, 1.5, 1.2, 1.3, 1.4, 1.4, 1.7, 1.5, 1.0, 1.1, 1.0, 1.2, 1.6, 1.5, 1.6, 1.5, 1.3, 1.3, 1.3, 1.2, 1.4, 1.2, 1.0, 1.3, 1.2, 1.3, 1.3, 1.1, 1.3],
      //                   ["virginica", 2.5, 1.9, 2.1, 1.8, 2.2, 2.1, 1.7, 1.8, 1.8, 2.5, 2.0, 1.9, 2.1, 2.0, 2.4, 2.3, 1.8, 2.2, 2.3, 1.5, 2.3, 2.0, 2.0, 1.8, 2.1, 1.8, 1.8, 1.8, 2.1, 1.6, 1.9, 2.0, 2.2, 1.5, 1.4, 2.3, 2.4, 1.8, 1.8, 2.1, 2.4, 2.3, 1.9, 2.3, 2.5, 2.3, 1.9, 2.0, 2.3, 1.8],
      //               ]
      //           });
      //       }, 1500);

      //       setTimeout(function () {
      //           chart.unload({
      //               ids: 'data1'
      //           });
      //           chart.unload({
      //               ids: 'data2'
      //           });
      //       }, 2500);
      // };

