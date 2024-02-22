import csv
import os
from pathlib import Path
from datetime import datetime
import pandas as pd

#Creates blank table containing header
def createHeaderCSV(file_name):
    data = [
    ["CarOrdinalID", "CarFriendlyName", "CarMake", "CarModel", "CarManYear", "CarClass", "CarPerformanceIndex", "DriveTrainType", "NumCylinders", "EngineMaxRPM", "EngineIdleRPM", "Gears", "FinalDriveRatio", "Ratio1", "Ratio2", "Ratio3", "Ratio4", "Ratio5", "Ratio6", "Ratio7", "Ratio8", "Ratio9", "Ratio10", "mphShiftPoint1", "torqueShiftPoint1", "rpmShiftPoint1", "mphShiftPoint2", "torqueShiftPoint2", "rpmShiftPoint2", "mphShiftPoint3", "torqueShiftPoint3", "rpmShiftPoint3", "mphShiftPoint4", "torqueShiftPoint4", "rpmShiftPoint4", "mphShiftPoint5", "torqueShiftPoint5", "rpmShiftPoint5", "mphShiftPoint6", "torqueShiftPoint6", "rpmShiftPoint6", "mphShiftPoint7", "torqueShiftPoint7", "rpmShiftPoint7", "mphShiftPoint8", "torqueShiftPoint8", "rpmShiftPoint8", "mphShiftPoint9", "torqueShiftPoint9", "rpmShiftPoint9", "mphShiftPoint10", "torqueShiftPoint10", "rpmShiftPoint10", "LastModified"],
    ]
    
    # Writing to the CSV file
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(data[0])

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
            if int(row[search_column_index]) == int(search_term):
                return reader.line_num
        
    return None

#Creates a folder in the telemDataFile folder for storage of telem data
def createTelemDataFileDirectoryForCar(CarOrdinalID):
    file_path = "E:\\Code Projects\\Forza_telemetry_project-develop\\Forza_telemetry_project-develop\\TelemDataFiles\\" + str(CarOrdinalID)

    if os.path.exists(file_path):
        print(f"Directory '{file_path}' found.")
    else:
        print(f"Directory '{file_path}' doesn\'t exist.")
        os.makedirs(file_path)
        print(f"Directory '{file_path}' created.")

