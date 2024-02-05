"""Class to handle calculating engine conditions"""
class TachCalc:
    
    def __init__(self, CurrentEngineRpm, EngineIdleRpm, EngineMaxRpm):
        self.CurrentEngineRpm = CurrentEngineRpm
        self.EngineIdleRpm = EngineIdleRpm
        self.EngineMaxRpm = EngineMaxRpm
        self.condition = self.conditionCalculator()
        
    def conditionCalculator(self):
        condition = "engineOff"
        overRevBotRange = self.EngineMaxRpm - (self.EngineMaxRpm*.1)
        optimalShiftBotRange = self.EngineMaxRpm - ((self.EngineMaxRpm*.11))
        optimalShiftTopRange = self.EngineMaxRpm - (self.EngineMaxRpm*.1)
        ledSize = 15
        interval = (optimalShiftBotRange - self.EngineIdleRpm)/ledSize
        #engine off condition
        if self.CurrentEngineRpm <= self.EngineIdleRpm:
            condition = "engineIdle"
            return condition
        elif self.CurrentEngineRpm >= overRevBotRange:
            condition = "overRev"
            return condition
        elif (self.CurrentEngineRpm >= optimalShiftBotRange) & (self.CurrentEngineRpm < optimalShiftTopRange):
            condition = "optimalShift"
            return condition
        else:
            count = 0
            while count < ledSize:
                if (self.CurrentEngineRpm > (self.EngineIdleRpm + (interval*count))) & (self.CurrentEngineRpm <= (self.EngineIdleRpm + (interval*(count+1)))):
                    count = ledSize
                    return condition
                else:
                    count = count+1