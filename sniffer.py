import socket
from struct import unpack
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType
import math
import data_packet
import tachCalculator
import led_conditions
from datetime import datetime

#Creates file for logging condition data against current RPM
#file1 = open("E:\Code Projects\Case Lights\Forza M7\conditionLog.txt", "a")  # append mode

#Creates file for logging UDP data from forza
#file2 = open("E:\Code Projects\Case Lights\Forza M7\udpLog.txt", "a")  # append mode

#Sets UDP information for Forza Motorsport connection
UDP_IP = "127.0.0.1"
UDP_PORT = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

#Initializes DataPacket module for parsing data from FM7
dp = data_packet.DataPacket(version="dash_fm8")

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    dp.parse(data, recording = False)
    engineMaxRPM = dp.engine_max_rpm
    engineIdleRpm = dp.engine_idle_rpm
    #overRevBotRange = self.EngineMaxRpm - (self.EngineMaxRpm*.1)
    #optimalShiftBotRange = self.EngineMaxRpm - ((self.EngineMaxRpm*.11))
    #optimalShiftTopRange = self.EngineMaxRpm - (self.EngineMaxRpm*.1)
    if dp.active==1:
        #Writes required UDP data to file
        #file2.write('active= ' + str(dp.active) + ', timestamp= ' + str(datetime.now()) + ', engine_max_rpm= ' + str(dp.engine_max_rpm) + ', engine_idle_rpm= ' + str(dp.engine_idle_rpm) + ', engine_current_rpm= ' + str(dp.engine_current_rpm) + "\n")

        #Runs data through calculator to gather the condition
        stats = tachCalculator.TachCalc(math.floor(dp.engine_current_rpm), math.ceil(dp.engine_idle_rpm), math.ceil(dp.engine_max_rpm))
        
        #Sets lighting sequence based on provided condition
        led_conditions.conditionChecker.conditionSet(stats.condition)

        #Writes condition data to file after calculation and light change
        #file1.write('timestamp: ' + str(datetime.now()) + ', Condition: ' + str(stats.condition) + ', CurrentRPM: ' + str(stats.CurrentEngineRpm) +', IdleRPM: ' + str(stats.EngineIdleRpm) + ", MaxRPM: " + str(stats.EngineMaxRpm) + "\n")
    else:
        led_conditions.conditionChecker.conditionSet("engineOff")
else:
    file1.close()
    file2.close()
    print("Loop Ended")