#Method for creating a new entry for a car that hasn't existed before by manual input
def addNewCarByManualInputWithoutGearInfoInput(CarOrdinalID, file_name):
    # Create a Path object
    file_path_obj = Path(file_name)

    if file_path_obj.is_file():
        print(f'The file "{file_name}" exists.')
    else:
        createHeaderCSV(file_name)
        
    #Sets search term for searching CSV file for match
    search_term = CarOrdinalID  

    #Runs search_csv method and returns row value if matched
    result = search_csv(file_name, search_term)

    if result:
        print('Existing match for this car already found, please use an alternate method to update the car\'s information.')

        #Runs check to ensure telem folder is present and will do nothing if folder already exists
        createTelemDataFileDirectoryForCar(CarOrdinalID)
    else:
        print(f'No match found for {"CarOrdinalID: " + str(search_term)}.')

        CarFriendlyName = input("What is the cars friendly name?")
        CarMake = input("What is the cars make?")
        CarModel = input("What is the cars model?")
        CarManYear = input("What is the cars manufacturing year?")
        CarClass = input("What is the cars class? Between 0 (D -- worst cars) and 7 (X class -- best cars)")
        CarPerformanceIndex = input("What is the cars performance index? Between 100 (worst car) and 999 (best car) inclusive")
        DriveTrainType = input("What is the cars drivetrain type? (0 = FWD, 1 = RWD, 2 = AWD)")
        NumCylinders = input("What is the cars number of cylinders in the engine?")
        EngineMaxRPM = input("What is the cars maximum engine RPM limit? (Provide full value not x1000 value)")
        EngineIdleRPM = input("What is the cars idle engine RPM value")
        Gears = input("What is the cars number of gears?")

        #Sets default None values to add to the entry
        FinalDriveRatio = None
        Ratio1 = None
        Ratio2 = None
        Ratio3 = None
        Ratio4 = None
        Ratio5 = None
        Ratio6 = None
        Ratio7 = None
        Ratio8 = None
        Ratio9 = None
        Ratio10 = None
        mphShiftPoint1 = None
        torqueShiftPoint1 = None
        rpmShiftPoint1 = None
        mphShiftPoint2 = None
        torqueShiftPoint2 = None
        rpmShiftPoint2 = None
        mphShiftPoint3 = None
        torqueShiftPoint3 = None
        rpmShiftPoint3 = None
        mphShiftPoint4 = None
        torqueShiftPoint4 = None
        rpmShiftPoint4 = None
        mphShiftPoint5 = None
        torqueShiftPoint5 = None
        rpmShiftPoint5 = None
        mphShiftPoint6 = None
        torqueShiftPoint6 = None
        rpmShiftPoint6 = None
        mphShiftPoint7 = None
        torqueShiftPoint7 = None
        rpmShiftPoint7 = None
        mphShiftPoint8 = None
        torqueShiftPoint8 = None
        rpmShiftPoint8 = None
        mphShiftPoint9 = None
        torqueShiftPoint9 = None
        rpmShiftPoint9 = None
        mphShiftPoint10 = None
        torqueShiftPoint10 = None
        rpmShiftPoint10 = None

        #Sets values into an array before adding to CSV
        data = [
            CarOrdinalID,CarFriendlyName,CarMake,CarModel,CarManYear,CarClass,CarPerformanceIndex,DriveTrainType,NumCylinders,EngineMaxRPM,EngineIdleRPM,Gears,FinalDriveRatio,Ratio1,Ratio2,Ratio3,Ratio4,Ratio5,Ratio6,Ratio7,Ratio8,Ratio9,Ratio10,mphShiftPoint1,torqueShiftPoint1,rpmShiftPoint1,mphShiftPoint2,torqueShiftPoint2,rpmShiftPoint2,mphShiftPoint3, torqueShiftPoint3,rpmShiftPoint3,mphShiftPoint4,torqueShiftPoint4,rpmShiftPoint4,mphShiftPoint5,torqueShiftPoint5,rpmShiftPoint5,mphShiftPoint6,torqueShiftPoint6,rpmShiftPoint6, mphShiftPoint7,torqueShiftPoint7,rpmShiftPoint7,mphShiftPoint8,torqueShiftPoint8,rpmShiftPoint8,mphShiftPoint9,torqueShiftPoint9,rpmShiftPoint9,mphShiftPoint10,torqueShiftPoint10,rpmShiftPoint10,str(datetime.now())
        ]

        # Writing to the CSV file
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write the data to the next available row
            writer.writerow(data)

            file.close

        #Runs check to ensure telem folder is present and will do nothing if folder already exists
        createTelemDataFileDirectoryForCar(CarOrdinalID)

