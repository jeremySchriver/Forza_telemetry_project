import pandas as pd
import csv
import numpy as np
import os
import time
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
from sklearn.ensemble import IsolationForest
from shapely.geometry import LineString

'''Class intended for dyno use. Since FM8 currently has no Dyno option it can be difficult to build power curves for you car. This class is meant to be run on a captured data set from a live race/practice. Run through your normal race and let the telemetryCapture class build your csv file. Ensure your file name in this class matches the capture file before starting the chain of modifications.'''

def createHeaderCSV(file_name):
    data = ["Timestamp", "CarOrdinalID", "CarClass", "CarPerformanceIndex", "DriveTrainType", "NumCylinders", "EngineMaxRPM", "EngineIdleRPM", "EngineCurrentRPM", "Speed", "Power", "Torque", "Boost", "Gear", "Accel", "Brake", "Clutch", "HandBrake", "Fuel", "roundedCurrentRPM", "roundedPower", "roundedTorque",]
    
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
                row['EngineIdleRPM'] = round(float(row['EngineIdleRPM']))
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
def gearPullBuilder(numGears,captureFile,carOrdinalID):
    count = 0
    while count < numGears:
        gear = count+1
        #Sets file name for each gear in the car
        fileName = os.path.join("TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_Gear_" + str(gear) + "_data.csv")
        createHeaderCSV(fileName)
        
        #grabs rows that match the gear supplied
        matchedRows = read_csv_and_filter(captureFile, 'Gear', gear)
        
        if len(matchedRows) != 0:
            #writes row to the matching file
            write_to_csv(fileName, matchedRows)

        #sets the counter to next
        count = count + 1

    print("File building completed")

def duplicateRPMNormalizer(fileName, gear, carOrdinalID):
    #Cast CSV into a dataframe
    df = pd.read_csv(fileName)

    #Find duplicate rows
    duplicate_rows = df[df.duplicated(subset=['roundedCurrentRPM'], keep=False)]

    # Group by the duplicate values in column 'A'
    groups = duplicate_rows.groupby('roundedCurrentRPM')

    # Create separate DataFrames for each group
    duplicate_dfs = [group for _, group in groups]

    # Print each DataFrame
    #for i, dup_df in enumerate(duplicate_dfs):
        #print(f"Duplicate Group {i+1}:\n{dup_df}\n")

    #averages values found in duplicate rows to help normalize
    count = 0
    corrected_rows = []

    while count < len(duplicate_dfs):
        cf = duplicate_dfs[count]
        averageRoundedTorque = round(cf['roundedTorque'].max())
        averageRoundedPower = round(cf['roundedPower'].max())
        averageSpeed = cf['Speed'].max()
        averagePower = cf['Power'].max()
        averageBoost = cf['Boost'].max()
        averageTorque = cf['Torque'].max()
        corrected_rows.append({'Timestamp': '1/31/2024 01:00:01','CarOrdinalID': cf['CarOrdinalID'].max(),'CarClass': cf['CarClass'].max(),'CarPerformanceIndex': cf['CarPerformanceIndex'].max(),'DriveTrainType': cf['DriveTrainType'].max(),'NumCylinders': cf['NumCylinders'].max(),'EngineMaxRPM': cf['EngineMaxRPM'].max(),'EngineIdleRPM': cf['EngineIdleRPM'].max(),'Speed': averageSpeed,'Power': averagePower,'Torque': averageTorque,'Boost': 0,'Gear': cf['Gear'].max(),'Accel': 0,'Brake': 0,'Clutch': 0,'HandBrake': 0,'Fuel': 0,'roundedCurrentRPM': cf['roundedCurrentRPM'].max(),'roundedPower': averageRoundedPower,'roundedTorque': averageRoundedTorque})
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
    newFileName = os.path.join('TelemDataFiles', str(carOrdinalID), str(carOrdinalID) + '_combinedGear_' + str(gear) + '_data.csv')
    sorted_combined_dataframe.to_csv(newFileName, index=False)

