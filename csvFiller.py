import pandas as pd
import csv
import numpy as np
import os
import time
import matplotlib.pyplot as plt
import scipy
from scipy.optimize import curve_fit

'''Class intended for dyno use. Since FM8 currently has no Dyno option it can be difficult to build power curves for you car. This class is meant to be run on a captured data set from a live race/practice. Run through your normal race and let the telemetryCapture class build your csv file. Ensure your file name in this class matches the capture file before starting the chain of modifications.

Intended normalization pattern
1. Split capture file into individual files per gear
    a. Runs a sub method to round the values of idle RPM and max RPM before writing the row
    b. Runs a sub method to create and fill new rows for the following values roundedCurrentRPM, roundedPower, and roundedTorque
2. Looks through each gear file to finds duplicate values at each rounded RPM point 
    a. Runs a sub method to find the mean value of torque and power values at the RPM point
    b. Removes all duplicate rows
    c. Fills rows with static values and the mean values for the RPM
3. Determine a % missing data points after scrubbing process
    a. Present graphs?
    b. Ask if user wants an interpolated data set to work from and for which gear(s)
4. Interpolation process to be defined here'''

def createHeaderCSV(file_name):
    data = ["Timestamp", "CarOrdinalID", "CarClass", "CarPerformanceIndex", "DriveTrainType", "NumCylinders", "EngineMaxRPM", "EndingeIdelRPM", "EngineCurrentRPM", "Speed", "Power", "Torque", "Boost", "Gear", "Accel", "Brake", "Clutch", "HandBrake", "Fuel", "roundedCurrentRPM", "roundedPower", "roundedTorque",]
    
    # Writing to the CSV file
    if not os.path.exists(file_name):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Write the header
            writer.writerow(data)

            file.close
        print(f"CSV file '{file_name}' created successfully.")
    else:
        print(f"CSV file '{file_name}' already exists.")

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
def gearPullBuilder(numGears,captureFile):
    count = 0
    while count < numGears:
        gear = count+1
        #Sets file name for each gear in the car
        fileName = "Gear_" + str(gear) + "_data.csv"
        createHeaderCSV(fileName)
        
        #grabs rows that match the gear supplied
        matchedRows = read_csv_and_filter(captureFile, 'Gear', gear)
        
        if len(matchedRows) != 0:
            #writes row to the matching file
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

def duplicateRPMNormalizer(fileName, gear):
    #Cast CSV into a dataframe
    df = pd.read_csv(fileName)

    #Find duplicate rows
    duplicate_rows = df[df.duplicated(subset=['roundedCurrentRPM'], keep=False)]

    # Group by the duplicate values in column 'A'
    groups = duplicate_rows.groupby('roundedCurrentRPM')

    # Create separate DataFrames for each group
    duplicate_dfs = [group for _, group in groups]

    # Print each DataFrame
    for i, dup_df in enumerate(duplicate_dfs):
        print(f"Duplicate Group {i+1}:\n{dup_df}\n")

    #averages values found in duplicate rows to help normalize
    count = 0
    corrected_rows = []

    while count < len(duplicate_dfs):
        cf = duplicate_dfs[count]
        averageRoundedTorque = round(cf['roundedTorque'].mean())
        averageRoundedPower = round(cf['roundedPower'].mean())
        averageSpeed = cf['Speed'].max()
        averagePower = cf['Power'].max()
        averageBoost = cf['Boost'].max()
        averageTorque = cf['Torque'].max()
        corrected_rows.append({'Timestamp': '1/31/2024 01:00:01','CarOrdinalID': cf['CarOrdinalID'].max(),'CarClass': cf['CarClass'].max(),'CarPerformanceIndex': cf['CarPerformanceIndex'].max(),'DriveTrainType': cf['DriveTrainType'].max(),'NumCylinders': cf['NumCylinders'].max(),'EngineMaxRPM': cf['EngineMaxRPM'].max(),'EndingeIdelRPM': cf['EndingeIdelRPM'].max(),'Speed': averageSpeed,'Power': averagePower,'Torque': averageTorque,'Boost': 0,'Gear': cf['Gear'].max(),'Accel': 0,'Brake': 0,'Clutch': 0,'HandBrake': 0,'Fuel': 0,'roundedCurrentRPM': cf['roundedCurrentRPM'].max(),'roundedPower': averageRoundedPower,'roundedTorque': averageRoundedTorque})
        count = count + 1

    #Remove duplicate rows from the original data set
    df_cleaned = df.drop_duplicates(subset='roundedCurrentRPM', keep=False)

    #Sets corrected row data back into a data frame
    df_corrected_rows = pd.DataFrame(corrected_rows)

    #Appends corrected rows back to the data set
    frames = [df_cleaned,df_corrected_rows]
    combined_dataframe = pd.concat(frames, ignore_index=True)

    #sort the data frame
    sorted_combined_dataframe = combined_dataframe.sort_values(by=['roundedCurrentRPM'])

    #Print results to file
    newFileName = 'combinedGear_' + str(gear) + '_data.csv'
    sorted_combined_dataframe.to_csv(newFileName, index=False)

