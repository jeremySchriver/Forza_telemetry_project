import socket
from struct import unpack
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType
import math
import data_packet
import tachCalculator
import led_conditions
from datetime import datetime
import csv

#Creates file for logging telemtry data
file1 = open("E:\Code Projects\Case Lights\Forza M7\logTelemetry.txt", "a")  # append mode

#Sets UDP information for Forza Motorsport connection
UDP_IP = "127.0.0.1"
UDP_PORT = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

#Initializes DataPacket module for parsing data from FM7
dp = data_packet.DataPacket(version="dash_fm8")

def createHeaderCSV():
    data = ["Timestamp", "CarOrdinalID", "CarClass", "CarPerformanceIndex", "DriveTrainType", "NumCylinders", "EngineMaxRPM", "EndingeIdelRPM", "EngineCurrentRPM", "Speed", "Power", "Torque", "Boost", "Gear", "Accel", "Brake", "Clutch", "HandBrake", "Fuel"]
    
    # Writing to the CSV file
    with open("E:\Code Projects\Case Lights\Forza M7\logTelemetry.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(data)

        file.close

createHeaderCSV()

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    dp.parse(data, recording = False)
    
    if dp.active==1:
        #Writes data to txt file
        '''file1.write("timestamp= " + str(datetime.now()) + 
                    ", CarOrdinalID = " + str(dp.car_ordinal_id) + 
                    ", CarClass= " + str(dp.car_class_id) + 
                    ", CarPerformanceIndex= " + str(dp.car_performance_index) + 
                    ", DriveTrainType= " + str(dp.car_drivetrain_id) + 
                    ", NumCylinders= " + str(dp.car_num_cylinders) + 
                    ", engine_max_rpm= " + str(dp.engine_max_rpm) + 
                    ", engine_idle_rpm= " + str(dp.engine_idle_rpm) + 
                    ", engine_current_rpm= " + str(dp.engine_current_rpm) + 
                    ", Speed= " + str(dp.speed) + 
                    ", Power= " + str(dp.power) + 
                    ", Torque= " + str(dp.torque) + 
                    ", Boost= " + str(dp.boost) + 
                    ", Gear= " + str(dp.gear_num) + 
                    ", Accel= " + str(dp.throttle) + 
                    ", Brake= " + str(dp.brake) + 
                    ", Clutch= " + str(dp.clutch) + 
                    ", HandBrake= " + str(dp.handbrake) + 
                    ", Fuel= " + str(dp.fuel) + 
                    "\n")'''
        
        data = [str(datetime.now()), str(dp.car_ordinal_id), str(dp.car_class_id), str(dp.car_performance_index), str(dp.car_drivetrain_id), str(dp.car_num_cylinders), str(dp.engine_max_rpm), str(dp.engine_idle_rpm), str(dp.engine_current_rpm), str(dp.speed), str(dp.power), str(dp.torque), str(dp.boost), str(dp.gear_num), str(dp.throttle), str(dp.brake), str(dp.clutch), str(dp.handbrake), str(dp.fuel)]

        #Writes data to csv file
        with open("E:\Code Projects\Case Lights\Forza M7\logTelemetry.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write the data to the next available row
            writer.writerow(data)

            file.close
else:
    print("Loop Ended")