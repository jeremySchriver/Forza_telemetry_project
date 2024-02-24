import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv

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
def gearPullBuilder(file_Name, numGears):
    count = 0
    while count < numGears:
        gear = count+1
        #Sets file name for each gear in the car
        fileName = "Gear_" + str(gear) + "_data.csv"
        createHeaderCSV(fileName)
        
        #grabs rows that match the gear supplied
        matchedRows = read_csv_and_filter(file_Name, 'Gear', gear)
        
        #writes row to the matching fiel
        write_to_csv(fileName, matchedRows)

        #sets the counter to next
        count = count + 1

    print("File building completed")

def normalizeData(fileName):
    #Create dataframe out of the gear data provided
    df = pd.read_csv(fileName)

    #Find duplicate values of roundedCurrentRPM
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
        averageSpeed = cf['Speed'].mean()
        averagePower = cf['Power'].mean()
        averageBoost = cf['Boost'].mean()
        averageTorque = cf['Torque'].mean()
        corrected_rows.append({'Timestamp': '1/31/2024 01:00:01','CarOrdinalID': cf['CarOrdinalID'].max(),'CarClass': cf['CarClass'].max(),'CarPerformanceIndex': cf['CarPerformanceIndex'].max(),'DriveTrainType': cf['DriveTrainType'].max(),'NumCylinders': cf['NumCylinders'].max(),'EngineMaxRPM': cf['EngineMaxRPM'].max(),'EndingeIdelRPM': cf['EndingeIdelRPM'].max(),'Speed': averageSpeed,'Power': averagePower,'Torque': averageTorque,'Boost': 0,'Gear': cf['Gear'].max(),'Accel': 0,'Brake': 0,'Clutch': 0,'HandBrake': 0,'Fuel': 0,'roundedCurrentRPM': cf['roundedCurrentRPM'].max(),'roundedPower': averageRoundedPower,'roundedTorque': averageRoundedTorque})
        count = count + 1

    #Remove duplicate rows from the original data set
    df_cleaned = df.drop_duplicates(subset='roundedCurrentRPM', keep=False)

    #Optional Print results to file
    #df_cleaned.to_csv('duplicateCleanedGear2Output.csv', index=False)

    #Create a new datafram with the corrected rows
    df_corrected_rows = pd.DataFrame(corrected_rows)

    #Appends corrected rows back to the data set
    frames = [df_cleaned,df_corrected_rows]
    combined_dataframe = pd.concat(frames, ignore_index=True)

    #sort the data frame
    sorted_combined_dataframe = combined_dataframe.sort_values(by=['roundedCurrentRPM'])

    #Optional Print results to file
    #sorted_combined_dataframe.to_csv('combinedGear2Output.csv', index=False)

    #Remove rows where torque values are 0
    zeroRemoved_combined_dataframe = sorted_combined_dataframe[sorted_combined_dataframe['roundedTorque'] != 0]

    #sort the new data frame
    sorted_zeroRemoved_combined_dataframe = zeroRemoved_combined_dataframe.sort_values(by=['roundedCurrentRPM'],ascending=True)

    #Optional Print results to file
    #sorted_zeroRemoved_combined_dataframe.to_csv('dropped0TorqueGear2Output.csv', index=False)

    # Define the quadratic function to fit the data
    def quadratic_func(x, a, b, c):
        return a * x**2 + b * x + c

    # Sample data for the y-axis
    y_data = np.array(sorted_zeroRemoved_combined_dataframe['roundedTorque'])
    y2_data = np.array(sorted_zeroRemoved_combined_dataframe['roundedPower'])

    # Fit the quadratic function to the data using curve_fit
    popt, pcov = curve_fit(quadratic_func, sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], y_data)
    popt2, pcov = curve_fit(quadratic_func, sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], y2_data)

    #set quadratic lines into execution
    fitTorqueData = np.array(quadratic_func(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], *popt))
    fitPowerData = np.array(quadratic_func(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], *popt2))
    holderArray = np.array(sorted_zeroRemoved_combined_dataframe)

    #build a new data frame with the curved data
    count = 0
    frameSize = len(fitTorqueData)
    curvedFrame = []

    while count < frameSize:
        curvedFrame.append({'Timestamp': '1/31/2024 01:00:01','CarOrdinalID': holderArray[count, 1],'CarClass': holderArray[count, 2],'CarPerformanceIndex': holderArray[count, 3],'DriveTrainType': holderArray[count, 4],'NumCylinders': holderArray[count, 5],'EngineMaxRPM': holderArray[count, 6],'EndingeIdelRPM': holderArray[count, 7],'EngineCurrentRPM': holderArray[count, 8],'Speed': holderArray[count, 9],'Power': holderArray[count, 10],'Torque': holderArray[count, 11],'Boost': holderArray[count, 12],'Gear': holderArray[count, 13],'Accel': holderArray[count, 14],'Brake': holderArray[count, 15],'Clutch': holderArray[count, 16],'HandBrake': holderArray[count, 17],'Fuel': holderArray[count, 18],'roundedCurrentRPM': holderArray[count, 19],'roundedPower': round(fitPowerData[count]),'roundedTorque': round(fitTorqueData[count])})
        count = count + 1

    #Create a dataframe out of the curvedFrame data
    df_holderArray = pd.DataFrame(curvedFrame)

    #Option print data to file
    #df_holderArray.to_csv('E:\Code Projects\Case Lights\Forza M7\combinedCurveOutput.csv', index=False)

    # Assuming the column name containing integers is 'integer_column'
    integer_column = df_holderArray['roundedCurrentRPM']

    # Determine the min and max values of the column
    min_value = integer_column.min()
    max_value = integer_column.max()

    # Generate a list of missing values
    missing_values = list(set(range(min_value, max_value + 1)) - set(integer_column))
    numbersMissing = len(missing_values)

    #Set numpy arrays
    rpmArray = np.array(df_holderArray['roundedCurrentRPM'])
    torqueArray = np.array(df_holderArray['roundedTorque'])
    powerArray = np.array(df_holderArray['roundedPower'])

    #Generate interpolated torque data
    interpolated_Torque = np.interp(missing_values, rpmArray, torqueArray)

    #Generate interpolated power data
    interpolated_Power = np.interp(missing_values, rpmArray, powerArray)

    #Find static values in dataframe to fill in on new rows
    CarOrdinalID = df_holderArray['CarOrdinalID'].max()
    CarClass = df_holderArray['CarClass'].max()
    CarPerformanceIndex = df_holderArray['CarPerformanceIndex'].max()
    DriveTrainType = df_holderArray['DriveTrainType'].max()
    NumCylinders = df_holderArray['NumCylinders'].max()
    EngineMaxRPM = df_holderArray['EngineMaxRPM'].max()
    EndingeIdelRPM = df_holderArray['EndingeIdelRPM'].max()
    Gear = df_holderArray['Gear'].max()

    #Creates an array with the new rows
    new_rows = []
    count = 0
    while count < numbersMissing:
        new_rows.append({'Timestamp': '','CarOrdinalID': CarOrdinalID,'CarClass': CarClass,'CarPerformanceIndex': CarPerformanceIndex,'DriveTrainType': DriveTrainType,'NumCylinders': NumCylinders,'EngineMaxRPM': EngineMaxRPM,'EndingeIdelRPM': EndingeIdelRPM,'Speed': '','Power': 0,'Torque': 0,'Boost': 0,'Gear': Gear,'Accel': 0,'Brake': 0,'Clutch': 0,'HandBrake': 0,'Fuel': 0,'roundedCurrentRPM': missing_values[count],'roundedPower': round(interpolated_Power[count]),'roundedTorque': round(interpolated_Torque[count])})
        count = count + 1

    #Converts the array to a datafram
    df_new_rows = pd.DataFrame(new_rows)

    #Appends corrected rows back to the data set
    frames = [df_holderArray,df_new_rows]
    combined_dataframe = pd.concat(frames, ignore_index=True)

    #Resort the frame by roundedCurrentRPM
    combined_dataframe = combined_dataframe.sort_values(by=['roundedCurrentRPM'])
    print(combined_dataframe)

    #Print results to file
    combined_dataframe.to_csv('Gear_'+str(Gear)+'curveData.csv', index=False)

#Run methods to build Gear_X_data.csv files containing telem data for each gear
numberOfGears = 9
gearPullBuilder('logTelemetry copy.csv',numberOfGears)

#Runs data normalization/curving methods on the telem data for each gear and generates a new file for each gear
count = 1
while count <= numberOfGears:
    normalizeData('Gear_'+str(count)+'_data.csv')
    count = count + 1