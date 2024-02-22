from color_setter import tachometer

class conditionChecker:
    def conditionSet(condition):
        match condition:
            case "engineOff":
                tachometer.raceOff()
            case "engineIdle":
                tachometer.engineIdle()
            case "overRev":
                tachometer.overRev()
            case "optimalShift":
                tachometer.optimalShift()
            case "unlit":
                tachometer.unlit()
            #case 0:
                #tachometer.Phase1()
            #case 1:
                #tachometer.Phase2()
            #case 2:
                #tachometer.Phase3()
            #case 3:
                #tachometer.Phase4()
            #case 4:
                #tachometer.Phase5()
            #case 5:
                #tachometer.Phase6()
            #case 6:
                #tachometer.Phase7()
            #case 7:
                #tachometer.Phase8()
            #case 8:
                #tachometer.Phase9()
            #case 9:
                #tachometer.Phase10()
            #case 10:
                #tachometer.Phase11()
            #case 11:
                #tachometer.Phase12()
            #case 12:
                #tachometer.Phase13()
            #case 13:
                #tachometer.Phase14()
            #case 14:
                #tachometer.Phase15()