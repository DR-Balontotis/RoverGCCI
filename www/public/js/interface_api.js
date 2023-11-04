
// our websocket constant
let ws;
let ws_status;

// html objects from index.html file via elemnt id
var terminal_input  = document.getElementById("terminal-promt-input");
// var terminal_result = document.getElementById("terminal-promt-result");

function GetWebSocketStatus()
{
    return ws_status;
}

function StartWebSocket()
{
    // ws = new WebSocket("ws://localhost:8888/websocket");
    // ws = new WebSocket("ws://192.168.88.128:8888/websocket");
    ws = new WebSocket(`ws://${SERVER_URL}:${SERVER_PORT}/websocket`);

    ws_status = 1;

    // log a message when websocket is started
    ws.onopen = function() {
        console.log("WebSocket is opened");
    };

    // execute these statement when catching a message
    ws.onmessage = function (evt) {
        resp_data = JSON.parse(evt.data)

        // invalid request response from server
        if (resp_data["RetType"] == -1)
        {
            console.log("The request was invalid");
        }
        // terminal result
        else if (resp_data["RetType"] == 0)
        {
            // terminal_result.innerHTML += (resp_data["terminal_result"] + "\n");
            terminalWrite(resp_data["terminal_result"] + "\n");
            TerminalWrite_cursor();
        }
       // rover system status data
        else if (resp_data["RetType"] == 1)
        {
            motors = resp_data["data_packet"]["motors"];
            battary = resp_data["data_packet"]["battary"];
            
            SetValueToMotorChart ([
                { y: motors["motor_power_1"], label: "M1" },
                { y: motors["motor_power_2"],  label: "M2" },
                { y: motors["motor_power_3"],  label: "M3" },
                { y: motors["motor_power_4"],  label: "M4" },
            ]);

            SetValueToBatteryChargeChart([
                {y: battary["charge_percent"], label: "Charged"},
                {y: (100-battary["charge_percent"]), label: "Free"},
            ]);
        }
        // camera open/close
        else if (resp_data["RetType"] == 2)
        {
            SetCameraStatus(resp_data["camera_status"]);
        }
        // Conneciton is successful
        else if (resp_data["RetType"] == 3)
        {
            SetConnectionStatusSuccess();
        }
        // rover main response
        else if (resp_data["RetType"] == 4)
        {
            alert(resp_data["main_data_message"]);
        }
        // unknown type
        else
        {
            console.log("An unknown response is catched: " + resp_data["RetType"]);
        }
    };
}

function StopWebSocket()
{
    ws_status = 0;
    ws.close();
}

function StartCamera()
{
    if (!ws_status)
    {
        alert("You must firstly start connection!");
        return;
    }

    var data_value = {
        "api_id" : 2,
        "camera_status" : 1,
    };

    ws.send(JSON.stringify(data_value));
}

function StopCamera()
{
    if (!ws_status)
    {
        alert("You must firstly start connection!");
        return;
    }

    var data_value = {
        "api_id" : 2,
        "camera_status" : 0,
    };

    ws.send(JSON.stringify(data_value));
}

// send a new request for terminal command
// this function is called in second way (now)
// 1- in html file, send button
// 2- the next functino listen the enter key, if the enter key is pressed,
// this function is called
function sendTerminalPromt()
{
    if (!ws_status)
    {
        alert("You must firstly start connection!");
        return;
    }

    var data_value = {
        "api_id" : 0,
        "terminal_promt" : terminal_input.value,
    };

    ws.send(JSON.stringify(data_value));

    terminalWrite(terminal_input.value + "\n");

    // clear input box
    terminal_input.value = "";
}

// Execute a function when the user presses a key on the keyboard
terminal_input.addEventListener("keypress", function(event)
{
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter")
    {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        sendTerminalPromt();
    }
});