#Method for creating a new entry for a car that hasn't existed before by pulling data from logTelemtry
def addNewCarByReadingTelemtry(file_name, telemPath):
    question = input("Please confirm that that there is only 1 car\'s data in the logTelemetry file?")

    if question.lower() == "yes" or question.lower() == "y":
        print("Continuing process")
        # Create a Path object
        file_path_obj = Path(file_name)
        file_path_obj2 = Path(telemPath)

        if file_path_obj.is_file():
            print(f'The file "{file_name}" exists.')
        else:
            createHeaderCSV(file_name)

        if file_path_obj2.is_file():
            df = pd.read_csv(telemPath)
            #Gets row data for the matching car ID
            CarOrdinalID = df['CarOrdinalID'].iloc[0].max()
            CarClass = df['CarClass'].iloc[0].max()
            CarPerformanceIndex = df['CarPerformanceIndex'].iloc[0].max()
            DriveTrainType = df['DriveTrainType'].iloc[0].max()
            NumCylinders = df['NumCylinders'].iloc[0].max()
            EngineMaxRPM = round(df['EngineMaxRPM'].iloc[0].max())
            EngineIdleRPM = round(df['EngineIdleRPM'].iloc[0].max())
            Gears = df['Gear'].iloc[0].max()

            #Sets default None values to add to the entry
            CarFriendlyName = None
            CarMake = None
            CarModel = None
            CarManYear = None
            FinalDriveRatio = None
            Ratio1 = None
            Ratio2 = None
            Ratio3 = None
            Ratio4 = None
            Ratio5 = None
            Ratio6 = None
            Ratio7 = None
            Ratio8 = None
            Ratio9 = None
            Ratio10 = None
            mphShiftPoint1 = None
            torqueShiftPoint1 = None
            rpmShiftPoint1 = None
            mphShiftPoint2 = None
            torqueShiftPoint2 = None
            rpmShiftPoint2 = None
            mphShiftPoint3 = None
            torqueShiftPoint3 = None
            rpmShiftPoint3 = None
            mphShiftPoint4 = None
            torqueShiftPoint4 = None
            rpmShiftPoint4 = None
            mphShiftPoint5 = None
            torqueShiftPoint5 = None
            rpmShiftPoint5 = None
            mphShiftPoint6 = None
            torqueShiftPoint6 = None
            rpmShiftPoint6 = None
            mphShiftPoint7 = None
            torqueShiftPoint7 = None
            rpmShiftPoint7 = None
            mphShiftPoint8 = None
            torqueShiftPoint8 = None
            rpmShiftPoint8 = None
            mphShiftPoint9 = None
            torqueShiftPoint9 = None
            rpmShiftPoint9 = None
            mphShiftPoint10 = None
            torqueShiftPoint10 = None
            rpmShiftPoint10 = None

            #Sets values into an array before adding to CSV
            data = [
                CarOrdinalID,CarFriendlyName,CarMake,CarModel,CarManYear,CarClass,CarPerformanceIndex,DriveTrainType,NumCylinders,EngineMaxRPM,EngineIdleRPM,Gears,FinalDriveRatio,Ratio1,Ratio2,Ratio3,Ratio4,Ratio5,Ratio6,Ratio7,Ratio8,Ratio9,Ratio10,mphShiftPoint1,torqueShiftPoint1,rpmShiftPoint1,mphShiftPoint2,torqueShiftPoint2,rpmShiftPoint2,mphShiftPoint3, torqueShiftPoint3,rpmShiftPoint3,mphShiftPoint4,torqueShiftPoint4,rpmShiftPoint4,mphShiftPoint5,torqueShiftPoint5,rpmShiftPoint5,mphShiftPoint6,torqueShiftPoint6,rpmShiftPoint6, mphShiftPoint7,torqueShiftPoint7,rpmShiftPoint7,mphShiftPoint8,torqueShiftPoint8,rpmShiftPoint8,mphShiftPoint9,torqueShiftPoint9,rpmShiftPoint9,mphShiftPoint10,torqueShiftPoint10,rpmShiftPoint10,str(datetime.now())
            ]

            # Writing to the CSV file
            with open(file_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                
                # Write the data to the next available row
                writer.writerow(data)

                file.close

            #Runs check to ensure telem folder is present and will do nothing if folder already exists
            createTelemDataFileDirectoryForCar(CarOrdinalID)
        else:
            print("Telem data file not found.")
    else:
        print("This method is only intended to be run when one car is present in the dataset. Please add the car manually or remove data from the logTelemetry file")

#Method for updating all values on an existing car
def updateCarAllValuesManually(CarOrdinalID, file_name):
    # Create a Path object
    file_path_obj = Path(file_name)

    if file_path_obj.is_file():
        print(f'The file "{file_name}" exists.')

        #Sets search term for searching CSV file for match
        search_term = CarOrdinalID  

        #Runs search_csv method and returns row value if matched
        result = search_csv(file_name, search_term)

        if result:
            print("Confirmed car exists in DB starting questions.")

            CarFriendlyName = input("What is the cars friendly name?")
            CarMake = input("What is the cars make?")
            CarModel = input("What is the cars model?")
            CarManYear = input("What is the cars manufacturing year?")
            CarClass = input("What is the cars class? Between 0 (D -- worst cars) and 7 (X class -- best cars)")
            CarPerformanceIndex = input("What is the cars performance index? Between 100 (worst car) and 999 (best car) inclusive")
            DriveTrainType = input("What is the cars drivetrain type? (0 = FWD, 1 = RWD, 2 = AWD)")
            NumCylinders = input("What is the cars number of cylinders in the engine?")
            EngineMaxRPM = input("What is the cars maximum engine RPM limit? (Provide full value not x1000 value)")
            EngineIdleRPM = input("What is the cars idle engine RPM value")
            Gears = input("What is the cars number of gears?")
            FinalDriveRatio = input("What is the cars final drive ratio? (If unknown or NA fill as None)")
            Ratio1 = input("What is the cars 1st gear ratio? (If unknown or NA fill as None)")
            Ratio2 = input("What is the cars 2nd gear ratio? (If unknown or NA fill as None)")
            Ratio3 = input("What is the cars 3rd gear ratio? (If unknown or NA fill as None)")
            Ratio4 = input("What is the cars 4th gear ratio? (If unknown or NA fill as None)")
            Ratio5 = input("What is the cars 5th gear ratio? (If unknown or NA fill as None)")
            Ratio6 = input("What is the cars 6th gear ratio? (If unknown or NA fill as None)")
            Ratio7 = input("What is the cars 7th gear ratio? (If unknown or NA fill as None)")
            Ratio8 = input("What is the cars 8th gear ratio? (If unknown or NA fill as None)")
            Ratio9 = input("What is the cars 9th gear ratio? (If unknown or NA fill as None)")
            Ratio10 = input("What is the cars 10th gear ratio?")
            mphShiftPoint1 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            torqueShiftPoint1 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            rpmShiftPoint1 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            mphShiftPoint2 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            torqueShiftPoint2 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            rpmShiftPoint2 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            mphShiftPoint3 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            torqueShiftPoint3 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            rpmShiftPoint3 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            mphShiftPoint4 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            torqueShiftPoint4 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            rpmShiftPoint4 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            mphShiftPoint5 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            torqueShiftPoint5 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            rpmShiftPoint5 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            mphShiftPoint6 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            torqueShiftPoint6 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            rpmShiftPoint6 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            mphShiftPoint7 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            torqueShiftPoint7 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            rpmShiftPoint7 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            mphShiftPoint8 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            torqueShiftPoint8 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            rpmShiftPoint8 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            mphShiftPoint9 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            torqueShiftPoint9 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            rpmShiftPoint9 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            mphShiftPoint10 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            torqueShiftPoint10 = input("What is the cars number of gears? (If unknown or NA fill as None)")
            rpmShiftPoint10 = input("What is the cars number of gears? (If unknown or NA fill as None)")

            #Sets values into an array before adding to CSV
            data = [
                CarOrdinalID,CarFriendlyName,CarMake,CarModel,CarManYear,CarClass,CarPerformanceIndex,DriveTrainType,NumCylinders,EngineMaxRPM,EngineIdleRPM,Gears,FinalDriveRatio,Ratio1,Ratio2,Ratio3,Ratio4,Ratio5,Ratio6,Ratio7,Ratio8,Ratio9,Ratio10,mphShiftPoint1,torqueShiftPoint1,rpmShiftPoint1,mphShiftPoint2,torqueShiftPoint2,rpmShiftPoint2,mphShiftPoint3, torqueShiftPoint3,rpmShiftPoint3,mphShiftPoint4,torqueShiftPoint4,rpmShiftPoint4,mphShiftPoint5,torqueShiftPoint5,rpmShiftPoint5,mphShiftPoint6,torqueShiftPoint6,rpmShiftPoint6, mphShiftPoint7,torqueShiftPoint7,rpmShiftPoint7,mphShiftPoint8,torqueShiftPoint8,rpmShiftPoint8,mphShiftPoint9,torqueShiftPoint9,rpmShiftPoint9,mphShiftPoint10,torqueShiftPoint10,rpmShiftPoint10,str(datetime.now())
            ]

            #Reads database and extracts all values into a list
            with open(file_name, mode='r') as file:
                # Read the existing CSV data
                csv_data = list(csv.reader(file))
                file.close

            #Sets the required index in the list to the data created earlier
            csv_data[result-1] = data

            #Pushes the updated list back into the csv
            with open(file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(csv_data)
                file.close

            print("Car information updated in database.")
        else:
            print("Car doesn't already exist in the database. Please add it and then re-run this method")
    else:
        createHeaderCSV(file_name)
        print("Car doesn't already exist in the database. Please add it and then re-run this method")

#Method for updating all values on an existing car by being passed the values in the method head
def updateCarAllValuesViaMethodInput(file_name,CarOrdinalID,CarFriendlyName,CarMake,CarModel,CarManYear,CarClass,CarPerformanceIndex,DriveTrainType,NumCylinders,EngineMaxRPM,EngineIdleRPM,Gears,FinalDriveRatio,Ratio1,Ratio2,Ratio3,Ratio4,Ratio5,Ratio6,Ratio7,Ratio8,Ratio9,Ratio10,mphShiftPoint1,torqueShiftPoint1,rpmShiftPoint1,mphShiftPoint2,torqueShiftPoint2,rpmShiftPoint2,mphShiftPoint3, torqueShiftPoint3,rpmShiftPoint3,mphShiftPoint4,torqueShiftPoint4,rpmShiftPoint4,mphShiftPoint5,torqueShiftPoint5,rpmShiftPoint5,mphShiftPoint6,torqueShiftPoint6,rpmShiftPoint6, mphShiftPoint7,torqueShiftPoint7,rpmShiftPoint7,mphShiftPoint8,torqueShiftPoint8,rpmShiftPoint8,mphShiftPoint9,torqueShiftPoint9,rpmShiftPoint9,mphShiftPoint10,torqueShiftPoint10,rpmShiftPoint10):
    # Create a Path object
    file_path_obj = Path(file_name)

    if file_path_obj.is_file():
        print(f'The file "{file_name}" exists.')
    
        #Sets search term for searching CSV file for match
        search_term = CarOrdinalID  

        #Runs search_csv method and returns row value if matched
        result = search_csv(file_name, search_term)

        if result:
            print("Confirmed car exists in DB starting questions.")

            #Sets values into an array before adding to CSV
            data = [
                CarOrdinalID,CarFriendlyName,CarMake,CarModel,CarManYear,CarClass,CarPerformanceIndex,DriveTrainType,NumCylinders,EngineMaxRPM,EngineIdleRPM,Gears,FinalDriveRatio,Ratio1,Ratio2,Ratio3,Ratio4,Ratio5,Ratio6,Ratio7,Ratio8,Ratio9,Ratio10,mphShiftPoint1,torqueShiftPoint1,rpmShiftPoint1,mphShiftPoint2,torqueShiftPoint2,rpmShiftPoint2,mphShiftPoint3, torqueShiftPoint3,rpmShiftPoint3,mphShiftPoint4,torqueShiftPoint4,rpmShiftPoint4,mphShiftPoint5,torqueShiftPoint5,rpmShiftPoint5,mphShiftPoint6,torqueShiftPoint6,rpmShiftPoint6, mphShiftPoint7,torqueShiftPoint7,rpmShiftPoint7,mphShiftPoint8,torqueShiftPoint8,rpmShiftPoint8,mphShiftPoint9,torqueShiftPoint9,rpmShiftPoint9,mphShiftPoint10,torqueShiftPoint10,rpmShiftPoint10,str(datetime.now())
            ]

            #Reads database and extracts all values into a list
            with open(file_name, mode='r') as file:
                # Read the existing CSV data
                csv_data = list(csv.reader(file))
                file.close

            #Sets the required index in the list to the data created earlier
            csv_data[result-1] = data

            #Pushes the updated list back into the csv
            with open(file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(csv_data)
                file.close
            
            print("Car information updated in database.")
        else:
            print("Car doesn't already exist in the database. Please add it and then re-run this method.")
    else:
        createHeaderCSV(file_name)
        print("Car doesn't already exist in the database. Please add it and then re-run this method.")

#Method for updating a specific value on an existing car via manual input
def updateCarValueViaManualInput(file_name,CarOrdinalID,field):
    # Create a Path object
    file_path_obj = Path(file_name)

    if file_path_obj.is_file():
        print(f'The file "{file_name}" exists.')

        #Sets search term for searching CSV file for match
        search_term = CarOrdinalID  

        #Runs search_csv method and returns row value if matched
        result = search_csv(file_name, search_term)

        if result:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_name)

            rowData = df[df['CarOrdinalID'] == CarOrdinalID]
            
            try:
                fieldValue = rowData[field].iloc[0]
                print("Confirmed car exists in DB and requested field is currently set to: " + str(fieldValue))
                question = "Are you sure you want to update the " + str(field) + " value?"
                user_input = input(question)

                if user_input.lower() == "yes" or user_input.lower() == "y":
                    next_input = input("What should the field be set to?")

                    rowData[field].iloc[0] = next_input

                    df[df['CarOrdinalID'] == CarOrdinalID] = rowData

                    # Save the updated DataFrame back to a CSV file
                    df.to_csv(file_name, index=False)
                else:
                    print("User chose to exit method.")
            except:
                print("Something happened and the field value passed was not found.")
        else:
            print("Car doesn't already exist in the database. Please add it and then re-run this method.")
    else:
        createHeaderCSV(file_name)
        print("Car doesn't already exist in the database. Please add it and then re-run this method.")

#Method for updating a specific value on an existing car via method pass
def updateCarValueViaMethodInput(file_name,CarOrdinalID,field,value):
    # Create a Path object
    file_path_obj = Path(file_name)

    if file_path_obj.is_file():
        print(f'The file "{file_name}" exists.')

        #Sets search term for searching CSV file for match
        search_term = CarOrdinalID  

        #Runs search_csv method and returns row value if matched
        result = search_csv(file_name, search_term)

        if result:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_name)

            rowData = df[df['CarOrdinalID'] == CarOrdinalID]
            
            try:
                fieldValue = rowData[field].iloc[0]
                print("Confirmed car exists in DB and requested field is currently set to: " + str(fieldValue))
                question = "Are you sure you want to update the " + str(field) + " value?"
                user_input = input(question)

                if user_input.lower() == "yes" or user_input.lower() == "y":
                    rowData[field].iloc[0] = value

                    df[df['CarOrdinalID'] == CarOrdinalID] = rowData

                    # Save the updated DataFrame back to a CSV file
                    df.to_csv(file_name, index=False)
                else:
                    print("User chose to exit method.")
            except:
                print("Something happened and the field value passed was not found.")
        else:
            print("Car doesn't already exist in the database. Please add it and then re-run this method.")
    else:
        createHeaderCSV(file_name)
        print("Car doesn't already exist in the database. Please add it and then re-run this method.")

#Method for manually updating gear ratios on an existing car 
def updateCarGearRatiosViaManualInput(file_name,CarOrdinalID): 
    # Create a Path object
    file_path_obj = Path(file_name)

    if file_path_obj.is_file():
        print(f'The file "{file_name}" exists.')

        #Sets search term for searching CSV file for match
        search_term = CarOrdinalID  

        #Runs search_csv method and returns row value if matched
        result = search_csv(file_name, search_term)

        if result:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_name)
            
            #Gets row data for the matching car ID
            rowData = df[df['CarOrdinalID'] == CarOrdinalID]

            #Gets the number of gears from the DB to set the next loop
            numGears = rowData['Gears'].iloc[0]

            a = {}
            count = 1
            while count <= numGears:
                key = "Ratio" + str(count)

                a[key] = rowData[key].iloc[0]

                question = str(key) + "\'s value is currently: " + str(a[key]) + ". Are you sure you want to update the value?"
                user_input = input(question)

                if user_input.lower() == "yes" or user_input.lower() == "y":
                    next_question = input("What should the value be set to?")

                    rowData[key].iloc[0] = next_question
                else:
                    print("User chose to not update this value.")
                    rowData[key].iloc[0] = a[key]

                count += 1

            df[df['CarOrdinalID'] == CarOrdinalID] = rowData

            print("Updating db information with the following.")
            print(a)
            # Save the updated DataFrame back to a CSV file
            df.to_csv(file_name, index=False)
            print("Update complete.")
        else:
            print("Car doesn't already exist in the database. Please add it and then re-run this method.")
    else:
        createHeaderCSV(file_name)
        print("Car doesn't already exist in the database. Please add it and then re-run this method.")

