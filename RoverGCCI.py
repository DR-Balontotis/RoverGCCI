import os
import time
import asyncio
import tornado
import threading
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
import tornado.process
import tornado.template
import gen

import api_controller

server_thread = None

server_url = "localhost"
server_port = 8888
server_dir = "www"

GetCamFrame = None
GetSystemData = None
TerminalHandler = None
apiController = {}
lastUserID = 1

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_cookie("client")

class BaseHandlerSocket(tornado.websocket.WebSocketHandler):
    def get_current_user(self):
        return self.get_cookie("client")

class MainHandler(BaseHandler):
    def get(self):
        global lastUserID
        if not self.current_user:
            self.set_cookie("client", str(lastUserID))
            apiController[lastUserID] = api_controller.API_Controller(lastUserID, GetSystemData, TerminalHandler)
            print(apiController)
            lastUserID += 1
        else:
            UserID = int(tornado.escape.xhtml_escape(self.current_user))
            if apiController.get(UserID) == None:
                apiController[UserID] = api_controller.API_Controller(UserID, GetSystemData, TerminalHandler)

        self.render("index.html", SERVER_URL=f"{server_url}", SERVER_PORT=f"{server_port}")

class EchoWebSocket(BaseHandlerSocket):
    def open(self):
        UserID = int(tornado.escape.xhtml_escape(self.current_user))
        
        apiController[UserID].SetWebSocket(self)
        apiController[UserID].send_connection_started_message()
        apiController[UserID].visual_data_start()
        print("WebSocket opened")

    def on_message(self, message):
        UserID = int(tornado.escape.xhtml_escape(self.current_user))
        apiController[UserID].api_controller_catch_command(str(message))

    def on_close(self):
        UserID = int(tornado.escape.xhtml_escape(self.current_user))
        apiController[UserID].visual_data_stop()
        apiController[UserID].camera_status = False
        #apiController.pop(UserID)
        print("WebSocket closed")

class StreamHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        UserID = int(tornado.escape.xhtml_escape(self.current_user))

        ioloop = tornado.ioloop.IOLoop.current()

        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header( 'Pragma', 'no-cache')
        self.set_header( 'Content-Type', 'multipart/x-mixed-replace;boundary=--jpgboundary')
        self.set_header('Connection', 'close')

        self.served_image_timestamp = time.time()
        my_boundary = "--jpgboundary"
        
        try:
            while apiController[UserID].camera_status:
                # Generating images for mjpeg stream and wraps them into http resp
                camera_port_id = self.get_argument('port')

                img = GetCamFrame(camera_port_id)

                interval = 0.1
                if self.served_image_timestamp + interval < time.time():
                    self.write(my_boundary)
                    self.write("Content-type: image/jpeg\r\n")
                    self.write("Content-length: %s\r\n\r\n" % len(img))
                    self.write(img)
                    self.served_image_timestamp = time.time()
                    yield tornado.gen.Task(self.flush)
                else:
                    yield tornado.gen.Task(ioloop.add_timeout, ioloop.time() + interval)
        except Exception as e:
            print("Camera stream error:", e)

class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        
class GCCI():
    def ServerStart(self, _server_url : str, _server_port : str, _server_dir : str, _GetCamFrame, _GetSystemData, _TerminalHandler):
        global server_url, server_port, server_dir, server_thread, GetCamFrame, GetSystemData, TerminalHandler
        
        server_url = _server_url
        server_port = _server_port
        server_dir = _server_dir
        
        GetCamFrame = _GetCamFrame
        GetSystemData = _GetSystemData
        TerminalHandler = _TerminalHandler
        
        self.main_start()
    
    def GetClientCount(self):
        ret = 0
        for client in apiController.values():
            if client.WebSocketStatus():
                ret += 1
        return ret
    
    def SendDataAllClient(self, data):
        for client in apiController.values():
            client.SendData(data)
        return self.GetClientCount()

    def main_start(self):
        global server_url, server_port, server_dir

        self.event_loop = None
        
        tornado.locale.load_translations(server_dir)
        app = self.make_app()

        asyncio.set_event_loop(asyncio.new_event_loop())
        self.event_loop = tornado.ioloop.IOLoop()

        app.listen(server_port)

        threading.Thread(target = self.event_loop.start, daemon = True).start()

        self.lock = threading.Lock()
        
        print("Site dir:", server_dir)
        print(f'Listening on http://{server_url}:{server_port} (click on me)')

    def make_app(self):
        global server_url, server_port, server_dir

        tornado_settings = {
                'debug': True,
                'static_path': os.path.join(os.path.dirname(os.path.realpath(__file__)), server_dir)
            }

        tornado_handlers = [
                (r"/", MainHandler),
                (r"/websocket", EchoWebSocket),
                (r'/video_feed', StreamHandler),
                (r"/(.*)", NoCacheStaticFileHandler, {
                    "path": tornado_settings.get("static_path"),
                    "default_filename": "index.html"
                }),
        ]
        
        return tornado.web.Application(tornado_handlers, template_path=server_dir, cookie_secret="RoVeR")



