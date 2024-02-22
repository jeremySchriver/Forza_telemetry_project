import socket
from struct import unpack
#import data_packet
from datetime import datetime
import csv
import os
from Core.data_packet import DataPacket
import json

'''Class is meant to be used as the main telemetry capture method. It is required to have launched the game before starting this script or it may error out. Once the game is launched and default variables within the script have been updated (if required) you can launch this script. Current version has no built in kill switch other than keyboard interrupt within the terminal.'''

#Method to handle creation of the CSV file and fill the header with the supplied values
def createHeaderCSV(fileName):
    '''Sled values currently not in scope that could be added back
        'active', 'acceleration', 'velocity', 'angular_velocity', 'yaw', 'pitch', 'roll','suspension_travel_ratio','wheel_slip_ratio','wheel_rotation_speed','wheel_on_rumble_strip','wheel_puddle_depth','surface_rumble','wheel_slip_angle','wheel_combined_slip','suspension_travel',
    Dash values currently not in scope that could be added back
       'position''tire_temp''dist_traveled','lap_time_best', 'lap_time_last', 'lap_time_current','race_time', 'lap_num', 'race_position','steering_angle','driving_line', 'ai_brake_diff''tire_wear_front_left', 'tire_wear_front_right','tire_wear_rear_left', 'tire_wear_rear_right','track_ordinal_id' '''
    
    #Defines values to be placed in the header
    headerData = ["Timestamp", "CarOrdinalID", "CarClass", "CarPerformanceIndex", "DriveTrainType", "NumCylinders", "EngineMaxRPM", "EngineIdleRPM", "EngineCurrentRPM", "Speed", "Power", "Torque", "Boost", "Gear", "Accel", "Brake", "Clutch", "HandBrake", "Fuel"]
    
    #Writing to the CSV file
    if not os.path.exists(fileName):
        with open(fileName, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            #Write the header
            writer.writerow(headerData)

            file.close
        print(f"CSV file '{fileName}' created successfully.")
    else:
        print(f"CSV file '{fileName}' already exists.")


#Sets the path and file name for the logging file to be used
fileName = os.getcwd() + "\\TelemDataFiles\\logTelemetry.csv"

file_path = os.path.join(os.getcwd(), "Core", "preferences.json")

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            
            #Sets game version information
            gameVersion = data["GameVersion"]

            #Sets UDP information for Forza Motorsport connection
            UDP_IP = data["Forza_UDP_IP"]
            UDP_PORT = data["Forza_UDP_PORT"]
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((UDP_IP, UDP_PORT))

            #Initializes DataPacket module for parsing data from FM7
            dp = DataPacket(version=gameVersion)

            #Runs the method to create the file with headers, if file is missing
            createHeaderCSV(fileName)

            #Main loop that continues to run until script is terminated. Once UI is built while check will be changed to match a boolean there.
            while True:
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                
                #Parses the recieved data packet using the data_packet class
                dp.parse(data, recording = False) #Terminal output for "Packet Parsed" comes from this method
                
                if dp.active==1:
                    #Sets values captured from the data packed into an array        
                    data = [str(datetime.now()), str(dp.car_ordinal_id), str(dp.car_class_id), str(dp.car_performance_index), str(dp.car_drivetrain_id), str(dp.car_num_cylinders), str(dp.engine_max_rpm), str(dp.engine_idle_rpm), str(dp.engine_current_rpm), str(dp.speed), str(dp.power), str(dp.torque), str(dp.boost), str(dp.gear_num), str(dp.throttle), str(dp.brake), str(dp.clutch), str(dp.handbrake), str(dp.fuel)]

                    #Writes data to csv file
                    with open(fileName, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        
                        #Write the data to the next available row
                        writer.writerow(data)

                        file.close
            else:
                print("Loop Ended")

        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
else:
    print("File not found:", file_path)