def deletePreviousData(numGears):
    count = 1
    while count <= numGears:
        file_path = "Gear_" + str(count) + "_data.csv"
        file_path1 = "combinedGear_" + str(count) + "_data.csv"
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' deleted successfully.")
        else:
            print(f"File '{file_path}' does not exist.")

        if os.path.exists(file_path1):
            os.remove(file_path1)
            print(f"File '{file_path1}' deleted successfully.")
        else:
            print(f"File '{file_path1}' does not exist.")
        count = count + 1

def plotter(fileName, EngineMaxRPM):
    df = pd.read_csv(fileName)
    x = df['roundedCurrentRPM']
    y = df['roundedTorque']

    print("Printing graph of only duplicate max data")
    plt.plot(x,y)
    #plt.scatter(x,y)
    plt.title('Simple Line Chart')
    plt.xlabel('roundedCurrentRPM')
    plt.ylabel('roundedTorque')
    plt.show()

    #Remove rows where torque values are 0
    zeroRemoved_combined_dataframe = df[df['roundedTorque'] != 0]

    sorted_zeroRemoved_combined_dataframe = zeroRemoved_combined_dataframe.sort_values(by=['roundedCurrentRPM'],ascending=True)
    #print(sorted_zeroRemoved_combined_dataframe)

    x = sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM']
    y = sorted_zeroRemoved_combined_dataframe['roundedTorque']

    print("Printing graph of duplicate max data and torque = 0 values")
    plt.plot(x,y)
    #plt.scatter(x,y)
    plt.title('Simple Line Chart')
    plt.xlabel('roundedCurrentRPM')
    plt.ylabel('roundedTorque')
    plt.show()

    # Define the quadratic function to fit the data
    def quadratic_func(x, a, b, c):
        return a * x**2 + b * x + c

    # Sample data for the y-axis
    y_data = np.array(sorted_zeroRemoved_combined_dataframe['roundedTorque'])
    y2_data = np.array(sorted_zeroRemoved_combined_dataframe['roundedPower'])

    # Fit the quadratic function to the data using curve_fit
    popt, pcov = curve_fit(quadratic_func, sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], y_data)
    popt2, pcov = curve_fit(quadratic_func, sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], y2_data)

    xA = np.arange(EngineMaxRPM)
    yA = np.arange(sorted_zeroRemoved_combined_dataframe['roundedPower'].max())
    #print(quadratic_func(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], *popt2))
    plt.plot(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'],round(quadratic_func(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], *popt2)))
    plt.show()

    #quadratic_func(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], *popt2).to_csv('E:\Code Projects\Case Lights\Forza M7\curveOutput.csv', index=False)

    print("Plotting best fit quadratic line")
    # Plot the original data and the fitted quadratic curve
    plt.figure()
    plt.scatter(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], y_data, label='Torque')
    plt.plot(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], quadratic_func(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], *popt), 'r-', label='Fitted quadratic torque curve')
    plt.scatter(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], y2_data, label='Power')
    plt.plot(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], quadratic_func(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], *popt2), 'r-', label='Fitted quadratic power curve')
    plt.legend()
    plt.show()

#Define variables
captureFile = "logTelemetry2.csv"
numGears = 7
gearCounter = 1

