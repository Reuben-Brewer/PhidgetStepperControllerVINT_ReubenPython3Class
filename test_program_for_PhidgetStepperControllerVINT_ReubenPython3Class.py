# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision E, 08/18/2025

Verified working on: Python 3.11/3.12 for Windows 10, 11 64-bit.
'''

__author__ = 'reuben.brewer'

##########################################
from EntryListWithBlinking_ReubenPython2and3Class import *
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *
from PhidgetStepperControllerVINT_ReubenPython3Class import *
##########################################

##########################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
import signal #for CTRLc_HandlerFunction
import keyboard
##########################################

##########################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
##########################################

##########################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
##########################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def CTRLc_RegisterHandlerFunction():

    CurrentHandlerRegisteredForSIGINT = signal.getsignal(signal.SIGINT)
    #print("CurrentHandlerRegisteredForSIGINT: " + str(CurrentHandlerRegisteredForSIGINT))

    defaultish = (signal.SIG_DFL, signal.SIG_IGN, None, getattr(signal, "default_int_handler", None)) #Treat Python's built-in default handler as "unregistered"

    if CurrentHandlerRegisteredForSIGINT in defaultish: # Only install if it's default/ignored (i.e., nobody set it yet)
        signal.signal(signal.SIGINT, CTRLc_HandlerFunction)
        print("test_program_for_PhidgetStepperControllerVINT_ReubenPython3Class.py, CTRLc_RegisterHandlerFunction event fired!")

    else:
        print("test_program_for_PhidgetStepperControllerVINT_ReubenPython3Class.py, could not register CTRLc_RegisterHandlerFunction (already registered previously)")
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def CTRLc_HandlerFunction(signum, frame):

    print("test_program_for_PhidgetStepperControllerVINT_ReubenPython3Class.py, CTRLc_HandlerFunction event firing!")

    ExitProgram_Callback()

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

###########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def GetLatestWaveformValue(CurrentTime, MinValue, MaxValue, Period, WaveformTypeString="Sine"):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            OutputValue = 0.0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            WaveformTypeString_ListOfAcceptableValues = ["Sine", "Cosine", "Triangular", "Square"]

            if WaveformTypeString not in WaveformTypeString_ListOfAcceptableValues:
                print("GetLatestWaveformValue: Error, WaveformTypeString must be in " + str(WaveformTypeString_ListOfAcceptableValues))
                return -11111.0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if WaveformTypeString == "Sine":

                TimeGain = math.pi/Period
                OutputValue = (MaxValue + MinValue)/2.0 + 0.5*abs(MaxValue - MinValue)*math.sin(TimeGain*CurrentTime)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Cosine":

                TimeGain = math.pi/Period
                OutputValue = (MaxValue + MinValue)/2.0 + 0.5*abs(MaxValue - MinValue)*math.cos(TimeGain*CurrentTime)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Triangular":
                TriangularInput_TimeGain = 1.0
                TriangularInput_MinValue = -5
                TriangularInput_MaxValue = 5.0
                TriangularInput_PeriodInSeconds = 2.0

                #TriangularInput_Height0toPeak = abs(TriangularInput_MaxValue - TriangularInput_MinValue)
                #TriangularInput_CalculatedValue_1 = abs((TriangularInput_TimeGain*CurrentTime_CalculatedFromMainThread % PeriodicInput_PeriodInSeconds) - TriangularInput_Height0toPeak) + TriangularInput_MinValue

                A = abs(MaxValue - MinValue)
                P = Period

                #https://stackoverflow.com/questions/1073606/is-there-a-one-line-function-that-generates-a-triangle-wave
                OutputValue = (A / (P / 2)) * ((P / 2) - abs(CurrentTime % (2 * (P / 2)) - P / 2)) + MinValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Square":

                TimeGain = math.pi/Period
                MeanValue = (MaxValue + MinValue)/2.0
                SinusoidalValue =  MeanValue + 0.5*abs(MaxValue - MinValue)*math.sin(TimeGain*CurrentTime)

                if SinusoidalValue >= MeanValue:
                    OutputValue = MaxValue
                else:
                    OutputValue = MinValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            else:
                OutputValue = 0.0
            ##########################################################################################################
            ##########################################################################################################

            return OutputValue

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("GetLatestWaveformValue: Exceptions: %s" % exceptions)
            return -11111.0
            traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

    number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

    ListOfStringsToJoin = []

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if isinstance(input, str) == 1:
        ListOfStringsToJoin.append(input)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
        element = float(input)
        prefix_string = "{:." + str(number_of_decimal_places) + "f}"
        element_as_string = prefix_string.format(element)

        ##########################################################################################################
        ##########################################################################################################
        if element >= 0:
            element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
            element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
        else:
            element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
        ##########################################################################################################
        ##########################################################################################################

        ListOfStringsToJoin.append(element_as_string)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, list) == 1:

        if len(input) > 0:
            for element in input: #RECURSION
                ListOfStringsToJoin.append(ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a list() or []
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, tuple) == 1:

        if len(input) > 0:
            for element in input: #RECURSION
                ListOfStringsToJoin.append("TUPLE" + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a list() or []
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, dict) == 1:

        if len(input) > 0:
            for Key in input: #RECURSION
                ListOfStringsToJoin.append(str(Key) + ": " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a dict()
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    else:
        ListOfStringsToJoin.append(str(input))
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if len(ListOfStringsToJoin) > 1:

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        StringToReturn = ""
        for Index, StringToProcess in enumerate(ListOfStringsToJoin):

            ################################################
            if Index == 0: #The first element
                if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                    StringToReturn = "{"
                elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                    StringToReturn = "("
                else:
                    StringToReturn = "["

                StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
            ################################################

            ################################################
            elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                StringToReturn = StringToReturn + StringToProcess + ", "
            ################################################

            ################################################
            else: #The last element
                StringToReturn = StringToReturn + StringToProcess

                if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                    StringToReturn = StringToReturn + "}"
                elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                    StringToReturn = StringToReturn + ")"
                else:
                    StringToReturn = StringToReturn + "]"

            ################################################

        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    elif len(ListOfStringsToJoin) == 1:
        StringToReturn = ListOfStringsToJoin[0]

    else:
        StringToReturn = ListOfStringsToJoin

    return StringToReturn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ConvertDictToProperlyFormattedStringForPrinting(DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

    try:
        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ":\n" + \
                                                     ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ": " + \
                                                     ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)

            if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                ItemsPerLineCounter = ItemsPerLineCounter + 1
            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                ItemsPerLineCounter = 0

        return ProperlyFormattedStringForPrinting

    except:
        exceptions = sys.exc_info()[0]
        print("ConvertDictToProperlyFormattedStringForPrinting, Exceptions: %s" % exceptions)
        return ""
        # traceback.print_exc()
#######################################################################################################################
#######################################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global LoopCounter_CalculatedFromGUIthread
    global CurrentTime_CalculatedFromGUIthread
    global StartingTime_CalculatedFromGUIthread
    global LastTime_CalculatedFromGUIthread
    global DataStreamingFrequency_CalculatedFromGUIthread
    global DataStreamingDeltaT_CalculatedFromGUIthread

    global EntryListWithBlinking_Object
    global EntryListWithBlinking_OPEN_FLAG

    global PhidgetStepperControllerVINT_Object
    global PhidgetStepperControllerVINT_OPEN_FLAG
    global SHOW_IN_GUI_PhidgetStepperControllerVINT_FLAG
    global PhidgetStepperControllerVINT_MostRecentDict
    global PhidgetStepperControllerVINT_MostRecentDict_Label

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################
        #########################################################

            #########################################################
            #########################################################
            try:
                #########################################################
                CurrentTime_CalculatedFromGUIthread = getPreciseSecondsTimeStampString() - StartingTime_CalculatedFromGUIthread
                [LoopCounter_CalculatedFromGUIthread, LastTime_CalculatedFromGUIthread, DataStreamingFrequency_CalculatedFromGUIthread, DataStreamingDeltaT_CalculatedFromGUIthread] = UpdateFrequencyCalculation(LoopCounter_CalculatedFromGUIthread, CurrentTime_CalculatedFromGUIthread,
                                                                                                                                                                                                                  LastTime_CalculatedFromGUIthread, DataStreamingFrequency_CalculatedFromGUIthread,
                                                                                                                                                                                                                  DataStreamingDeltaT_CalculatedFromGUIthread)
                #########################################################

                #########################################################
                PhidgetStepperControllerVINT_MostRecentDict_Label["text"] = ConvertDictToProperlyFormattedStringForPrinting(PhidgetStepperControllerVINT_MostRecentDict, NumberOfDecimalsPlaceToUse=3, NumberOfEntriesPerLine=3, NumberOfTabsBetweenItems=1)
                #########################################################

                #########################################################
                if EntryListWithBlinking_OPEN_FLAG == 1:
                    EntryListWithBlinking_Object.GUI_update_clock()
                #########################################################

                #########################################################
                if PhidgetStepperControllerVINT_OPEN_FLAG == 1 and SHOW_IN_GUI_PhidgetStepperControllerVINT_FLAG == 1:
                    PhidgetStepperControllerVINT_Object.GUI_update_clock()
                #########################################################

                #########################################################
                root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
                #########################################################

            #########################################################
            #########################################################

            #########################################################
            #########################################################
            except:
                exceptions = sys.exc_info()[0]
                print("GUI_update_clock(), Exceptions: %s" % exceptions)
                traceback.print_exc()
            #########################################################
            #########################################################

        #########################################################
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG

    print("ExitProgram_Callback event fired!")

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def UpdateFrequencyCalculation(LoopCounter, CurrentTime, LastTime, DataStreamingFrequency, DataStreamingDeltaT):

    try:

        DataStreamingDeltaT = CurrentTime - LastTime

        ##########################
        if DataStreamingDeltaT != 0.0:
            DataStreamingFrequency = 1.0/DataStreamingDeltaT
        ##########################

        LastTime = CurrentTime

        LoopCounter = LoopCounter + 1

        return [LoopCounter, LastTime, DataStreamingFrequency, DataStreamingDeltaT]

    except:
        exceptions = sys.exc_info()[0]
        print("UpdateFrequencyCalculation, exceptions: %s" % exceptions)
        return [-11111.0]*4
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_PhidgetStepperControllerVINT

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_PhidgetStepperControllerVINT = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_PhidgetStepperControllerVINT, text='   PhidgetStepperControllerVINT   ')

        Tab_MainControls = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        TabControlObject.grid(row=0, column=0, sticky='nsew')

        ############# #Set the tab header font
        TabStyle = ttk.Style()
        TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############
        #################################################
    else:
        #################################################
        Tab_MainControls = root
        Tab_PhidgetStepperControllerVINT = root
        #################################################

    ##########################################################################################################

    #################################################
    #################################################
    global MainFrame
    MainFrame = Frame(Tab_MainControls)
    MainFrame.grid(row=0, column=0, padx=1, pady=1, rowspan=1, columnspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    global PhidgetStepperControllerVINT_MostRecentDict_Label
    PhidgetStepperControllerVINT_MostRecentDict_Label = Label(MainFrame, text="PhidgetStepperControllerVINT_MostRecentDict_Label", width=120, font=("Helvetica", 10))
    PhidgetStepperControllerVINT_MostRecentDict_Label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    global ButtonsFrame
    ButtonsFrame = Frame(MainFrame)
    ButtonsFrame.grid(row = 1, column = 0, padx = 1, pady = 1, rowspan = 1, columnspan = 1)
    #################################################
    #################################################

    #################################################
    #################################################
    global ZeroPosition_Button
    ZeroPosition_Button = Button(ButtonsFrame, text=" TestProgram: ZeroPos", state="normal", width=20, command=lambda: ZeroPosition_Button_Response())
    ZeroPosition_Button.grid(row=0, column=0, padx=10, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

    ##########################################################################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_PhidgetStepperControllerVINT_ReubenPython3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ZeroPosition_Button_Response():
    global PhidgetStepperControllerVINT_ZeroPosition_EventNeedsToBeFiredFlag

    PhidgetStepperControllerVINT_ZeroPosition_EventNeedsToBeFiredFlag = 1

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    CTRLc_RegisterHandlerFunction()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    #################################################
    #################################################

    ################################################# unicorn
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_EntryListWithBlinking_FLAG
    USE_EntryListWithBlinking_FLAG = 1

    global USE_PhidgetStepperControllerVINT_FLAG
    USE_PhidgetStepperControllerVINT_FLAG = 1

    global USE_MyPlotterPureTkinterStandAloneProcess0_FLAG
    USE_MyPlotterPureTkinterStandAloneProcess0_FLAG = 1

    global USE_KEYBOARD_FLAG
    USE_KEYBOARD_FLAG = 1

    global USE_PeriodicInput_FLAG
    USE_PeriodicInput_FLAG = 0
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_PhidgetStepperControllerVINT_FLAG
    SHOW_IN_GUI_PhidgetStepperControllerVINT_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_EntryListWithBlinking
    global GUI_COLUMN_EntryListWithBlinking
    global GUI_PADX_EntryListWithBlinking
    global GUI_PADY_EntryListWithBlinking
    global GUI_ROWSPAN_EntryListWithBlinking
    global GUI_COLUMNSPAN_EntryListWithBlinking
    GUI_ROW_EntryListWithBlinking = 2

    GUI_COLUMN_EntryListWithBlinking = 0
    GUI_PADX_EntryListWithBlinking = 1
    GUI_PADY_EntryListWithBlinking = 1
    GUI_ROWSPAN_EntryListWithBlinking = 1
    GUI_COLUMNSPAN_EntryListWithBlinking = 1

    global GUI_ROW_PhidgetStepperControllerVINT
    global GUI_COLUMN_PhidgetStepperControllerVINT
    global GUI_PADX_PhidgetStepperControllerVINT
    global GUI_PADY_PhidgetStepperControllerVINT
    global GUI_ROWSPAN_PhidgetStepperControllerVINT
    global GUI_COLUMNSPAN_PhidgetStepperControllerVINT
    GUI_ROW_PhidgetStepperControllerVINT = 1

    GUI_COLUMN_PhidgetStepperControllerVINT = 0
    GUI_PADX_PhidgetStepperControllerVINT = 1
    GUI_PADY_PhidgetStepperControllerVINT = 1
    GUI_ROWSPAN_PhidgetStepperControllerVINT = 1
    GUI_COLUMNSPAN_PhidgetStepperControllerVINT = 2
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    #################################################
    global CurrentTime_CalculatedFromMainThread
    CurrentTime_CalculatedFromMainThread = -11111.0

    global StartingTime_CalculatedFromMainThread
    StartingTime_CalculatedFromMainThread = -11111.0
    #################################################

    #################################################
    global LoopCounter_CalculatedFromGUIthread
    LoopCounter_CalculatedFromGUIthread = 0

    global CurrentTime_CalculatedFromGUIthread
    CurrentTime_CalculatedFromGUIthread = -11111.0

    global StartingTime_CalculatedFromGUIthread
    StartingTime_CalculatedFromGUIthread = -11111.0

    global LastTime_CalculatedFromGUIthread
    LastTime_CalculatedFromGUIthread = -11111.0

    global DataStreamingFrequency_CalculatedFromGUIthread
    DataStreamingFrequency_CalculatedFromGUIthread = -1

    global DataStreamingDeltaT_CalculatedFromGUIthread
    DataStreamingDeltaT_CalculatedFromGUIthread = -1
    #################################################

    global root

    global root_Xpos
    root_Xpos = 870

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1600

    global root_height
    root_height = 1300

    global TabControlObject
    global Tab_MainControls
    global Tab_PhidgetStepperControllerVINT

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 40

    global PeriodicInput_AcceptableValues
    PeriodicInput_AcceptableValues = ["Sine", "Cosine", "Triangular", "Square"]

    global PeriodicInput_Type_1
    PeriodicInput_Type_1 = "Triangular"

    global PeriodicInput_MinValue_1
    PeriodicInput_MinValue_1 = -0.5

    global PeriodicInput_MaxValue_1
    PeriodicInput_MaxValue_1 = 0.5

    global PeriodicInput_Period_1 #unicorn
    PeriodicInput_Period_1 = 3.0

    global PeriodicInput_CalculatedValue_1
    PeriodicInput_CalculatedValue_1 = 0.0
    #################################################
    #################################################

    #################################################
    #################################################
    global EntryListWithBlinking_Object

    global EntryListWithBlinking_OPEN_FLAG
    EntryListWithBlinking_OPEN_FLAG = -1

    global EntryListWithBlinking_MostRecentDict
    EntryListWithBlinking_MostRecentDict = dict()

    global EntryListWithBlinking_MostRecentDict_DataUpdateNumber
    EntryListWithBlinking_MostRecentDict_DataUpdateNumber = 0

    global EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last
    EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last = -1

    EntryWidth = 10
    LabelWidth = 80
    FontSize = 8
    #################################################
    #################################################

    #################################################
    #################################################
    global PhidgetStepperControllerVINT_Object

    global PhidgetStepperControllerVINT_OPEN_FLAG
    PhidgetStepperControllerVINT_OPEN_FLAG = 0

    global PhidgetStepperControllerVINT_VoltageInput_Value_ExponentialSmoothingFilterLambda
    PhidgetStepperControllerVINT_VoltageInput_Value_ExponentialSmoothingFilterLambda = 0.7

    global PhidgetStepperControllerVINT_VoltageInputDerivative_Value_ExponentialSmoothingFilterLambda
    PhidgetStepperControllerVINT_VoltageInputDerivative_Value_ExponentialSmoothingFilterLambda = 0.8

    global PhidgetStepperControllerVINT_StallDetectionThreshold
    PhidgetStepperControllerVINT_StallDetectionThreshold = 0.25

    global PhidgetStepperControllerVINT_MostRecentDict
    PhidgetStepperControllerVINT_MostRecentDict = dict()

    global PhidgetStepperControllerVINT_MostRecentDict_Time
    PhidgetStepperControllerVINT_MostRecentDict_Time = 0.0

    global PhidgetStepperControllerVINT_MostRecentDict_Position_ToBeSet_AllUnitsDict
    PhidgetStepperControllerVINT_MostRecentDict_Position_ToBeSet_AllUnitsDict = dict([("PhidgetsUnits", 0.0),
                                                                                                    ("Deg", 0.0),
                                                                                                    ("Rad", 0.0),
                                                                                                    ("Rev", 0.0)])

    global PhidgetStepperControllerVINT_MostRecentDict_Position_Actual_AllUnitsDict
    PhidgetStepperControllerVINT_MostRecentDict_Position_Actual_AllUnitsDict = dict([("PhidgetsUnits", 0.0),
                                                                                                    ("Deg", 0.0),
                                                                                                    ("Rad", 0.0),
                                                                                                    ("Rev", 0.0)])

    global PhidgetStepperControllerVINT_MostRecentDict_VoltageInput_Value_Raw
    PhidgetStepperControllerVINT_MostRecentDict_VoltageInput_Value_Raw = 0.0

    global PhidgetStepperControllerVINT_MostRecentDict_VoltageInput_Value_Filtered
    PhidgetStepperControllerVINT_MostRecentDict_VoltageInput_Value_Filtered = 0.0

    global PhidgetStepperControllerVINT_MostRecentDict_VoltageInputDerivative_Value_Raw
    PhidgetStepperControllerVINT_MostRecentDict_VoltageInputDerivative_Value_Raw = 0.0

    global PhidgetStepperControllerVINT_MostRecentDict_VoltageInputDerivative_Value_Filtered
    PhidgetStepperControllerVINT_MostRecentDict_VoltageInputDerivative_Value_Filtered = 0.0

    global PhidgetStepperControllerVINT_ZeroPosition_EventNeedsToBeFiredFlag
    PhidgetStepperControllerVINT_ZeroPosition_EventNeedsToBeFiredFlag = 0
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess0_Object

    global MyPlotterPureTkinterStandAloneProcess0_OPEN_FLAG
    MyPlotterPureTkinterStandAloneProcess0_OPEN_FLAG = -1

    global MyPlotterPureTkinterStandAloneProcess0_MostRecentDict
    MyPlotterPureTkinterStandAloneProcess0_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess0_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess0_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = -1

    global LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess0
    LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess0 = -11111.0
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## KEY GUI LINE
    ##########################################################################################################
    ##########################################################################################################
    if USE_GUI_FLAG == 1:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
        time.sleep(0.5)  #Allow enough time for 'root' to be created that we can then pass it into other classes.
    else:
        root = None
        Tab_MainControls = None
        Tab_PhidgetStepperControllerVINT = None
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global EntryListWithBlinking_Object_GUIparametersDict
    EntryListWithBlinking_Object_GUIparametersDict = dict([("root", Tab_MainControls),
                                                                                ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                                ("GUI_ROW", GUI_ROW_EntryListWithBlinking),
                                                                                ("GUI_COLUMN", GUI_COLUMN_EntryListWithBlinking),
                                                                                ("GUI_PADX", GUI_PADX_EntryListWithBlinking),
                                                                                ("GUI_PADY", GUI_PADY_EntryListWithBlinking),
                                                                                ("GUI_ROWSPAN", GUI_ROWSPAN_EntryListWithBlinking),
                                                                                ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_EntryListWithBlinking)])

    global EntryListWithBlinking_Variables_ListOfDicts
    EntryListWithBlinking_Variables_ListOfDicts = [dict([("Name", "PhidgetStepperControllerVINT_StallDetectionThreshold"),("Type", "float"),("StartingVal", PhidgetStepperControllerVINT_StallDetectionThreshold),("MinVal", 0.0),("MaxVal", 1000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                   dict([("Name", "PhidgetStepperControllerVINT_VoltageInput_Value_ExponentialSmoothingFilterLambda"),("Type", "float"),("StartingVal", PhidgetStepperControllerVINT_VoltageInput_Value_ExponentialSmoothingFilterLambda),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                   dict([("Name", "PhidgetStepperControllerVINT_VoltageInputDerivative_Value_ExponentialSmoothingFilterLambda"),("Type", "float"),("StartingVal", PhidgetStepperControllerVINT_VoltageInputDerivative_Value_ExponentialSmoothingFilterLambda),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)])]

    global EntryListWithBlinking_Object_SetupDict
    EntryListWithBlinking_Object_SetupDict = dict([("GUIparametersDict", EntryListWithBlinking_Object_GUIparametersDict),
                                                                          ("EntryListWithBlinking_Variables_ListOfDicts", EntryListWithBlinking_Variables_ListOfDicts),
                                                                          ("DebugByPrintingVariablesFlag", 0),
                                                                          ("LoseFocusIfMouseLeavesEntryFlag", 0)])
    if USE_EntryListWithBlinking_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            EntryListWithBlinking_Object = EntryListWithBlinking_ReubenPython2and3Class(EntryListWithBlinking_Object_SetupDict)
            EntryListWithBlinking_OPEN_FLAG = EntryListWithBlinking_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("EntryListWithBlinking_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_EntryListWithBlinking_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if EntryListWithBlinking_OPEN_FLAG != 1:
                print("Failed to open EntryListWithBlinking_ReubenPython2and3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global PhidgetStepperControllerVINT_GUIparametersDict
    PhidgetStepperControllerVINT_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_PhidgetStepperControllerVINT_FLAG),
                                                            ("root", Tab_PhidgetStepperControllerVINT),
                                                            ("EnableInternal_MyPrint_Flag", 0),
                                                            ("NumberOfPrintLines", 10),
                                                            ("UseBorderAroundThisGuiObjectFlag", 0),
                                                            ("GUI_ROW", GUI_ROW_PhidgetStepperControllerVINT),
                                                            ("GUI_COLUMN", GUI_COLUMN_PhidgetStepperControllerVINT),
                                                            ("GUI_PADX", GUI_PADX_PhidgetStepperControllerVINT),
                                                            ("GUI_PADY", GUI_PADY_PhidgetStepperControllerVINT),
                                                            ("GUI_ROWSPAN", GUI_ROWSPAN_PhidgetStepperControllerVINT),
                                                            ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_PhidgetStepperControllerVINT)])

    global PhidgetStepperControllerVINT_MinAndMaxLimitsUserSetDict
    PhidgetStepperControllerVINT_MinAndMaxLimitsUserSetDict = dict([("Position_Min_PhidgetsUnits_UserSet", -44444),
                                                                    ("Position_Max_PhidgetsUnits_UserSet", 44444)])

    '''
    ("VelocityLimit_Min_PhidgetsUnits_UserSet", 200),
    ("VelocityLimit_Max_PhidgetsUnits_UserSet", 20000),
    ("Acceleration_Min_PhidgetsUnits_UserSet", 300),
    ("Acceleration_Max_PhidgetsUnits_UserSet", 20000),
    ("CurrentLimit_Min_PhidgetsUnits_UserSet", 0),
    ("CurrentLimit_Max_PhidgetsUnits_UserSet", 8),
    ("HoldingCurrentLimit_Min_PhidgetsUnits_UserSet", 0),
    ("HoldingCurrentLimit_Max_PhidgetsUnits_UserSet", 8)
    '''

    global PhidgetStepperControllerVINT_InitialSettingsDict
    PhidgetStepperControllerVINT_InitialSettingsDict = dict([("Position_ToBeSet_PhidgetsUnits", 0),
                                                            ("VelocityLimit_ToBeSet_PhidgetsUnits", 10000),
                                                            ("Acceleration_ToBeSet_PhidgetsUnits", 20000),
                                                            ("CurrentLimit_ToBeSet_PhidgetsUnits", 0.5),
                                                            ("HoldingCurrentLimit_ToBeSet_PhidgetsUnits", 0.5)])

    global PhidgetStepperControllerVINT_SetupDict
    PhidgetStepperControllerVINT_SetupDict = dict([("GUIparametersDict", PhidgetStepperControllerVINT_GUIparametersDict),
                                                   ("UsePhidgetsLoggingInternalToThisClassObjectFlag", 1),
                                                   ("VINT_DesiredSerialNumber", -1),  # CHANGE THIS TO MATCH YOUR UNIQUE VINT 723183, 765592
                                                   ("VINT_DesiredPortNumber", 5),  # CHANGE THIS TO MATCH YOUR UNIQUE VINT
                                                   ("DesiredDeviceID", -1), #118, 149
                                                   ("WaitForAttached_TimeoutDuration_Milliseconds", 1000),
                                                   ("MainThread_TimeToSleepEachLoop", 0.008),
                                                   ("NameToDisplay_UserSet", "PhidgetStepperControllerVINT"),
                                                   ("EngageMotorOnAttachFlag", 1),
                                                   ("FailsafeTime_Milliseconds", 555),
                                                   ("DegPerStep", 1.8),
                                                   ("MinAndMaxLimitsUserSetDict", PhidgetStepperControllerVINT_MinAndMaxLimitsUserSetDict),
                                                   ("InitialSettingsDict", PhidgetStepperControllerVINT_InitialSettingsDict),
                                                   ("VoltageInput_Value_ExponentialSmoothingFilterLambda", PhidgetStepperControllerVINT_VoltageInput_Value_ExponentialSmoothingFilterLambda),
                                                   ("VoltageInputDerivative_Value_ExponentialSmoothingFilterLambda", PhidgetStepperControllerVINT_VoltageInputDerivative_Value_ExponentialSmoothingFilterLambda),
                                                   ("StallDetectionThreshold", PhidgetStepperControllerVINT_StallDetectionThreshold),
                                                   ("HomeStepperAgainstHardStop_Direction", -1),
                                                   ("HomeStepperAgainstHardStopOnStartupFlag", 1)])

    if USE_PhidgetStepperControllerVINT_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            PhidgetStepperControllerVINT_Object = PhidgetStepperControllerVINT_ReubenPython3Class(PhidgetStepperControllerVINT_SetupDict)
            PhidgetStepperControllerVINT_OPEN_FLAG = PhidgetStepperControllerVINT_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("PhidgetStepperControllerVINT_ReubenPython3ClassObject __init__, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_PhidgetStepperControllerVINT_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if PhidgetStepperControllerVINT_OPEN_FLAG != 1:
                print("Failed to open PhidgetStepperControllerVINT_ReubenPython3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess0_NameList
    MyPlotterPureTkinterStandAloneProcess0_NameList = ["Position_Commanded", "Position_Actual"]

    global MyPlotterPureTkinterStandAloneProcess0_MarkerSizeList
    MyPlotterPureTkinterStandAloneProcess0_MarkerSizeList = [0]*2

    global MyPlotterPureTkinterStandAloneProcess0_LineWidthList
    MyPlotterPureTkinterStandAloneProcess0_LineWidthList = [2]*2

    global MyPlotterPureTkinterStandAloneProcess0_IncludeInXaxisAutoscaleCalculationList
    MyPlotterPureTkinterStandAloneProcess0_IncludeInXaxisAutoscaleCalculationList = [1, 1]

    global MyPlotterPureTkinterStandAloneProcess0_IncludeInYaxisAutoscaleCalculationList
    MyPlotterPureTkinterStandAloneProcess0_IncludeInYaxisAutoscaleCalculationList = [1, 1]

    global MyPlotterPureTkinterStandAloneProcess0_ColorList
    MyPlotterPureTkinterStandAloneProcess0_ColorList = ["Green", "Red"]

    global MyPlotterPureTkinterStandAloneProcess0_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess0_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                    ("NumberOfPrintLines", 10),
                                                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                    ("GraphCanvasWidth", 800),
                                                                    ("GraphCanvasHeight", 550),
                                                                    ("GraphCanvasWindowStartingX", 0),
                                                                    ("GraphCanvasWindowStartingY", 0),
                                                                    ("GraphCanvasWindowTitle", "Stepper"),
                                                                    ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 30)])

    global MyPlotterPureTkinterStandAloneProcess0_SetupDict
    MyPlotterPureTkinterStandAloneProcess0_SetupDict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess0_GUIparametersDict),
                                                            ("ParentPID", os.getpid()),
                                                            ("WatchdogTimerExpirationDurationSeconds_StandAlonePlottingProcess", 5.0),
                                                            ("CurvesToPlotNamesAndColorsDictOfLists",
                                                                dict([("NameList", MyPlotterPureTkinterStandAloneProcess0_NameList),
                                                                      ("MarkerSizeList", MyPlotterPureTkinterStandAloneProcess0_MarkerSizeList),
                                                                      ("LineWidthList", MyPlotterPureTkinterStandAloneProcess0_LineWidthList),
                                                                      ("IncludeInXaxisAutoscaleCalculationList", MyPlotterPureTkinterStandAloneProcess0_IncludeInXaxisAutoscaleCalculationList),
                                                                      ("IncludeInYaxisAutoscaleCalculationList", MyPlotterPureTkinterStandAloneProcess0_IncludeInYaxisAutoscaleCalculationList),
                                                                      ("ColorList", MyPlotterPureTkinterStandAloneProcess0_ColorList)])),
                                                            ("SmallTextSize", 7),
                                                            ("LargeTextSize", 12),
                                                            ("NumberOfDataPointToPlot", 50),
                                                            ("XaxisNumberOfTickMarks", 10),
                                                            ("YaxisNumberOfTickMarks", 10),
                                                            ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("XaxisAutoscaleFlag", 1),
                                                            ("YaxisAutoscaleFlag", 1),
                                                            ("X_min", 0.0),
                                                            ("X_max", 20.0),
                                                            ("Y_min", -10.00),
                                                            ("Y_max", 10.00),
                                                            ("XaxisDrawnAtBottomOfGraph", 0),
                                                            ("XaxisLabelString", "Time (sec)"),
                                                            ("YaxisLabelString", "Y-units (units)"),
                                                            ("ShowLegendFlag", 1),
                                                            ("SavePlot_DirectoryPath", os.path.join(os.getcwd(), "SavedImagesFolder"))])

    if USE_MyPlotterPureTkinterStandAloneProcess0_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPlotterPureTkinterStandAloneProcess0_Object = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess0_SetupDict)
            MyPlotterPureTkinterStandAloneProcess0_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess0_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess0_Object, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPlotterPureTkinterStandAloneProcess0_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPlotterPureTkinterStandAloneProcess0_OPEN_FLAG != 1:
                print("Failed to open MyPlotterPureTkinterClass_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if USE_KEYBOARD_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    #PhidgetStepperControllerVINT_Object.HomeStepperAgainstHardStop(-1)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if EXIT_PROGRAM_FLAG == 0:
        print("Starting main loop 'test_program_for_PhidgetStepperControllerVINT_ReubenPython3Class.")
        StartingTime_CalculatedFromMainThread = getPreciseSecondsTimeStampString()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    while(EXIT_PROGRAM_FLAG == 0):

        ##########################################################################################################
        ##########################################################################################################

        ###################################################
        ###################################################
        ###################################################
        CurrentTime_CalculatedFromMainThread = getPreciseSecondsTimeStampString() - StartingTime_CalculatedFromMainThread
        ###################################################
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        ###################################################

        ################################################### GET's
        ###################################################
        if EntryListWithBlinking_OPEN_FLAG == 1:

            EntryListWithBlinking_MostRecentDict = EntryListWithBlinking_Object.GetMostRecentDataDict()

            if "DataUpdateNumber" in EntryListWithBlinking_MostRecentDict and EntryListWithBlinking_MostRecentDict["DataUpdateNumber"] != EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last:
                EntryListWithBlinking_MostRecentDict_DataUpdateNumber = EntryListWithBlinking_MostRecentDict["DataUpdateNumber"]
                #print("DataUpdateNumber = " + str(EntryListWithBlinking_MostRecentDict_DataUpdateNumber) + ", EntryListWithBlinking_MostRecentDict: " + str(EntryListWithBlinking_MostRecentDict))

                ###################################################
                if EntryListWithBlinking_MostRecentDict_DataUpdateNumber > 1:

                    PhidgetStepperControllerVINT_StallDetectionThreshold = float(EntryListWithBlinking_MostRecentDict["PhidgetStepperControllerVINT_StallDetectionThreshold"])
                    PhidgetStepperControllerVINT_VoltageInput_Value_ExponentialSmoothingFilterLambda = float(EntryListWithBlinking_MostRecentDict["PhidgetStepperControllerVINT_VoltageInput_Value_ExponentialSmoothingFilterLambda"])
                    PhidgetStepperControllerVINT_VoltageInputDerivative_Value_ExponentialSmoothingFilterLambda = float(EntryListWithBlinking_MostRecentDict["PhidgetStepperControllerVINT_VoltageInputDerivative_Value_ExponentialSmoothingFilterLambda"])

                    if PhidgetStepperControllerVINT_OPEN_FLAG == 1:

                        PhidgetStepperControllerVINT_Object.UpdateStallDetectionThreshold(PhidgetStepperControllerVINT_StallDetectionThreshold)

                        PhidgetStepperControllerVINT_Object.UpdateVariableFilterSettingsFromExternalProgram("VoltageInput_Value",
                                                                                                            UseMedianFilterFlag=1,
                                                                                                            UseExponentialSmoothingFilterFlag=1,
                                                                                                            ExponentialSmoothingFilterLambda=PhidgetStepperControllerVINT_VoltageInput_Value_ExponentialSmoothingFilterLambda,
                                                                                                            PrintInfoForDebuggingFlag=0)

                        PhidgetStepperControllerVINT_Object.UpdateVariableFilterSettingsFromExternalProgram("VoltageInputDerivative_Value",
                                                                                                             UseMedianFilterFlag=1,
                                                                                                             UseExponentialSmoothingFilterFlag=1,
                                                                                                             ExponentialSmoothingFilterLambda=PhidgetStepperControllerVINT_VoltageInputDerivative_Value_ExponentialSmoothingFilterLambda,
                                                                                                             PrintInfoForDebuggingFlag=0)
                ###################################################

        ###################################################
        ###################################################

        ###################################################
        ###################################################
        EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last = EntryListWithBlinking_MostRecentDict_DataUpdateNumber
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        ###################################################

        ################################################### GET's
        ###################################################
        ###################################################
        if PhidgetStepperControllerVINT_OPEN_FLAG == 1:

            PhidgetStepperControllerVINT_MostRecentDict = PhidgetStepperControllerVINT_Object.GetMostRecentDataDict()
            #print("PhidgetStepperControllerVINT_MostRecentDict: " + str(PhidgetStepperControllerVINT_MostRecentDict))

            if "Time" in PhidgetStepperControllerVINT_MostRecentDict:
                PhidgetStepperControllerVINT_MostRecentDict_Time = PhidgetStepperControllerVINT_MostRecentDict["Time"]
                PhidgetStepperControllerVINT_MostRecentDict_Position_ToBeSet_AllUnitsDict = PhidgetStepperControllerVINT_MostRecentDict["Position_ToBeSet_AllUnitsDict"]
                PhidgetStepperControllerVINT_MostRecentDict_Position_Actual_AllUnitsDict = PhidgetStepperControllerVINT_MostRecentDict["Position_Actual_AllUnitsDict"]

                PhidgetStepperControllerVINT_MostRecentDict_VoltageInput_Value_Raw = PhidgetStepperControllerVINT_MostRecentDict["VoltageInput_Value_Raw"]
                PhidgetStepperControllerVINT_MostRecentDict_VoltageInput_Value_Filtered = PhidgetStepperControllerVINT_MostRecentDict["VoltageInput_Value_Filtered"]

                PhidgetStepperControllerVINT_MostRecentDict_VoltageInputDerivative_Value_Raw = PhidgetStepperControllerVINT_MostRecentDict["VoltageInputDerivative_Value_Filtered"]
                PhidgetStepperControllerVINT_MostRecentDict_VoltageInputDerivative_Value_Filtered = PhidgetStepperControllerVINT_MostRecentDict["VoltageInputDerivative_Value_Filtered"]
        ###################################################
        ###################################################
        ###################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ######################################################################################################
        ######################################################################################################
        PeriodicInput_CalculatedValue_1 = GetLatestWaveformValue(CurrentTime_CalculatedFromMainThread, 
                                                                PeriodicInput_MinValue_1, 
                                                                PeriodicInput_MaxValue_1, 
                                                                PeriodicInput_Period_1, 
                                                                PeriodicInput_Type_1)
        ######################################################################################################
        ######################################################################################################

        ################################################### SET's
        ###################################################
        ###################################################
        if PhidgetStepperControllerVINT_OPEN_FLAG == 1:

            ###################################################
            ###################################################
            if PhidgetStepperControllerVINT_ZeroPosition_EventNeedsToBeFiredFlag == 1:
                PhidgetStepperControllerVINT_Object.SetZeroPosition()
                PhidgetStepperControllerVINT_ZeroPosition_EventNeedsToBeFiredFlag = 0
            ###################################################
            ###################################################

            ###################################################
            ###################################################
            if USE_PeriodicInput_FLAG == 1:
                PhidgetStepperControllerVINT_Object.SetPosition(PeriodicInput_CalculatedValue_1, "Rev")
            ###################################################
            ###################################################

        ###################################################
        ###################################################
        ###################################################

        #################################################### SET's
        ####################################################
        ####################################################
        if MyPlotterPureTkinterStandAloneProcess0_OPEN_FLAG == 1:
            try:
                ####################################################
                ####################################################
                MyPlotterPureTkinterStandAloneProcess0_MostRecentDict = MyPlotterPureTkinterStandAloneProcess0_Object.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess0_MostRecentDict:
                    MyPlotterPureTkinterStandAloneProcess0_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess0_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if MyPlotterPureTkinterStandAloneProcess0_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag == 1:
                        if CurrentTime_CalculatedFromMainThread - LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess0 >= 0.030:

                            '''
                            ####################################################
                            ListOfValuesToPlot = []
                            ListOfCurveNamesToPlot = []

                            if USE_PeriodicInput_FLAG == 1:
                                ListOfValuesToPlot.append(PhidgetStepperControllerVINT_MostRecentDict_Position_ToBeSet_AllUnitsDict["Deg"])
                                ListOfCurveNamesToPlot.append(MyPlotterPureTkinterStandAloneProcess0_NameList[0])

                            ListOfValuesToPlot.append(PhidgetStepperControllerVINT_MostRecentDict_Position_Actual_AllUnitsDict["Deg"])
                            ListOfCurveNamesToPlot.append(MyPlotterPureTkinterStandAloneProcess0_NameList[1])
                            ####################################################
                            '''

                            ####################################################
                            ListOfValuesToPlot = []
                            ListOfCurveNamesToPlot = []
                            #ListOfValuesToPlot.append(PhidgetStepperControllerVINT_MostRecentDict_VoltageInput_Value_Raw)
                            ListOfValuesToPlot.append(PhidgetStepperControllerVINT_MostRecentDict_VoltageInput_Value_Filtered)
                            #ListOfValuesToPlot.append(PhidgetStepperControllerVINT_MostRecentDict_VoltageInput_Value_MeanOfHistoryList)
                            ListOfValuesToPlot.append(PhidgetStepperControllerVINT_MostRecentDict_VoltageInputDerivative_Value_Filtered)
                            ListOfCurveNamesToPlot.append(MyPlotterPureTkinterStandAloneProcess0_NameList[0])
                            ListOfCurveNamesToPlot.append(MyPlotterPureTkinterStandAloneProcess0_NameList[1])
                            ####################################################

                            ####################################################
                            MyPlotterPureTkinterStandAloneProcess0_Object.ExternalAddPointOrListOfPointsToPlot(ListOfCurveNamesToPlot,
                                                                                                                [CurrentTime_CalculatedFromMainThread]*len(ListOfValuesToPlot),
                                                                                                                ListOfValuesToPlot)
                            ####################################################

                            ####################################################
                            LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess0 = CurrentTime_CalculatedFromMainThread
                            ####################################################

                ####################################################
                ####################################################

            except:
                exceptions = sys.exc_info()[0]
                print("test_program_for_PhidgetStepperControllerVINT_ReubenPython3Class, if MyPlotterPureTkinterStandAloneProcess0_OPEN_FLAG == 1: SET's, Exceptions: %s" % exceptions)
                traceback.print_exc()
        ####################################################
        ####################################################
        ####################################################

        ##########################################################################################################
        ##########################################################################################################

        time.sleep(0.008)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## THIS IS THE EXIT ROUTINE!
    ##########################################################################################################
    ##########################################################################################################
    print("Exiting main program 'test_program_for_PhidgetStepperControllerVINT_ReubenPython3Class.")

    #################################################
    if EntryListWithBlinking_OPEN_FLAG == 1:
        EntryListWithBlinking_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if PhidgetStepperControllerVINT_OPEN_FLAG == 1:
        PhidgetStepperControllerVINT_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPlotterPureTkinterStandAloneProcess0_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess0_Object.ExitProgram_Callback()
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################