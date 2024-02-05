import tachCalculator
import led_conditions
from datetime import datetime
#import math

#Creates file for logging condition data against current RPM
file1 = open("testLog.txt", "a")  # append mode

class tests():
    #Test condition and lights by specific values
    def conditionByValue():
        stats = tachCalculator.TachCalc(CurrentEngineRpm=8769, EngineIdleRpm=800, EngineMaxRpm=9000)
        print(stats.condition)
        led_conditions.conditionChecker.conditionSet(stats.condition)

    #Test lights by condition name
    #engineIdle, overRev, optimalShift, unlit, engineOff
    def conditionByCondition():
        led_conditions.conditionChecker.conditionSet("optimalShift")

    #Test looper to run through sequence of currentEngineRPM from 0 to engineMaxRPM
    def sequenceLooper():
        count = 0
        maxRpm = 6000
        while count <= maxRpm:
            stats = tachCalculator.TachCalc(count, 800, maxRpm)
            led_conditions.conditionChecker.conditionSet(stats.condition)
            file1.write('timestamp: ' + str(datetime.now()) + ", Condition: " + str(stats.condition) + ", RPM: " + str(count) + "\n")
            count = count+1
        else:
            file1.close()
            led_conditions.conditionChecker.conditionSet("unlit")
            print("run completed")

tests.sequenceLooper()
#conditionByCondition()
#conditionByValue()