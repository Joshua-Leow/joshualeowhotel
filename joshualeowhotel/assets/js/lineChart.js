function drawXYChart(roomType, xyChartData) {
  const config = {
    type: "line",
    data: {datasets: []},
    options: {
      scales: {
        x: {
          type: "time",
          offset: true,
          time: {
            parser: "MMM yyyy",
            unit: "month",
            displayFormats: {
              minute: "MMM yyyy"
            }
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  };

  var myChart = new Chart(document.getElementById("myChart"), config);

  for (var i = 0; i < roomType.length; i++) {
    var newDataSet = {
      label: roomType[i],
      data: xyChartData[i],
      fill: false,
      borderColor: '#'+(0x1100000+Math.random()*0xffffff).toString(16).substr(1,6),
      backgroundColor: 'rgba(249, 238, 236, 0.74)',            
      tension: 0    
    }; //end of newDataSet

    if (roomType[i] === 'deluxe') {
      newDataSet.borderColor = 'rgba(50, 205, 50, 0.74)'; // lime green
    } else if (roomType[i] === 'standard') {
      newDataSet.borderColor = 'rgba(128, 0, 128, 0.74)'; // purple
    }

    myChart.data.datasets.push(newDataSet);

  } //end of for loop

  myChart.update();

}

$.ajax({
  url:"/linechart",
  type:"POST",
  contentType: 'application/json;charset=UTF-8',
  data: {testdata:1},
  error: function() {
      alert("Error");
  },
  success: function(data, status, xhr) {
    // xyData is a dictionary (key:value pairs)
    // {
    //   "deluxe":[{bookingMonth1: numOfBookings1},{bookingMonth2: numOfBookings2},{bookingMonth3: umOfBookings3}],
    //   "standard":[{bookingMonth1: numOfBookings1},{bookingMonth2: numOfBookings2},...]
    // }

    var roomType = [];
    var xyChartData = [];

    for (const[key, values] of Object.entries(data.xyData)) {
      roomType.push(key);
      //convert xyData to xyChartData format
      var xy = values.map(function(item) {
        var key = Object.keys(item)[0];
        var value = item[key];
        return {x: key, y: value};
      });
      xyChartData.push(xy)
    }

    drawXYChart(roomType, xyChartData);
  }
})