#Method for adding optimal shifting information on an existing car
def updateCarShiftValuesViaTelemFiles(file_name,CarOrdinalID):
    # Create a Path object
    file_path_obj = Path(file_name)

    if file_path_obj.is_file():
        print(f'The file "{file_name}" exists.')

        #Sets search term for searching CSV file for match
        search_term = CarOrdinalID  

        #Runs search_csv method and returns row value if matched
        result = search_csv(file_name, search_term)

        if result:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_name)
        else:
            print("Car doesn't already exist in the database. Please add it and then re-run this method.")
    else:
        createHeaderCSV(file_name)
        print("Car doesn't already exist in the database. Please add it and then re-run this method.")

#Method for adding optimal shifting information on an existing car
def updateCarShiftValuesViaTelemFiles(file_name,CarOrdinalID,shiftPointArray,validGears):
    # Create a Path object
    file_path_obj = Path(file_name)

    if file_path_obj.is_file():
        print(f'The file "{file_name}" exists.')

        #Sets search term for searching CSV file for match
        search_term = CarOrdinalID  

        #Runs search_csv method and returns row value if matched
        result = search_csv(file_name, search_term)

        if result:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_name)

            #Gets row data for the matching car ID
            rowData = df[df['CarOrdinalID'] == CarOrdinalID]

            #Unpacks the shiftPointArray
            count = 1
            while count <= validGears:
                key = "gear_" + str(count) + "_Rounded_TORQUE_ShiftPoint"
                key1 = "gear_" + str(count) + "_Rounded_MPH_ShiftPoint"
                newKey = "mphShiftPoint" + str(count)
                newKey1 = "torqueShiftPoint" + str(count)

                rowData[newKey] = shiftPointArray[key]
                rowData[newKey1] = shiftPointArray[key1]

                count += 1

            print("Updating db information with the following.")
            print(rowData)

            df[df['CarOrdinalID'] == CarOrdinalID] = rowData

            # Save the updated DataFrame back to a CSV file
            df.to_csv(file_name, index=False)
            print("Update complete.")
        else:
            print("Car doesn't already exist in the database. Please add it and then re-run this method.")
    else:
        createHeaderCSV(file_name)
        print("Car doesn't already exist in the database. Please add it and then re-run this method.")