#Method to delete previous files for the car ID in question
def deletePreviousData(numGears,carOrdinalID):
    count = 1
    while count <= numGears:
        file_path = os.path.join(os.getcwd(), "TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_Gear_" + str(count) + "_data.csv")
        file_path1 = os.path.join(os.getcwd(), "TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_combinedGear_" + str(count) + "_data.csv")
        file_path2 = os.path.join(os.getcwd(), "TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_firstPlot_Gear_" + str(count) + "_data.png")
        file_path3 = os.path.join(os.getcwd(), "TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_secondPlot_Gear_" + str(count) + "_data.png")
        file_path4 = os.path.join(os.getcwd(), "TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_combinedCurvedPlot_Gear_" + str(count) + "_data.png")
        file_path5 = os.path.join(os.getcwd(), "TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_Gear_" + str(count) + "_PowerAndTorqueCurve.png")
        file_path6 = os.path.join(os.getcwd(), "TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_TorquePerGearOverSpeed.png")
        file_path7 = os.path.join(os.getcwd(), "TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_TorquePerGearOverSpeed_wIntersections.png")
        file_path8 = os.path.join(os.getcwd(), "TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_RPMvSpeed.png")
        file_path9 = os.path.join(os.getcwd(), "TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_Gear_" + str(count) + "_PowerAndTorqueCurve_Poly.png")
        
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

        if os.path.exists(file_path2):
            os.remove(file_path2)
            print(f"File '{file_path2}' deleted successfully.")
        else:
            print(f"File '{file_path2}' does not exist.")

        if os.path.exists(file_path3):
            os.remove(file_path3)
            print(f"File '{file_path3}' deleted successfully.")
        else:
            print(f"File '{file_path3}' does not exist.")

        if os.path.exists(file_path4):
            os.remove(file_path4)
            print(f"File '{file_path4}' deleted successfully.")
        else:
            print(f"File '{file_path4}' does not exist.")

        if os.path.exists(file_path5):
            os.remove(file_path5)
            print(f"File '{file_path5}' deleted successfully.")
        else:
            print(f"File '{file_path5}' does not exist.")

        if os.path.exists(file_path6):
            os.remove(file_path6)
            print(f"File '{file_path6}' deleted successfully.")
        else:
            print(f"File '{file_path6}' does not exist.")

        if os.path.exists(file_path7):
            os.remove(file_path7)
            print(f"File '{file_path7}' deleted successfully.")
        else:
            print(f"File '{file_path7}' does not exist.")

        if os.path.exists(file_path8):
            os.remove(file_path8)
            print(f"File '{file_path8}' deleted successfully.")
        else:
            print(f"File '{file_path8}' does not exist.")

        if os.path.exists(file_path9):
            os.remove(file_path9)
            print(f"File '{file_path9}' deleted successfully.")
        else:
            print(f"File '{file_path9}' does not exist.")

        count = count + 1

