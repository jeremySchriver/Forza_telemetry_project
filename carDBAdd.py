import csv
import os
from pathlib import Path
from datetime import datetime

#Defines file path and name
file_name = "E:\Code Projects\Case Lights\Forza M7\carDb.csv"

# Create a Path object
file_path_obj = Path(file_name)

#Creates blank table containing header
def createHeaderCSV():
    data = [
    ["CarOrdinalID", "CarFriendlyName", "CarMake", "CarModel", "CarManYear", "CarClass", "CarPerformanceIndex", "DriveTrainType", "NumCylinders", "CylinderNumber", "EngineMaxRPM", "EndingeIdelRPM", "Gears", "Ratio1", "Ratio2", "Ratio3", "Ratio4", "Ratio5", "Ratio6", "Ratio7", "Ratio8", "Ratio9", "Ratio10", "LastModified"],
    ]
    
    # Writing to the CSV file
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(data[0])

        file.close

#CSV writer function to append entry to the table
def addEntry(CarOrdinalID, CarFriendlyName, CarMake, CarModel, CarManYear, CarClass, CarPerformanceIndex, DriveTrainType, NumCylinders, EngineMaxRPM, EngineIdleRPM, Gears, Ratio1, Ratio2, Ratio3, Ratio4, Ratio5, Ratio6, Ratio7, Ratio8, Ratio9, Ratio10):
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
def overwriteEntry(Row, CarOrdinalID, CarFriendlyName, CarMake, CarModel, CarManYear, CarClass, CarPerformanceIndex, DriveTrainType, NumCylinders, EngineMaxRPM, EngineIdleRPM, Gears, Ratio1, Ratio2, Ratio3, Ratio4, Ratio5, Ratio6, Ratio7, Ratio8, Ratio9, Ratio10):
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

#defines car attributes
CarOrdinalID = "2352"
CarFriendlyName = "Acura NSX"
CarMake = "Acura"
CarModel = "NSX"
CarManYear = "2017"
CarClass = "6" #Between 0 (D – worst cars) and 7 (X class – best cars) inclusive
CarPerformanceIndex = "836" #Between 100 (worst car) and 999 (best car) inclusive
DriveTrainType = "2" #0 = FWD, 1 = RWD, 2 = AWD
NumCylinders = "6"
EngineMaxRPM = "9000"
EngineIdleRPM = "800"
Gears = "9"
Ratio1 = "3.84"
Ratio2 = "2.43"
Ratio3 = "1.78"
Ratio4 = "1.43" 
Ratio5 = "1.21"
Ratio6 = "1.04"
Ratio7 = ".88"
Ratio8 = ".75"
Ratio9 = ".63"
Ratio10 = "null"

if file_path_obj.is_file():
    print(f'The file "{file_name}" exists.')

    #Sets search term for searching CSV file for match
    search_term = CarOrdinalID  

    #Runs search_csv method and returns row value if matched
    result = search_csv(file_name, search_term)

    if result:
        print(f'Match found for ordinal# '+str(CarOrdinalID)+' in row# ' + str(result))
        #find line item and grab timestamp
        resultLastModified = get_value_from_csv(file_name, result)

        #compare timestamp to current and determine if swap is required
        if datetime.now() > datetime.strptime(resultLastModified, "%Y-%m-%d %H:%M:%S.%f"):
            #Should add a line comparison to ensure there are updates required but skipping for now
            
            #Overwrite entry in the table
            overwriteEntry(result, CarOrdinalID, CarFriendlyName, CarMake, CarModel, CarManYear, CarClass, CarPerformanceIndex, DriveTrainType, NumCylinders, EngineMaxRPM, EngineIdleRPM, Gears, Ratio1, Ratio2, Ratio3, Ratio4, Ratio5, Ratio6, Ratio7, Ratio8, Ratio9, Ratio10)
            print("Line #" + str(result) + " updated based on outdated timestamp")
    else:
        print(f'No match found for {"CarOrdinalID" + str(search_term)}.')

        #Adds entry to the table on the next available row
        addEntry(CarOrdinalID, CarFriendlyName, CarMake, CarModel, CarManYear, CarClass, CarPerformanceIndex, DriveTrainType, NumCylinders, EngineMaxRPM, EngineIdleRPM, Gears, Ratio1, Ratio2, Ratio3, Ratio4, Ratio5, Ratio6, Ratio7, Ratio8, Ratio9, Ratio10)
else:
    print(f'The file "{file_name}" does not exist.')
    
    #runs method to create file and place headers
    createHeaderCSV()
    print("File created with headers")

    #runs method to add provided data to the first row of the table
    addEntry(CarOrdinalID, CarFriendlyName, CarMake, CarModel, CarManYear, CarClass, CarPerformanceIndex, DriveTrainType, NumCylinders, EngineMaxRPM, EngineIdleRPM, Gears, Ratio1, Ratio2, Ratio3, Ratio4, Ratio5, Ratio6, Ratio7, Ratio8, Ratio9, Ratio10)
    print("Line filled")