'''Starts block for triggering commands as needed'''
#Defines file path and name
file_name = os.getcwd() + "\\DBModule\\carDb2.csv"
telemPath = os.getcwd() + "\\TelemDataFiles\\logTelemetry2.csv"

#Method for creating a new entry for a car that hasn't existed before by manual input
#addNewCarByManualInputWithoutGearInfoInput(CarOrdinalID, file_name)

#Method for creating a new entry for a car that hasn't existed before by pulling data from logTelemtry
addNewCarByReadingTelemtry(file_name, telemPath)

#Method for updating all values on an existing car
#def updateCarAllValuesManually(CarOrdinalID, file_name)

#Method for updating all values on an existing car by being passed the values in the method head
#def updateCarAllValuesViaMethodInput(file_name,CarOrdinalID,CarFriendlyName,CarMake,CarModel,CarManYear,CarClass,CarPerformanceIndex,DriveTrainType,NumCylinders,EngineMaxRPM,EngineIdleRPM,Gears,FinalDriveRatio,Ratio1,Ratio2,Ratio3,Ratio4,Ratio5,Ratio6,Ratio7,Ratio8,Ratio9,Ratio10,mphShiftPoint1,torqueShiftPoint1,rpmShiftPoint1,mphShiftPoint2,torqueShiftPoint2,rpmShiftPoint2,mphShiftPoint3, torqueShiftPoint3,rpmShiftPoint3,mphShiftPoint4,torqueShiftPoint4,rpmShiftPoint4,mphShiftPoint5,torqueShiftPoint5,rpmShiftPoint5,mphShiftPoint6,torqueShiftPoint6,rpmShiftPoint6, mphShiftPoint7,torqueShiftPoint7,rpmShiftPoint7,mphShiftPoint8,torqueShiftPoint8,rpmShiftPoint8,mphShiftPoint9,torqueShiftPoint9,rpmShiftPoint9,mphShiftPoint10,torqueShiftPoint10,rpmShiftPoint10)

#Method for updating a specific value on an existing car via manual input
#def updateCarValueViaManualInput(file_name,CarOrdinalID,field)

#Method for updating a specific value on an existing car via method pass
#def updateCarValueViaMethodInput(file_name,CarOrdinalID,field,value)

#Method for manually updating gear ratios on an existing car 
#def updateCarGearRatiosViaManualInput(file_name,CarOrdinalID)