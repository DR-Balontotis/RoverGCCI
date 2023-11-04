import json
import time
import threading

class API_Controller(object):
    def __init__(self, _id, _GetSystemData_Func, _TerminalHandler):
        self.visual_data_timer = 1000
        self.visualData_thread = None
        
        self.id = _id
        self.websocket = None
        self.camera_status = 0

        self.GetSystemData_Func = _GetSystemData_Func
        self.TerminalHandler_Func = _TerminalHandler

    def SetWebSocket(self, _websocket):
        self.websocket = _websocket

    def WebSocketStatus(self):
        return (self.websocket != None)

    def SendData(self, data):
        dataJSON = json.dumps(data)
        self.websocket.write_message(dataJSON)

    def api_controller_catch_command(self, request):
        # decode json message
        req_data = json.loads(request)
        
        response = {"RetType" : -1}

        try:
            id = int(req_data["api_id"])

            if id == 0:
                response = {"RetType" : 0, "terminal_result" : self.TerminalHandler_Func(req_data["terminal_promt"])}
            elif id == 2:
                self.camera_status = req_data["camera_status"]
                response = {"RetType" : 2, "camera_status" : self.camera_status}
        except:
            print("APICONTROLLER: api_id type error:", req_data["api_id"])

        # encode the repsonse to send to client
        responseJSON = json.dumps(response)
        self.websocket.write_message(responseJSON)

    def visual_data_status(self):
        return (self.visualData_thread != None)
    
    def visual_data_start(self):
        self.visualData_thread = threading.Thread(target=self.visual_data_send)
        self.visualData_thread.start()

    def visual_data_stop(self):
        if self.visual_data_status():
            self.visualData_thread = None

    def visual_data_send(self):
        while self.visualData_thread:
            response = {"RetType" : 1, "data_packet" : self.GetSystemData_Func()}
            responseJSON = json.dumps(response)
            self.websocket.write_message(responseJSON)

            time.sleep(self.visual_data_timer / 1000) # visual_data_timer is ms, so it is converted to seconds

    def send_connection_started_message(self):
        response = {"RetType" : 3}
        responseJSON = json.dumps(response)
        self.websocket.write_message(responseJSON)
