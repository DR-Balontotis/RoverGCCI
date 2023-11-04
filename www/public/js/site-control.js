

var connection_start_stop_button_elemnt = document.getElementById("connection-start-stop-button");
var connection_status_bar = document.getElementById("connection-status-bar");

var video_card = document.getElementById("camera-field");

function connection_start_stop_button_click()
{
    var button_text = connection_start_stop_button_elemnt.innerHTML;

    if (button_text === "Start")
    {
        StartWebSocket();
    }
    else
    {
        connection_start_stop_button_elemnt.innerHTML = "Start";
        connection_status_bar.classList.remove("opened");
        connection_status_bar.classList.add("closed");

        StopWebSocket()
    }
}

function SetConnectionStatusSuccess()
{
    connection_start_stop_button_elemnt.innerHTML = "Stop";
    connection_status_bar.classList.add("opened");
    connection_status_bar.classList.remove("closed");
}

var camera_start_stop_button_elemnt = document.getElementById("camera-start-stop-button");
var camera_status_bar = document.getElementById("camera-status-bar");

function camera_start_stop_button_click()
{
    var button_text = camera_start_stop_button_elemnt.innerHTML;

    if (button_text === "Start")
    {
        StartCamera();
    }
    else
    {
        StopCamera()
    }
}

function SetCameraStatus(status)
{
    var button_text = camera_start_stop_button_elemnt.innerHTML;
    if ((button_text === "Start") ^ status)
        alert("Camera error!");

    if (status)
    {
        camera_start_stop_button_elemnt.innerHTML = "Stop";
        camera_status_bar.classList.add("opened");
        camera_status_bar.classList.remove("closed");

        video_card.innerHTML = '<img id="videofield" class="video" src="\\video_feed?port=0">';
        
    }
    else
    {
        camera_start_stop_button_elemnt.innerHTML = "Start";
        camera_status_bar.classList.remove("opened");
        camera_status_bar.classList.add("closed");

        video_card.innerHTML = '';
    }
}

function ChangeCameraPort(port_id)
{
    if (!GetWebSocketStatus())
    {
        alert("You must firstly connect to server!");
    }

    var videofield = document.getElementById("videofield");
    var port_status = document.getElementById("camera-current-port");
    
    if (videofield)
    {
        videofield.setAttribute("src", `\\video_feed?port=${port_id}`);
        port_status.innerHTML = "Port: " + (port_id+1);
    }
}