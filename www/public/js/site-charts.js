var motors_power_chart;
var battery_charge_chart;

window.onload = function ()
{
    motors_power_chart = new CanvasJS.Chart("chartContainer_motor_powers", {
        animationEnabled: true,
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        title:{
            text: "Motors"
        },
        axisY: {
            title: "Usage"
        },
        data: [{        
            type: "column",  
            showInLegend: true, 
            legendMarkerColor: "grey",
            legendText: "% = usage percent",
            dataPoints: [      
                { y: 0, label: "M1" },
                { y: 0,  label: "M2" },
                { y: 0,  label: "M3" },
                { y: 0,  label: "M4" },
            ]
        }]
    });

    motors_power_chart.render();

    battery_charge_chart = new CanvasJS.Chart("chartContainer_battery_charge", {
        animationEnabled: true,
        title: {
            text: "BATTERY CHARGE"
        },
        data: [{
            type: "pie",
            startAngle: 240,
            yValueFormatString: "##0.00\"%\"",
            indexLabel: "{label} {y}",
            dataPoints: [
                {y: 0, label: "Charged"},
                {y: 100, label: "Free"}
            ]
        }]
    });

    battery_charge_chart.render();
}

function SetValueToMotorChart(_dataPoints)
{
    motors_power_chart.options.data[0].dataPoints = _dataPoints; 
	motors_power_chart.render();
}

function SetValueToBatteryChargeChart(_dataPoints)
{
    battery_charge_chart.options.data[0].dataPoints = _dataPoints; 
	battery_charge_chart.render();
}