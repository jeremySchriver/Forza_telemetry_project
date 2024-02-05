import pandas as pd
import csv
import numpy as np

df = pd.read_csv('logTelemetry copy.csv')

def createHeaderCSV(file_name):
    data = ["Timestamp", "CarOrdinalID", "CarClass", "CarPerformanceIndex", "DriveTrainType", "NumCylinders", "EngineMaxRPM", "EndingeIdelRPM", "EngineCurrentRPM", "Speed", "Power", "Torque", "Boost", "Gear", "Accel", "Brake", "Clutch", "HandBrake", "Fuel", "roundedCurrentRPM", "roundedPower", "roundedTorque",]
    
    # Writing to the CSV file
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(data)

        file.close

def read_csv_and_filter(csv_file, target_column, target_value):
    filtered_rows = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if str(row[target_column]) == str(target_value):
                #Rounds values before placing them in the array
                row['EndingeIdelRPM'] = round(float(row['EndingeIdelRPM']))
                row['EngineMaxRPM'] = round(float(row['EngineMaxRPM']))
                
                #Inserts a rounded value into the dictionary
                row['roundedCurrentRPM'] = round(float(row['EngineCurrentRPM']))
                row['roundedPower'] = round(float(row['Power']))
                row['roundedTorque'] = round(float(row['Torque']))

                #Add row to the 3d array
                filtered_rows.append(row)

    #Sorts array by roundedCurrentRPM in Ascending order
    filtered_rows.sort(key=lambda x: int(x['roundedCurrentRPM']))

    return filtered_rows

#Writes data to the desired CSV file which already contains headers
def write_to_csv(output_file, rows):
    with open(output_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writerows(rows)

#Main function to trigger other methods in this script. Builds required CSV files and fills them with data contained in the logTelemetry.csv file
def gearPullBuilder(numGears):
    count = 0
    while count < numGears:
        gear = count+1
        #Sets file name for each gear in the car
        fileName = "Gear_" + str(gear) + "_data.csv"
        createHeaderCSV(fileName)
        
        #grabs rows that match the gear supplied
        matchedRows = read_csv_and_filter('logTelemetry copy.csv', 'Gear', gear)
        
        #writes row to the matching fiel
        write_to_csv(fileName, matchedRows)

        #sets the counter to next
        count = count + 1

    print("File building completed")

def generateMissingRPMData(fileName):
    df = pd.read_csv(fileName)

    originalData = []

    #Captures original csv file into an array
    with open(fileName, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            #Add row to the 3d array
            originalData.append(row)


    # Assuming the column name containing integers is 'integer_column'
    integer_column = df['roundedCurrentRPM']

    # Determine the min and max values of the column
    min_value = integer_column.min()
    max_value = integer_column.max()

    #Find static values in table to fill later
    CarOrdinalID = df['CarOrdinalID'][1]
    CarClass = df['CarClass'][1]
    CarPerformanceIndex = df['CarPerformanceIndex'][1]
    DriveTrainType = df['DriveTrainType'][1]
    NumCylinders = df['NumCylinders'][1]
    EngineMaxRPM = df['EngineMaxRPM'][1]
    EndingeIdelRPM = df['EndingeIdelRPM'][1]
    Gear = df['Gear'][1]

    # Generate a list of missing values
    missing_values = list(set(range(min_value, max_value + 1)) - set(integer_column))
    numbersMissing = len(missing_values)
    count = 0

    while count < numbersMissing:
        originalData.append({'Timestamp': '','CarOrdinalID': CarOrdinalID,'CarClass': CarClass,'CarPerformanceIndex': CarPerformanceIndex,'DriveTrainType': DriveTrainType,'NumCylinders': NumCylinders,'EngineMaxRPM': EngineMaxRPM,'EndingeIdelRPM': EndingeIdelRPM,'Speed': '','Power': 0,'Torque': 0,'Boost': 0,'Gear': Gear,'Accel': 0,'Brake': 0,'Clutch': 0,'HandBrake': 0,'Fuel': 0,'roundedCurrentRPM': missing_values[count],'roundedPower': 0,'roundedTorque': 0})
        count = count + 1

    #sorts the array in ascending order based on roundedCurrentRPM
    originalData.sort(key=lambda x: int(x['roundedCurrentRPM']))

    file_name = 'Gear_2_dataFilled.csv'
    createHeaderCSV(file_name)
    write_to_csv(file_name, originalData)

def generateMissingTorqueData(fileName):
    originalData = []
    count = 0

    #Captures original csv file into an array
    with open(fileName, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            #Add row to the 3d array
            originalData.append(row)

    totalRows = len(originalData)

    #Search through data to find all rows with missing value and build a list of the rows
    missingRows = []
    foundRows = []
    while count < totalRows:
        if originalData[count]['roundedTorque'] == 0:
            missingRows.append(count)
        else:
            foundRows.append(count)
        count = count + 1

    #use numpy to find the linear values between the rows
    count = 0
    foundSize = len(foundRows)
    while count < foundSize:
        try:
            firstMatch = foundRows[count]
            secondMatch = foundRows[count+1]
            rowsAppart = secondMatch - firstMatch

            #use numpy
            numpyArray = np.linspace(int(originalData[firstMatch]['roundedTorque']),int(originalData[secondMatch]['roundedTorque']),rowsAppart)
            secondCount = 0
            while secondCount < rowsAppart:
                originalData[firstMatch+1]['roundedTorque'] = round(numpyArray[secondCount])
                secondCount = secondCount + 1
            count = count + 1
        except:
            break

    write_to_csv('Gear_2_torqueDataFilled.csv', originalData)
    print("Torque generation complete")


gearPullBuilder(9)
generateMissingRPMData("Gear_2_data.csv")
#generateMissingTorqueData("E:\Code Projects\Case Lights\Forza M7\Gear_2_dataFilled.csv")