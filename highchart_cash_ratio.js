let period = 1000; //1sec

document.addEventListener('DOMContentLoaded',() =>{
Highcharts.chart("container", {
  chart: {
    type: "spline",
    backgroundColor:"#fceee4"
  },

  title: {
    text: "Averages of Cash Ratio across various Sectors"
  },


  xAxis: {
    crosshair: {
      width: 2
    },
     tickInterval: 1
  },

  yAxis: {
    title: {
      text: "Cash Ratio"
    }
  },

  plotOptions: {
    series: {
      color: "#ABB2B9",
      marker: {
        enabled: false
      },
      label: {
        connectorAllowed: false
      },
      animation:{
        duration:1200
      }
    }
  },

  data: {
    csv: document.getElementById("csv").innerHTML
  },

  tooltip: {
    shared: true,
    valueSuffix: ""
  },


  series: [
    { color: "#4608F0",
      animation: {
        defer: period*0
      }
    },
    { color: "#FF0000",
      animation: {
        defer: period
      }
    },
    { color: "#FFD700",
      animation: {
        defer: period * 2
      }
    },
    { color: "#FA8072",
      animation: {
        defer: period * 3
      }
    },
    {
      color: "#000000",
      animation: {
        defer: period * 4
      }
    },
    {
      color: "#0000FF",
      animation: {
        defer: period * 5
      }
    },
      { color: "#8B008B",
      animation: {
        defer: period*6
      }
    },
    { color: "#7FFF00",
      animation: {
        defer: period*7
      }
    },
    { color: "#228B22",
      animation: {
        defer: period * 8
      }
    },
    { color: "#1E90FF",
      animation: {
        defer: period * 9
      }
    },
    {
      color: "#FF69B4",
      animation: {
        defer: period * 10
      }
    }
    ]

  })
});