df = pd.read_csv(captureFile)

#Add pause for user input y/delete files previously generated by this class n/continue with warning data may be skewed
user_input = input("Is this the same car as last run?")

if user_input.lower() == "yes" or user_input.lower() == "y" or user_input.lower() == "ys":
    next_input = input("Have you made any performance or tuning updates to the car since the last run?")
    
    if next_input.lower() == "yes" or next_input.lower() == "y" or next_input.lower() == "ys":
        print("It's recommended that you wipe previously existing data before running this process or data may become skewed, unless its the same car with the same performance index.")
        next_input = input("Please confirm that you would like to delete previous data.")
        
        if next_input.lower() == "yes" or next_input.lower() == "y" or next_input.lower() == "ys":
            #placeholder for deleting old files before continuing
            print("Starting process for deleting old data files.")
            deletePreviousData(numGears)
            time.sleep(5)

            #Build files for each gear
            gearPullBuilder(numGears,captureFile)

            #itterates through the created gear files to build new copies with normalized and sorted data
            while gearCounter <= numGears:
                fileName = "Gear_" + str(gearCounter) + "_data.csv"
                duplicateRPMNormalizer(fileName, gearCounter)
                #plotter(fileName, df.EngineMaxRPM.max())
                gearCounter = gearCounter + 1
        elif next_input.lower() == "no" or next_input.lower() == "n":
            #continue into process
            print("Continuing process since user opted to not delete previous data.")

            #Build files for each gear
            gearPullBuilder(numGears,captureFile)

            #itterates through the created gear files to build new copies with normalized and sorted data
            while gearCounter <= numGears:
                fileName = "Gear_" + str(gearCounter) + "_data.csv"
                duplicateRPMNormalizer(fileName, gearCounter)
                #plotter(fileName, df.EngineMaxRPM.max())
                gearCounter = gearCounter + 1

    elif next_input.lower() == "no" or next_input.lower() == "n":
        #continue into process
        print("Continuing process since car and performance index are the same.")

        #Build files for each gear
        gearPullBuilder(numGears,captureFile)

        #itterates through the created gear files to build new copies with normalized and sorted data
        while gearCounter <= numGears:
            fileName = "Gear_" + str(gearCounter) + "_data.csv"
            duplicateRPMNormalizer(fileName, gearCounter)
            #plotter(fileName, df.EngineMaxRPM.max())
            gearCounter = gearCounter + 1
    else:
        print("Invalid input.")
        #break
elif user_input.lower() == "no" or user_input.lower() == "n":
    print("It's recommended that you wipe previously existing data before running this process or data may become skewed, unless its the same car with the same performance index.")
    next_input = input("Please confirm that you would like to delete previous data.")

    if next_input.lower() == "yes" or next_input.lower() == "y" or next_input.lower() == "ys":
            #placeholder for deleting old files before continuing
            print("Starting process for deletingnn old data files.")
            deletePreviousData(numGears)
            time.sleep(5)

            #Build files for each gear
            gearPullBuilder(numGears,captureFile)

            #itterates through the created gear files to build new copies with normalized and sorted data
            while gearCounter <= numGears:
                fileName = "Gear_" + str(gearCounter) + "_data.csv"
                duplicateRPMNormalizer(fileName, gearCounter)
                #plotter(fileName, df.EngineMaxRPM.max())
                gearCounter = gearCounter + 1
    elif next_input.lower() == "no" or next_input.lower() == "n":
        #continue into process
        print("Continuing process since car and performance index are the same.")

        #Build files for each gear
        gearPullBuilder(numGears,captureFile)

        #itterates through the created gear files to build new copies with normalized and sorted data
        while gearCounter <= numGears:
            fileName = "Gear_" + str(gearCounter) + "_data.csv"
            duplicateRPMNormalizer(fileName, gearCounter)
            #plotter(fileName, df.EngineMaxRPM.max())
            gearCounter = gearCounter + 1
else:
    print("Invalid input.")
    #break

#generateMissingRPMData("Gear_2_data.csv")
#generateMissingTorqueData("E:\Code Projects\Case Lights\Forza M7\Gear_2_dataFilled.csv")