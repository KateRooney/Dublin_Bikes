/*jslint browser: true*/
/*global $,jQuery,google,console,x*/

function initMap() {
        var map = new google.maps.Map(document.getElementById('map-container'),
        		{zoom: 14, center: 
        		{lat: 53.3498, lng: -6.2603}
        }); 
        var markers,infoWindows,infoWindow,marker, contentString,output,bikes,station_number,
        list,temp,icon,icon_show,off_peak;
                         
     $.getJSON("http://localhost:5000/off_peak", null, function (off_peak)
                         {
            off_peak = off_peak.off_peak;
            console.log('finding off_peak', off_peak);
            for (j=0; j<off_peak.length; j++) {
                createMarker(j);
            }
            
             function createMarker(j) {
            	var station = off_peak[j],
            	station_number = station.number;
            	console.log('off_peak',off_peak);
            	var marker = new google.maps.Marker({ 
            		position: {
		                lat: station.lat,
		                lng: station.lon
		            },
		            map: map,
		            title: station.name,
		            station_number: station.number,
		      
            	});
            		
            	  var URL = "http://api.openweathermap.org/data/2.5/forecast?id=7778677&units=metric&APPID=7dc97eec8449218feec4838d26264d0b"
                      
                  	$.getJSON(URL, null, function (obj) {
                      var list = obj.list;
                      console.log('list',list);
                      var output = "<table>";
                      for (var i=0; i<1; i++)
                           { var date = new Date((list[i].dt) * 1000),
                              temp = list[i].main.temp,
                              icon = list[i].weather[0].icon,
                              icon_show = ("<img src='http://openweathermap.org/img/w/" + icon + ".png'>"),
                              output = "<tr><td>" +date.toDateString()+icon_show+temp +"°C"+"</td></tr>";
                      			output +="</table>";
                              console.log('weather', output);
                              };
                
            		var bikes = station.off_peak_bikes_available;
            		var stands =station.off_peak_bike_stands;
            		google.maps.event.addListener(marker, 'click', (function (marker, j) 
            		{return function (){
            			contentString = station.name+" has " +bikes+" bikes and "+stands+" free bike stands available on average during off_peak hours "+output;
            	        infoWindow = new google.maps.InfoWindow({content: contentString
            	            			});

                        console.log('content string', contentString);
                        console.log('infowindow', infoWindow);
		            	infoWindow.open(map, marker);}
               		})
               		(marker, j))   
                  	});           	  
                        
	             //closes the for loop on the off_peak 
            
          };
 		//closes the function to find the off_peak JSON input
 
})  
         var heatmap = $.getJSON("http://localhost:5000/off_peak", null,function(off_peak) {
             var heatmapData = [];
             var off_peak = off_peak.off_peak;
             for (var i = 0; i<off_peak.length; i++) {
            	 var latLng = new google.maps.LatLng(off_peak[i].lat, off_peak[i].lon),
            	 weight;      
            	 	var magnitude = parseInt(off_peak[i].off_peak_bikes_available);
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
             console.log(heatmapData);
            var heatmap = new google.maps.visualization.HeatmapLayer({
              		data: heatmapData,
              		map: map 
          			});
            
            heatmap.set('radius', 40);
            heatmap.setMap(map);
                                
                                });
            
//closes the map init function

}