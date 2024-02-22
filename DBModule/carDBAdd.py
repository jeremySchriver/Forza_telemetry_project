import csv
import os
from pathlib import Path
from datetime import datetime

#Creates blank table containing header
def createHeaderCSV():
    data = [
    ["CarOrdinalID", "CarFriendlyName", "CarMake", "CarModel", "CarManYear", "CarClass", "CarPerformanceIndex", "DriveTrainType", "NumCylinders", "CylinderNumber", "EngineMaxRPM", "EndingeIdelRPM", "Gears", "FinalDriveRatio", "Ratio1", "Ratio2", "Ratio3", "Ratio4", "Ratio5", "Ratio6", "Ratio7", "Ratio8", "Ratio9", "Ratio10", "LastModified"],
    ]
    
    # Writing to the CSV file
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(data[0])

        file.close

#CSV writer function to append entry to the table
def addEntry(CarOrdinalID, CarFriendlyName, CarMake, CarModel, CarManYear, CarClass, CarPerformanceIndex, DriveTrainType, NumCylinders, EngineMaxRPM, EngineIdleRPM, Gears, FinalDriveRatio, Ratio1, Ratio2, Ratio3, Ratio4, Ratio5, Ratio6, Ratio7, Ratio8, Ratio9, Ratio10):
    data = [
        CarOrdinalID,
        CarFriendlyName,
        CarMake,
        CarModel,
        CarManYear,
        CarClass,
        CarPerformanceIndex,
        DriveTrainType,
        NumCylinders,
        EngineMaxRPM,
        EngineIdleRPM,
        Gears,
        FinalDriveRatio,
        Ratio1,
        Ratio2,
        Ratio3,
        Ratio4,
        Ratio5,
        Ratio6,
        Ratio7,
        Ratio8,
        Ratio9,
        Ratio10,
        str(datetime.now())
    ]

    # Writing to the CSV file
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the data to the next available row
        writer.writerow(data)

        file.close

#CSV writer function to append entry to the table
def overwriteEntry(Row, CarOrdinalID, CarFriendlyName, CarMake, CarModel, CarManYear, CarClass, CarPerformanceIndex, DriveTrainType, NumCylinders, EngineMaxRPM, EngineIdleRPM, Gears, FinalDriveRatio, Ratio1, Ratio2, Ratio3, Ratio4, Ratio5, Ratio6, Ratio7, Ratio8, Ratio9, Ratio10):
    data = [
        CarOrdinalID,
        CarFriendlyName,
        CarMake,
        CarModel,
        CarManYear,
        CarClass,
        CarPerformanceIndex,
        DriveTrainType,
        NumCylinders,
        EngineMaxRPM,
        EngineIdleRPM,
        Gears,
        FinalDriveRatio,
        Ratio1,
        Ratio2,
        Ratio3,
        Ratio4,
        Ratio5,
        Ratio6,
        Ratio7,
        Ratio8,
        Ratio9,
        Ratio10,
        str(datetime.now())
    ]

    with open(file_name, mode='r') as file:
        # Read the existing CSV data
        csv_data = list(csv.reader(file))
        file.close

    csv_data[Row-1] = data

    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)
        file.close

#Searches CSV file for oridinalID
def search_csv(file_name, search_term):
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        
        # Assuming the first row contains headers
        headers = next(reader)
        
        # Assuming you want to search in a specific column, change the index accordingly
        search_column_index = headers.index('CarOrdinalID')
        
        for row in reader:
            if row[search_column_index] == search_term:
                return reader.line_num
        
    return None

#method to grab the timestamp from a certain row
def get_value_from_csv(file_name, target_row):
    target_column = "LastModified"
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        
        # Assuming the first row contains headers
        headers = next(reader)
        
        # Assuming you want to search in a specific column, change the index accordingly
        search_column_index = headers.index(target_column)

        for row in reader:
            if reader.line_num == target_row:
                print("Timestamp from current line: " + str(row[search_column_index-1]))
                return row[search_column_index-1]
        
    return None
    

