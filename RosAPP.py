import RoverGCCI

import video
import random
import subprocess

SERVER_URL = "localhost"
# SERVER_URL = "192.168.88.128"
SERVER_PORT = 8888
SERVER_DIR = "www"

server = None
cam = None

def GetCamFrame(cam_id):
    return cam.get_frame(cam_id)

def GetSystmeData():
    return {
            "motors" :
            {
                "motor_power_1" : random.randint(0, 100),
                "motor_power_2" : random.randint(0, 100),
                "motor_power_3" : random.randint(0, 100),
                "motor_power_4" : random.randint(0, 100),
            },

            "battary" :
            {
                "charge_percent": random.randint(0, 100),
                "charge_voltage": random.randint(0, 100),
            },
        }

def TerminalHandler(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("Command executed successfully. Output:")
            return(result.stdout)
        else:
            print("Command failed. Error output:")
            print(result.stderr)
            return(result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")
    

if __name__ == "__main__":
    print("Camera is opening, now ...")

    # creates camera
    cam = video.UsbCamera()

    server = RoverGCCI.GCCI()
    server.ServerStart(SERVER_URL, SERVER_PORT, SERVER_DIR, GetCamFrame, GetSystmeData, TerminalHandler)
    
    print("server started")

    while True:
        input("Exit")