#Method to build the torque and power v RPM curve files
def powerCurvePlotter(fileName, currentGear, carOrdinalID):
    df = pd.read_csv(fileName)

    #Remove rows where torque values are 0
    zeroRemoved_combined_dataframe = df[df['roundedTorque'] != 0]

    #Sort the data frame
    sorted_zeroRemoved_combined_dataframe = zeroRemoved_combined_dataframe.sort_values(by=['roundedCurrentRPM'],ascending=True)

    # Define the quadratic function to fit the data
    def quadratic_func(x, a, b, c):
        return a * x**2 + b * x + c

    # Sample data for the y-axis
    y_data = np.array(sorted_zeroRemoved_combined_dataframe['roundedTorque'])
    y2_data = np.array(sorted_zeroRemoved_combined_dataframe['roundedPower'])

    # Fit the quadratic function to the data using curve_fit
    popt, pcov = curve_fit(quadratic_func, sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], y_data)
    popt2, pcov = curve_fit(quadratic_func, sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], y2_data)

    #quadratic_func(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], *popt2).to_csv('E:\Code Projects\Case Lights\Forza M7\curveOutput.csv', index=False)

    # Plot the original data and the fitted quadratic curve
    plt.figure()

    '''Used for showing corrected values against normalized scatter data'''
    plt.scatter(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], y_data, label='Torque', color= 'orange')
    #plt.scatter(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], y2_data, label='Power', color= 'blue')

    plt.plot(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], quadratic_func(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], *popt), label='Quadratic fit torque curve', color= 'red')
    plt.plot(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], quadratic_func(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], *popt2), label='Quadratic fit power curve', color= 'green')

    #Finds the maximum y-axis values for each curve
    max_torque_value = np.max(quadratic_func(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], *popt))
    max_power_value = np.max(quadratic_func(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], *popt2))

    # Find the index of the maximum torque value
    max_torque_index = np.argmax(quadratic_func(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], *popt))

    # Find the index of the maximum power value
    max_power_index = np.argmax(quadratic_func(sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'], *popt2))

    # Get the x-values corresponding to the maximum torque and power
    xValofMaxTorque = sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'].iloc[max_torque_index]
    xValofMaxPower = sorted_zeroRemoved_combined_dataframe['roundedCurrentRPM'].iloc[max_power_index]

    plt.scatter(xValofMaxTorque, max_torque_value, label= 'Max Torque Value', color='red')
    plt.scatter(xValofMaxPower, max_power_value, label= 'Max Power Value', color='green')

    # Annotate maximum values on the plot
    plt.text(xValofMaxTorque, max_torque_value, f'Max Torque: {max_torque_value:.2f}', ha='center', va='bottom', color='red', fontsize=6)
    plt.text(xValofMaxPower, max_power_value, f'Max Power: {max_power_value:.2f}', ha='center', va='bottom', color='green', fontsize=6)

    #Sets labels for chart
    plt.xlabel('Engine RPM\'s (Rotations Per Minute)')
    plt.ylabel('Torque (ft lbs)/Power (Horsepower)')
    plt.title('Torque and Horsepower Band For Gear ' + str(currentGear))

    #Sets a legend for chart
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    #Turns on the grid in the chart
    plt.grid(True)

    #Saves the image to a png file
    plt.savefig(os.path.join("TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_Gear_" + str(currentGear) + "_PowerAndTorqueCurve.png"), bbox_inches='tight')

#New method to build the torque and power vs RPM curve files. New method uses polynomial curving and a different run book of data normalization before plotting
def altPowerCurvePlotter(carOrdinalID, numGears):
    a = {}
    count = 1
    while count <= numGears:
        key = "df" + str(count)
        path = os.path.join('TelemDataFiles', str(carOrdinalID), str(carOrdinalID) + '_Gear_' + str(count) + '_data.csv')
        value = pd.read_csv(path)

        a[key] = value
        count += 1

    #Rounds all the RPM data, in each dataframe, to the nearest 50 rpm value
    count = 1
    while count <= numGears:
        key = "df" + str(count)
        newKey = "roundedDf" + str(count)

        cf = a[key]
        cf['roundedCurrentRPM'] = np.round(cf['roundedCurrentRPM'] / 50) * 50

        a[newKey] = cf
        count += 1

    #Groups all RPM data, in each dataframe, and determines the maximum value in each column
    count = 1
    while count <= numGears:
        key = "roundedDf" + str(count)
        newKey = "roundedGroupedDf" + str(count)

        cf = a[key]
        value = cf.groupby('roundedCurrentRPM').max().reset_index()

        a[newKey] = value
        count += 1

    #Sorts all the data frames by the roundedCurrentRPM and pushes them into a new frame
    count = 1
    while count <= numGears:
        key = "roundedGroupedDf" + str(count)
        newKey = "roundedGroupedSortedDf" + str(count)

        value = a[key].sort_values(by=['roundedCurrentRPM'],ascending=True)

        a[newKey] = value
        count += 1

    #Removes rows from the data frame which have a 0 torque value
    count = 1
    while count <= numGears:
        key = "roundedGroupedSortedDf" + str(count)
        newKey = "roundedGroupedSortedZeroDroppedDf" + str(count)

        value = a[key][a[key]['roundedTorque'] != 0]

        a[newKey] = value
        count += 1

    #Method to run isolation forest on the provided data set to remove outliers from the set
    def remove_outliers_isolation_forest(df, column_name, contamination=0.05):
        # Extract the column data
        column_data = df[column_name].values.reshape(-1, 1)
        
        # Fit the Isolation Forest model
        clf = IsolationForest(contamination=contamination)
        clf.fit(column_data)
        
        # Identify outliers
        outliers = clf.predict(column_data) == -1
        
        # Remove outliers from the DataFrame
        df_clean = df[~outliers]
        
        return df_clean

    #Runs the outliers method above to correct data and push into a new frame
    count = 1
    while count <= numGears:
        key = "roundedGroupedSortedZeroDroppedDf" + str(count)
        newKey = "cleanedDf" + str(count)

        value = remove_outliers_isolation_forest(a[key], 'roundedTorque', contamination=0.1)

        a[newKey] = value
        count += 1

    #Builds power curve plots based polynomial curving
    count = 1
    while count <= numGears:
        key = "cleanedDf" + str(count)

        # Fit a polynomial curve for torque (adjust the degree as needed)
        degree_torque = 2
        coefficients_torque = np.polyfit(a[key]['roundedCurrentRPM'], a[key]['roundedTorque'], degree_torque)
        polynomial_torque = np.poly1d(coefficients_torque)

        # Generate y values for the torque curve fit
        x_values_torque = np.linspace(min(a[key]['roundedCurrentRPM']), max(a[key]['roundedCurrentRPM']), 100)
        y_values_torque = polynomial_torque(x_values_torque)

        # Find max torque and its corresponding RPM
        max_torque_index = np.argmax(y_values_torque)
        max_torque_RPM = x_values_torque[max_torque_index]
        max_torque_value = y_values_torque[max_torque_index]

        # Fit a polynomial curve for power (adjust the degree as needed)
        degree_power = 2
        coefficients_power = np.polyfit(a[key]['roundedCurrentRPM'], a[key]['roundedPower'], degree_power)
        polynomial_power = np.poly1d(coefficients_power)

        # Generate y values for the power curve fit
        x_values_power = np.linspace(min(a[key]['roundedCurrentRPM']), max(a[key]['roundedCurrentRPM']), 100)
        y_values_power = polynomial_power(x_values_power)

        # Find max power and its corresponding RPM
        max_power_index = np.argmax(y_values_power)
        max_power_RPM = x_values_power[max_power_index]
        max_power_value = y_values_power[max_power_index]

        # Plot the data and the curve fits
        plt.figure(figsize=(10, 6))

        #Plots normalized data in a scatter plot format to ensure the curve is close to intended dataset
        plt.scatter(a[key]['roundedCurrentRPM'], a[key]['roundedTorque'], label='Data Points', color='blue')
        plt.scatter(a[key]['roundedCurrentRPM'], a[key]['roundedPower'], label='Power vs RPM plot', color='orange')

        #Plots 
        plt.plot(x_values_torque, y_values_torque, color='red', label=f'Torque Polynomial Fit (Degree {degree_torque})')
        plt.plot(x_values_power, y_values_power, color='green', label=f'Power Polynomial Fit (Degree {degree_power})')

        # Annotate max torque and power points
        plt.annotate(f'Max Torque: {max_torque_value:.2f} at {max_torque_RPM:.2f} RPM',
                    xy=(max_torque_RPM, max_torque_value), xytext=(-50, 30),
                    textcoords='offset points', ha='center', va='center',
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.5'), fontsize=10, color='red')
        plt.annotate(f'Max Power: {max_power_value:.2f} at {max_power_RPM:.2f} RPM',
                    xy=(max_power_RPM, max_power_value), xytext=(-50, -30),
                    textcoords='offset points', ha='center', va='center',
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.5'), fontsize=10, color='green')

        # Set labels and title for the chart
        plt.xlabel('Engine RPM\'s (Rotations Per Minute)')
        plt.ylabel('Torque (ft lbs)/Power (Horsepower)')
        plt.title('Torque and Horsepower Band For Gear ' + str(count))
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.grid(True)

        # Save the plot
        plt.savefig(os.path.join("TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_Gear_" + str(count) + "_PowerAndTorqueCurve_Poly.png"), bbox_inches='tight')
        plt.clf()  # Clear the plot for the next iteration

        count += 1

#Method to build the Torque vs Speed curve file
def processDataForTorqueVsSpeed(carOrdinalID, numGears):
    count = 1
    a = {}

    #Sets all available combinedGear files, for this carID, into unique dataframes
    while count <= numGears:
        key = "df" + str(count)
        path = os.path.join("TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + '_combinedGear_' + str(count) + '_data.csv')
        value = pd.read_csv(path)

        a[key] = value
        count += 1

    #sort the data frames
    count = 1
    while count <= numGears:
        key = "df" + str(count)
        newKey = "sorted_combined_dataframe" + str(count)

        value = a[key].sort_values(by=['Speed'],ascending=True)

        a[newKey] = value
        count += 1

    #Find duplicate rows by speed for each gear
    count = 1
    while count <= numGears:
        key = "sorted_combined_dataframe" + str(count)
        newKey = "duplicate_rows" + str(count)

        value = a[key][a[key].duplicated(subset=['Speed'], keep=False)]

        a[newKey] = value
        count += 1

    #Group all the duplicates together by speed
    count = 1
    while count <= numGears:
        key = "duplicate_rows" + str(count)
        newKey = "groups" + str(count)
        currentFrame = a[key]

        value = currentFrame.groupby('Speed')

        a[newKey] = value
        count += 1

    #Create separate DataFrames for each group
    count = 1
    while count <= numGears:
        key = "groups" + str(count)
        newKey = "duplicate_dfs" + str(count)
        currentFrame = a[key]

        value = [group for _, group in currentFrame]

        a[newKey] = value
        count += 1

    #Build corrected rows with max values from the duplicate groups
    c = {}
    count = 1
    while count <= numGears:
        key = "duplicate_dfs" + str(count)
        key1 = "corrected_rows" + str(count)
        c[key1] = []
        currentDuplicateFrame = a[key]
        currentCorrectedFrame = c[key1]
        rowCount = 0
        
        while rowCount < len(currentDuplicateFrame):
            cf = currentDuplicateFrame[rowCount]
            try:
                maxRoundedTorque = round(cf['Torque'].max())
            except:
                maxRoundedTorque = 0
            
            try:
                maxRoundedPower = round(cf['Power'].max())
            except:
                maxRoundedPower = 0

            maxSpeed = cf['Speed'].max()
            maxPower = cf['Power'].max()
            maxBoost = cf['Boost'].max()
            maxTorque = cf['Torque'].max()
            maxCurrentRPM = cf['EngineCurrentRPM'].max()

            if maxCurrentRPM is None:
                maxCurrentRPM = 0

            try:
                maxCurrentRPMRounded = round(maxCurrentRPM)
            except:
                maxCurrentRPMRounded = 0
            
            currentCorrectedFrame.append({'Timestamp': '1/31/2024 01:00:01','CarOrdinalID': cf['CarOrdinalID'].max(),'CarClass': cf['CarClass'].max(),'CarPerformanceIndex': cf['CarPerformanceIndex'].max(),'DriveTrainType': cf['DriveTrainType'].max(),'NumCylinders': cf['NumCylinders'].max(),'EngineMaxRPM': cf['EngineMaxRPM'].max(),'EngineIdleRPM': cf['EngineIdleRPM'].max(),'EngineCurrentRPM': maxCurrentRPM,'Speed': maxSpeed,'Power': maxPower,'Torque': maxTorque,'Boost': maxBoost,'Gear': cf['Gear'].max(),'Accel': 0,'Brake': 0,'Clutch': 0,'HandBrake': 0,'Fuel': 0,'roundedCurrentRPM': maxCurrentRPMRounded,'roundedPower': maxRoundedPower,'roundedTorque': maxRoundedTorque})
            rowCount += 1

        c[key1] = currentCorrectedFrame
        count += 1

    #Remove duplicate rows from the original data set
    count = 1
    while count <= numGears:
        key = "sorted_combined_dataframe" + str(count)
        newKey = "df_cleaned" + str(count)

        value = a[key].drop_duplicates(subset='Speed', keep=False)

        a[newKey] = value
        count += 1

    #Sets the corrected rows arrays into a data frame
    count = 1
    while count <= numGears:
        key = "corrected_rows" + str(count)
        newKey = "df_corrected_rows" + str(count)

        value = pd.DataFrame(c[key])

        c[newKey] = value
        count += 1

    #Appends corrected rows back to the data set
    count = 1
    while count <= numGears:
        key = "df_cleaned" + str(count)
        key1 = "df_corrected_rows" + str(count)
        newKey = "combined_dataframe" + str(count)

        frame1 = a[key]
        frame2 = c[key1]
        value = pd.concat([a[key],c[key1]], ignore_index=True)

        a[newKey] = value
        count += 1

    #Sort the dataframes by speed
    count = 1
    while count <= numGears:
        key = "combined_dataframe" + str(count)
        newKey = "sorted_combined_dataframe" + str(count)

        value = a[key].sort_values(by=['Speed'])

        a[newKey] = value
        count += 1

    #Removes rows where torque is showing as 0
    count = 1
    while count <= numGears:
        key = "sorted_combined_dataframe" + str(count)
        newKey = "sorted_combined_dataframe" + str(count)

        value = a[key][a[key]['roundedTorque'] != 0]

        a[newKey] = value
        count += 1

    #Removes rows where speed is showing as 0
    count = 1
    while count <= numGears:
        key = "sorted_combined_dataframe" + str(count)
        newKey = "sorted_combined_dataframe" + str(count)

        value = a[key][a[key]['Speed'] != 0]

        a[newKey] = value
        count += 1

    #Removes rows where RPM is showing as 0
    count = 1
    while count <= numGears:
        key = "sorted_combined_dataframe" + str(count)
        newKey = "sorted_combined_dataframe" + str(count)

        value = a[key][a[key]['roundedCurrentRPM'] != 0]

        a[newKey] = value
        count += 1

    # Define the quadratic function to fit the data
    def quadratic_func(x, a, b, c):
        return a * x**2 + b * x + c

    # Define function to find intersection points of two quadratic functions
    def find_intersection(a1, b1, c1, a2, b2, c2, x_min, x_max):
        # Define the coefficients of the quadratic equation: (a1 - a2)x^2 + (b1 - b2)x + (c1 - c2) = 0
        coeff_a = a1 - a2
        coeff_b = b1 - b2
        coeff_c = c1 - c2
        
        # Find the roots of the quadratic equation within the specified range
        roots = np.roots([coeff_a, coeff_b, coeff_c])
        return [root for root in roots if x_min <= root <= x_max]
    
    #Used as an array to allow different colors in the mathlib plotting sections
    colorList = ['red','blue','green','purple','orange','brown','black','olive','cyan','pink']

    # Sample data for the y-axis
    plotData = {}
    count = 1
    while count <= numGears:
        key = "sorted_combined_dataframe" + str(count)
        newKey = "y_data" + str(count)

        value = np.array(a[key]['roundedTorque'])

        plotData[newKey] = value
        count += 1

    #Checks y axis data to ensure there are more than 3 plots as this is the minimum for the function to work
    count = 1
    validGearData = []
    while count <= numGears:
        newKey = "y_data" + str(count)
        if len(plotData[newKey]) > 2:
            validGearData.append(count)
        else:
            print("Not enough data available in gear " + str(count) + " data for proper mapping.")
        count += 1

    # Fit the quadratic function to the data using curve_fit
    count = 0
    validGears = len(validGearData)
    while count < validGears:
        key = "sorted_combined_dataframe" + str(validGearData[count])
        key1 = "y_data" + str(validGearData[count])
        newKey = "popt" + str(validGearData[count])

        value = curve_fit(quadratic_func, a[key]['Speed'], plotData[key1])

        plotData[newKey] = value[0]
        count += 1

    #Plot quadratic curves without intersection points/data
    plt.figure()
    count = 0
    while count < validGears: #Should be <= but removed because 7th gear is erroring currently
        key = "sorted_combined_dataframe" + str(validGearData[count])
        key1 = "popt" + str(validGearData[count])

        plt.plot(a[key]['Speed'], quadratic_func(a[key]['Speed'], *plotData[key1]), label='Quadratic fit gear ' + str(validGearData[count]) + ' torque vs speed curve', color=colorList[count])
        count += 1

    plt.xlabel('Speed in MPH (Miles Per Hour)')
    plt.ylabel('Torque (ft lbs)')
    plt.title('Torque vs Speed Curve Per Gear wo/Intersection Points')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.savefig(os.path.join("TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_TorquePerGearOverSpeed.png"), bbox_inches='tight')

    #Clears the current plot
    plt.clf()

    #Plot quadratic curves with intersection points/data
    count = 0
    intersection_points = []

    while count < validGears:  # Limiting to adjacent pairs
        if count + 1 < validGears:
            key = "sorted_combined_dataframe" + str(validGearData[count])
            key1 = "popt" + str(validGearData[count])
            key_next = "sorted_combined_dataframe" + str(validGearData[count + 1])
            key1_next = "popt" + str(validGearData[count + 1])

            # Plot quadratic curve
            plt.plot(a[key]['Speed'], quadratic_func(a[key]['Speed'], *plotData[key1]),
                    label='Quadratic fit gear ' + str(validGearData[count]) + ' torque vs speed curve',
                    color=colorList[count])
            
            # Find intersection points with the next curve
            a1, b1, c1 = plotData[key1]
            a2, b2, c2 = plotData[key1_next]
            
            # Define the range of x values for intersection points
            x_min = min(a[key]['Speed'])
            x_max = max(a[key_next]['Speed'])
            
            intersection = find_intersection(a1, b1, c1, a2, b2, c2, x_min, x_max)
            
            # Plot intersection points and store x, y values
            for x in intersection:
                y = quadratic_func(x, a1, b1, c1)
                plt.plot(x, y, 'ro')  # Plot intersection point
                intersection_points.append((x, y))

                # Annotate intersection points with their coordinates
                plt.annotate(f'({x:.2f}, {y:.2f})', (x, y), textcoords="offset points", xytext=(0,10), va='top', ha='center', fontsize=6, color='red')
            
            count += 1
        else:
            key = "sorted_combined_dataframe" + str(validGearData[count])
            key1 = "popt" + str(validGearData[count])

            # Plot quadratic curve
            plt.plot(a[key]['Speed'], quadratic_func(a[key]['Speed'], *plotData[key1]),
                    label='Quadratic fit gear ' + str(validGearData[count]) + ' torque vs speed curve',
                    color=colorList[count])
            
            break

    plt.xlabel('Speed in MPH (Miles Per Hour)')
    plt.ylabel('Torque (ft lbs)')
    plt.title('Torque vs Speed Curve Per Gear w/Intersection Points')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.savefig(os.path.join("TelemDataFiles", str(carOrdinalID),  str(carOrdinalID) + "_TorquePerGearOverSpeed_wIntersections.png"), bbox_inches='tight')

    #Clears the current plot
    plt.clf()

    #Uses previously found intersection data to set optimal shift points data into an array
    count = 0
    intersection_pointsLEN = len(intersection_points)
    shiftPoints = {}

    while count < intersection_pointsLEN:
        newKey = "gear_" + str(validGearData[count]) + "_MPH_ShiftPoint"
        newKey1 = "gear_" + str(validGearData[count]) + "_TORQUE_ShiftPoint"
        newKey2 = "gear_" + str(validGearData[count]) + "_Rounded_MPH_ShiftPoint"
        newKey3 = "gear_" + str(validGearData[count]) + "_Rounded_TORQUE_ShiftPoint"

        mphValue = intersection_points[count][0]
        torqueValue = intersection_points[count][1]

        shiftPoints[newKey] = mphValue
        shiftPoints[newKey1] = torqueValue
        shiftPoints[newKey2] = round(mphValue)
        shiftPoints[newKey3] = round(torqueValue)

        count += 1

    print(shiftPoints)

#Method to build the RPM vs Speed linear regression file
def processDataForRPMVsSpeed(carOrdinalID, numGears):
    count = 1
    a = {}
    colorList = ['red','blue','green','purple','orange','brown','black','olive','cyan','pink']

    #Grab relevant files and push them into data frames under the dictionary a
    while count <= numGears:
        key = "df" + str(count)
        path = os.path.join('TelemDataFiles', str(carOrdinalID), str(carOrdinalID) + '_combinedGear_' + str(count) + '_data.csv')
        value = pd.read_csv(path)

        a[key] = value
        count += 1
    
    #sort the data frames contained in the dictionary a
    count = 1
    while count <= numGears:
        key = "df" + str(count)
        newKey = "sorted_combined_dataframe" + str(count)

        value = a[key].sort_values(by=['Speed'],ascending=True)

        a[newKey] = value
        count += 1

    #Removes rows where speed is showing as 0
    count = 1
    while count <= numGears:
        key = "sorted_combined_dataframe" + str(count)
        newKey = "sorted_combined_dataframe" + str(count)

        value = a[key][a[key]['Speed'] != 0]

        a[newKey] = value
        count += 1

    #Removes rows where RPM is showing as 0
    count = 1
    while count <= numGears:
        key = "sorted_combined_dataframe" + str(count)
        newKey = "sorted_combined_dataframe" + str(count)

        value = a[key][a[key]['roundedCurrentRPM'] != 0]

        a[newKey] = value
        count += 1

    # Function to calculate maximum value of y-axis in a dataset
    def calculate_max_y(dataframes):
        max_y_values = []
        for key, dataframe in dataframes.items():
            max_y_values.append(dataframe['roundedCurrentRPM'].max())
        return max(max_y_values)

    #Starts plotting of data
    plt.figure()
    count = 1
    while count <= numGears:
        key = "sorted_combined_dataframe" + str(count)
        labelValue = 'Gear ' + str(count) + ' Engine RPM vs Speed'
        
        #Scatter plot underlay option available if original data is needed
        #plt.scatter(a[key]['Speed'], a[key]['roundedCurrentRPM'], label=labelValue)

        # Linear regression to get best fit line
        slope, intercept, r_value, p_value, std_err = stats.linregress(a[key]['Speed'], a[key]['roundedCurrentRPM'])
        newLabelValue = 'Gear ' + str(count) + ' Linear Best Fit Engine RPM vs Speed Line'

        # Calculate maximum y-value in the dataset
        max_y_value = a[key]['roundedCurrentRPM'].max()

        # Calculate corresponding x-value where regression line reaches max_y_value
        max_y_index = np.argmax(a[key]['roundedCurrentRPM'])
        x_value_at_max_y = a[key]['Speed'].iloc[max_y_index]

        # Clip the regression line to not exceed max_y_value
        clipped_x_values = np.clip(a[key]['Speed'], None, x_value_at_max_y)
        clipped_y_values = intercept + slope * clipped_x_values

        plt.plot(clipped_x_values, clipped_y_values, color=colorList[count - 1], label=newLabelValue)

        # Annotate the maximum value of each line
        plt.text(clipped_x_values.max(), clipped_y_values.max(), f'Max: {clipped_y_values.max():.2f}', fontsize=8, color=colorList[count - 1], ha='right', va='bottom')

        count += 1

    plt.xlabel('Speed in MPH (Miles Per Hour)')
    plt.ylabel("Engine RPM's (Rotations Per Minute)")
    plt.title('Engine RPM vs Speed for Each Gear')
    plt.grid(True)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.savefig(os.path.join("TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_RPMvSpeed.png"), bbox_inches='tight')
    #plt.show()
    #Clears the current plot
    plt.clf()

'''Start main block to trigger methods and menu system'''

#Define variables
captureFile = os.getcwd() + '\\TelemDataFiles\\logTelemetry.csv'
df = pd.read_csv(captureFile)
gearCounter = 1

#Checks df for a carID within the file to use !!Warning this will break if more than one carID is present in the log file!!
if df['CarOrdinalID'].max() != None:
    carOrdinalID = df['CarOrdinalID'].max()
    print(carOrdinalID)
else:
    carOrdinalID = input("What is the carOrdinalID for the car?")
if df['Gear'].max() != None:
    numGears = df['Gear'].max()
    print(numGears)
else:
    numGears = input("How many gears does the car have?")
#numGears = 7
#carOrdinalID = 3655 #Used to build files unique to the car

#Add pause for user input y/delete files previously generated by this class n/continue with warning data may be skewed
user_input = input("Have you ever generated telem data for this car?")

if user_input.lower() == "yes" or user_input.lower() == "y" or user_input.lower() == "ys":
    next_input = input("Have you made any performance or tuning updates to the car since the last run?")
    
    if next_input.lower() == "yes" or next_input.lower() == "y" or next_input.lower() == "ys":
        print("It's recommended that you wipe previously existing data before running this process or data may become skewed, unless its the same car with the same performance index.")
        next_input = input("Please confirm that you would like to delete previous data.")
        
        if next_input.lower() == "yes" or next_input.lower() == "y" or next_input.lower() == "ys":
            #delete old files before continuing
            print("Starting process for deleting old data files.")
            deletePreviousData(numGears, carOrdinalID)
            time.sleep(5)

            #Build files for each gear
            gearPullBuilder(numGears, captureFile, carOrdinalID)

            #itterates through the created gear files to build new copies with normalized and sorted data
            while gearCounter <= numGears:
                #fileName = "TelemDataFiles\Gear_" + str(gearCounter) + "_data.csv"
                fileName = os.path.join("TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_Gear_" + str(gearCounter) + "_data.csv")
                duplicateRPMNormalizer(fileName, gearCounter,carOrdinalID)
                powerCurvePlotter(fileName, df.EngineMaxRPM.max(), gearCounter, carOrdinalID)
                gearCounter = gearCounter + 1
            
            altPowerCurvePlotter(carOrdinalID, numGears)
            processDataForTorqueVsSpeed(carOrdinalID, numGears)
            processDataForRPMVsSpeed(carOrdinalID, numGears)
        elif next_input.lower() == "no" or next_input.lower() == "n":
            print("It's recommended that you wipe previously existing data before running this process or data may become skewed, unless its the same car with the same performance index.")
            next_input = input("Please confirm that you would like to delete previous data.")

            if next_input.lower() == "yes" or next_input.lower() == "y" or next_input.lower() == "ys":
                #delete old files before continuing
                print("Starting process for deleting old data files.")
                deletePreviousData(numGears, carOrdinalID)
                time.sleep(5)

                #Build files for each gear
                gearPullBuilder(numGears, captureFile, carOrdinalID)

                #itterates through the created gear files to build new copies with normalized and sorted data
                while gearCounter <= numGears:
                    fileName = os.path.join("TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_Gear_" + str(gearCounter) + "_data.csv")
                    duplicateRPMNormalizer(fileName, gearCounter,carOrdinalID)
                    powerCurvePlotter(fileName, df.EngineMaxRPM.max(), gearCounter, carOrdinalID)
                    gearCounter = gearCounter + 1
                
                altPowerCurvePlotter(carOrdinalID, numGears)
                processDataForTorqueVsSpeed(carOrdinalID, numGears)
                processDataForRPMVsSpeed(carOrdinalID, numGears)
            elif next_input.lower() == "no" or next_input.lower() == "n":
                #continue into process
                print("Continuing process since user opted to not delete previous data. This behavior is still untested and may cause eratic file behaviors")

                #Build files for each gear
                gearPullBuilder(numGears,captureFile,carOrdinalID)

                #itterates through the created gear files to build new copies with normalized and sorted data
                while gearCounter <= numGears:
                    fileName = os.path.join("TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_Gear_" + str(gearCounter) + "_data.csv")
                    duplicateRPMNormalizer(fileName, gearCounter, carOrdinalID)
                    powerCurvePlotter(fileName, df.EngineMaxRPM.max(), gearCounter, carOrdinalID)
                    gearCounter = gearCounter + 1

                altPowerCurvePlotter(carOrdinalID, numGears)
                processDataForTorqueVsSpeed(carOrdinalID, numGears)
                processDataForRPMVsSpeed(carOrdinalID, numGears)
    elif next_input.lower() == "no" or next_input.lower() == "n":
        #continue into process
        print("Continuing process since car and performance index are the same. This behavior is still untested and may cause eratic file behaviors")

        #Build files for each gear
        gearPullBuilder(numGears, captureFile, carOrdinalID)

        #itterates through the created gear files to build new copies with normalized and sorted data
        while gearCounter <= numGears:
            fileName = os.path.join("TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_Gear_" + str(gearCounter) + "_data.csv")
            duplicateRPMNormalizer(fileName, gearCounter, carOrdinalID)
            powerCurvePlotter(fileName, df.EngineMaxRPM.max(), gearCounter, carOrdinalID)
            gearCounter = gearCounter + 1

        altPowerCurvePlotter(carOrdinalID, numGears)
        processDataForTorqueVsSpeed(carOrdinalID, numGears)
        processDataForRPMVsSpeed(carOrdinalID, numGears)
    else:
        print("Invalid input.")
        #break
elif user_input.lower() == "no" or user_input.lower() == "n":
    print("Continuing process since this car has yet to be analyzed")
    #Build files for each gear
    gearPullBuilder(numGears, captureFile, carOrdinalID)

    #itterates through the created gear files to build new copies with normalized and sorted data
    while gearCounter <= numGears:
        fileName = os.path.join("TelemDataFiles", str(carOrdinalID), str(carOrdinalID) + "_Gear_" + str(gearCounter) + "_data.csv")
        duplicateRPMNormalizer(fileName, gearCounter, carOrdinalID)
        powerCurvePlotter(fileName, df.EngineMaxRPM.max(), gearCounter, carOrdinalID)
        gearCounter = gearCounter + 1

    altPowerCurvePlotter(carOrdinalID, numGears)
    processDataForTorqueVsSpeed(carOrdinalID, numGears)
    processDataForRPMVsSpeed(carOrdinalID, numGears)
else:
    print("Invalid input.")