#method to get current number of rows in the table
def count_rows_in_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        row_count = sum(1 for row in reader)
        file.close
    return row_count



'''Main class to add cars to the database is here'''
#defines car attributes set to "null" if unknown or are looking to fill later
#gear ratio data must be consumed by human eye, from the tuning screens, as this is not provided by the data out
#if unable any values for ID/name/model/make/year use https://forums.forza.net/t/car-ordinal-list-for-forza-motorsport/649188 to reference their list

CarOrdinalID = "323" #Primary key of the table but can be found in telemetry captures
CarFriendlyName = "Lancia Delta"
CarMake = "Lancia"
CarModel = "Delta HF Integrale EVO"
CarManYear = "1992"
CarClass = "1" #Between 0 (D – worst cars) and 7 (X class – best cars) inclusive
CarPerformanceIndex = "351" #Between 100 (worst car) and 999 (best car) inclusive
DriveTrainType = "2" #0 = FWD, 1 = RWD, 2 = AWD
NumCylinders = "4"
EngineMaxRPM = "9000"
EngineIdleRPM = "800"
Gears = "5"
FinalDriveRatio = "null"
Ratio1 = "null"
Ratio2 = "null"
Ratio3 = "null"
Ratio4 = "null" 
Ratio5 = "null"
Ratio6 = "null"
Ratio7 = "null"
Ratio8 = "null"
Ratio9 = "null"
Ratio10 = "null"

#Defines file path and name
file_name = "DBModule\carDb.csv"

# Create a Path object
file_path_obj = Path(file_name)

if file_path_obj.is_file():
    print(f'The file "{file_name}" exists.')

    #Sets search term for searching CSV file for match
    search_term = CarOrdinalID  

    #Runs search_csv method and returns row value if matched
    result = search_csv(file_name, search_term)

    if result:
        print(f'Match found for CarOrdinalID: '+str(CarOrdinalID)+' in row# ' + str(result))
        #find line item and grab timestamp
        resultLastModified = get_value_from_csv(file_name, result)

        #compare timestamp to current and determine if swap is required
        if datetime.now() > datetime.strptime(resultLastModified, "%Y-%m-%d %H:%M:%S.%f"):
            #Should add a line comparison to ensure there are updates required but skipping for now
            
            #Overwrite entry in the table
            overwriteEntry(result, CarOrdinalID, CarFriendlyName, CarMake, CarModel, CarManYear, CarClass, CarPerformanceIndex, DriveTrainType, NumCylinders, EngineMaxRPM, EngineIdleRPM, Gears, FinalDriveRatio, Ratio1, Ratio2, Ratio3, Ratio4, Ratio5, Ratio6, Ratio7, Ratio8, Ratio9, Ratio10)
            print("Line #" + str(result) + " updated based on outdated timestamp")
    else:
        print(f'No match found for {"CarOrdinalID: " + str(search_term)}.')

        #Adds entry to the table on the next available row
        addEntry(CarOrdinalID, CarFriendlyName, CarMake, CarModel, CarManYear, CarClass, CarPerformanceIndex, DriveTrainType, NumCylinders, EngineMaxRPM, EngineIdleRPM, Gears, FinalDriveRatio, Ratio1, Ratio2, Ratio3, Ratio4, Ratio5, Ratio6, Ratio7, Ratio8, Ratio9, Ratio10)

        print(f'{"CarOrdinalID: " + str(search_term)} added to the database.')
else:
    print(f'The file "{file_name}" does not exist.')
    
    #runs method to create file and place headers
    createHeaderCSV()
    print("Database created with header information filled")

    #runs method to add provided data to the first row of the table
    addEntry(CarOrdinalID, CarFriendlyName, CarMake, CarModel, CarManYear, CarClass, CarPerformanceIndex, DriveTrainType, NumCylinders, EngineMaxRPM, EngineIdleRPM, Gears, FinalDriveRatio, Ratio1, Ratio2, Ratio3, Ratio4, Ratio5, Ratio6, Ratio7, Ratio8, Ratio9, Ratio10)

    print("CarOrdinalID " + str(CarOrdinalID) + " added to the database.")