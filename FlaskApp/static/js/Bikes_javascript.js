/*jslint browser: true*/
/*global $,jQuery,google,charts,console,x*/

//all functional code for our application is in this javascript file, accessed via link in index.html file

function initMap() {
	
		//use Google's map API to generate the map
        var map = new google.maps.Map(document.getElementById('map-container'),
        		{zoom: 14, center: 
        		{lat: 53.3498, lng: -6.2603}
        }); 
        
        //declare all the Javascript variables at top of the function for cleaner code - easy as no 
        //values need to be initialised with Javascript
        
        var markers,infoWindows,infoWindow,marker, contentString,output,bikes,station_number,
        list,temp,icon,icon_show,stations;
                         
     $.getJSON("http://localhost:5000/stations", null, function (stations)
                         {
            stations = stations.stations;
            for (j=0; j<stations.length; j++) {
                createMarker(j);
            }
            
            //create markers to show the bike stations around Dublin city
             function createMarker(j) {
            	var station = stations[j],
            	station_number = station.number;
            	var marker = new google.maps.Marker({ 
            		position: {
		                lat: station.lat,
		                lng: station.lon
		            },
		            map: map,
		            title: station.name,
		            station_number: station.number,
		      
            	});
            	
            		//the weather data is displayed in JSON dict format at this http location from open weather map
            	  var URL = "http://api.openweathermap.org/data/2.5/forecast?id=7778677&units=metric&APPID=c219176876dbea25f50034f610fd0128"
                      
                  	$.getJSON(URL, null, function (obj) {
                      
                  		//pull weather info from JSON object returned by the API to the http page above
                  	  var list = obj.list;
                      var output = "<table>";
                      for (var i=0; i<1; i++)
                           { var date = new Date((list[i].dt) * 1000),
                              temp = list[i].main.temp,
                              icon = list[i].weather[0].icon,
                              icon_show = ("<img src='http://openweathermap.org/img/w/" + icon + ".png'>"),
                              output = "<tr><td>" +date.toDateString()+icon_show+temp +"°C"+"</td></tr>";
                      			output +="</table>";
                              };
                
            		var bikes = station.available_bikes;
            		var stands =station.available_bike_stands;
            		google.maps.event.addListener(marker, 'click', (function (marker, j) 
            		{return function (){
            			contentString = station.name+" has " +bikes+" bikes and "+stands+" free bike stands available now "+output;
            	        infoWindow = new google.maps.InfoWindow({content: contentString
            	            			});


		            	infoWindow.open(map, marker);}
               		})
               		(marker, j))   
                  	});           	  
                        
	             //closes the for loop on the stations 
            
          };
 		//closes the function to find the stations JSON input
 
})  
         var heatmap = $.getJSON("http://localhost:5000/stations", null,function(stations) {
             //generate the table of locations (same as stations) for the heatmap
        	 var heatmapData = [];
             var stations = stations.stations;
             for (var i = 0; i<stations.length; i++) {
            	 var latLng = new google.maps.LatLng(stations[i].lat, stations[i].lon),
            	
            	 //display zero bikes as redder, over 6 as greener, orange between them
            	 weight;      
            	 	var magnitude = parseInt(stations[i].available_bikes);
				         switch(magnitude){
					         case magnitude=0:
						         weight=100;
						         break;
					         case magnitude>=6:
						         weight=0;
						         break;
					         default:
						         weight=50;
						         }
				         
		      var weightedLoc = {
	    		  location: latLng,
	    		  weight: weight
	      			};
                 
		      heatmapData.push(weightedLoc);
             }
             
             //use the API to generate the heatmap
            var heatmap = new google.maps.visualization.HeatmapLayer({
              		data: heatmapData,
              		map: map 
          			});
            
            heatmap.set('radius', 40);
            heatmap.setMap(map);
                                
                                });
            

     google.charts.load("current", {packages:["corechart"]});
     google.charts.setOnLoadCallback(drawChart); 
     
     function drawChart (){
    	 //peak_times_chart
    	 	var forChart = $.getJSON("http://localhost:5000/peak", null,function (peak) {
    	 	var peak = peak.peak;
    	    for (var p=0; p<1; p++)
            { var no_bikes = peak[p].peak_bikes_available,
    	 		no_stands = peak[p].peak_bike_stands;}
    	 	
    	 	var table = new google.visualization.arrayToDataTable([
            			["Available", "Number"],
            			["bikes", no_bikes],
            			["stands",no_stands]
            			]);
            	
		    console.log('tabledata', table);
		    
		    //use the API to create the chart
		    var chart = new google.visualization.PieChart(document.getElementById('peak_chart'));
		    chart.draw(table, {width: 400, height: 340, title: 'Peak Bike and Stand Availability'});
		    console.log('chart', chart);
    	 	});
    	 	}
   
     	//off_peak_times_chart
 	 	var forChart2 = $.getJSON("http://localhost:5000/off_peak", null,function (off_peak) {
 	 	var off_peak = off_peak.off_peak;
 	    for (var o=0; o<1; o++)
         { var no_bikes_o = off_peak[o].off_peak_bikes_available,
 	 		no_stands_o = off_peak[o].off_peak_bike_stands;}
 	 	
 	 	var table2 = new google.visualization.arrayToDataTable([
         			["Available", "Number"],
         			["bikes", no_bikes_o],
         			["stands",no_stands_o]
         			]);
         
		    
		    //use the API to create the chart for off-peak
		    var chart2 = new google.visualization.PieChart(document.getElementById('off_peak_chart'));
		    chart2.draw(table2, {width: 400, height: 340, title: 'Off-Peak Bike and Stand Availability'});
		    console.log('chart', chart2);
 	 	});
 	 	

 	 //closes the map init function
}
     
//references Google Developers https://developers.google.com, https://openweathermap.org, 
//W3 schools, and lecture notes from comp30670(software engineering) and comp30680(web design)

