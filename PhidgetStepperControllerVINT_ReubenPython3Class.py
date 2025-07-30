# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision C, 07/29/2025

Verified working on: Python 3.11/3.12 for Windows 10, 11 64-bit.
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################

##########################################
from LowPassFilterForDictsOfLists_ReubenPython2and3Class import *
##########################################

##########################################
import os
import sys
import platform
import time
import datetime
import math
import queue as Queue
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
import subprocess
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
import signal #for CTRLc_HandlerFunction
##########################################

##########################################
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.Stepper import *
##########################################

##########################################
try:
    import platform

    if platform.system() == "Windows":
        import ctypes
        winmm = ctypes.WinDLL('winmm')
        winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.

except:
    print("PhidgetStepperControllerVINT_ReubenPython3Class,winmm.timeBeginPeriod(1) failed.")
##########################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
class PhidgetStepperControllerVINT_ReubenPython3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, SetupDict): #Subclass the Tkinter Frame

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        print("#################### PhidgetStepperControllerVINT_ReubenPython3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.HasOnAttachEverFiredPreviouslyFlag = 0

        self.FailsafeEnabledFlag = 0

        self.MainThread_StillRunningFlag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.Stepper_ImmutableLimitsReadFromDevice = dict([("DataInterval_Min_Milliseconds", -1),
                                                           ("DataInterval_Max_Milliseconds", -1),
                                                           ("DataRate_Min_Hz", -1),
                                                           ("DataRate_Max_Hz", -1),
                                                           ("FailsafeTimeMinLimit_Milliseconds", -1),
                                                           ("FailsafeTimeMaxLimit_Milliseconds", -1),
                                                           ("Position_Min_PhidgetsUnits", -1),
                                                           ("Position_Max_PhidgetsUnits", -1),
                                                           ("VelocityLimit_Min_PhidgetsUnits", -1),
                                                           ("VelocityLimit_Max_PhidgetsUnits", -1),
                                                           ("Acceleration_Min_PhidgetsUnits", -1),
                                                           ("Acceleration_Max_PhidgetsUnits", -1),
                                                           ("CurrentLimit_Min_PhidgetsUnits", -1),
                                                           ("CurrentLimit_Max_PhidgetsUnits", -1)])

        self.Stepper_ChangeableSettingsReadFromDevice = dict([("DataRate_Hz", -1)])
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################

        self.Position_ListOfAcceptableUnitString = ["PhidgetsUnits", "Deg", "Rad", "Rev"]
        self.Velocity_ListOfAcceptableUnitString = ["PhidgetsUnitsPerSec", "DegPerSec", "RadPerSec", "RevPerSec"]

        self.MotionIsStoppedFlag_Actual = 0

        self.ZeroPosition_NeedsToBeSetFlag = 0

        self.EngagedState_Actual = 0
        self.EngagedState_ToBeSet = 0
        self.EngagedState_NeedsToBeSetFlag = 1

        self.Position_Actual_PhidgetsUnits = 0.0
        self.Position_Actual_AllUnitsDict = dict([("PhidgetsUnits", 0.0),
                                                    ("Deg", 0.0),
                                                    ("Rad", 0.0),
                                                    ("Rev", 0.0)])
        self.Position_ToBeSet_PhidgetsUnits = 0
        self.Position_NeedsToBeSetFlag = 0
        self.Position_GUIscale_NeedsToBeSetFlag = 0

        self.Velocity_Actual_AllUnitsDict = dict([("PhidgetsUnitsPerSec", 0.0),
                                                    ("DegPerSec", 0.0),
                                                    ("RadPerSec", 0.0),
                                                    ("RevPerSec", 0.0)])

        self.VelocityLimit_Actual_PhidgetsUnits = 0
        self.VelocityLimit_ToBeSet_PhidgetsUnits = 0
        self.VelocityLimit_NeedsToBeSetFlag = 0
        self.VelocityLimit_GUIscale_NeedsToBeSetFlag = 0

        self.Acceleration_Actual_PhidgetsUnits = 0
        self.Acceleration_ToBeSet_PhidgetsUnits = 0
        self.Acceleration_NeedsToBeSetFlag = 0
        self.Acceleration_GUIscale_NeedsToBeSetFlag = 0

        self.CurrentLimit_Actual_PhidgetsUnits = 0
        self.CurrentLimit_ToBeSet_PhidgetsUnits = 0
        self.CurrentLimit_NeedsToBeSetFlag = 0
        self.CurrentLimit_GUIscale_NeedsToBeSetFlag = 0

        self.HoldingCurrentLimit_Actual_PhidgetsUnits = 0
        self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits = 0
        self.HoldingCurrentLimit_NeedsToBeSetFlag = 0
        self.HoldingCurrentLimit_GUIscale_NeedsToBeSetFlag = 0

        self.MostRecentDataDict = dict()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.CurrentTime_CalculatedFromGUIthread = -11111.0
        self.LastTime_CalculatedFromGUIthread = -11111.0
        self.StartingTime_CalculatedFromGUIthread = -11111.0
        self.DataStreamingFrequency_CalculatedFromGUIthread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromGUIthread = -11111.0
        self.LoopCounter_CalculatedFromDedicatedGUIthread = 0

        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0
        self.LoopCounter_CalculatedFromMainThread = 0
        
        self.CurrentTime_CalculatedFromPositionChangeCallback = -11111.0
        self.LastTime_CalculatedFromPositionChangeCallback = -11111.0
        self.StartingTime_CalculatedFromPositionChangeCallback = -11111.0
        self.DataStreamingFrequency_CalculatedFromPositionChangeCallback = -11111.0
        self.DataStreamingDeltaT_CalculatedFromPositionChangeCallback = -11111.0
        self.LoopCounter_CalculatedFromPositionChangeCallback = 0
        #########################################################
        #########################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if "GUIparametersDict" in SetupDict:

            GUIparametersDict = SetupDict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "root" in GUIparametersDict:
                self.root = GUIparametersDict["root"]
            else:
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: ERROR, must pass in 'root'")
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            ##########################################
            if "GUI_ROWSPAN" in GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in GUIparametersDict:
                self.GUI_STICKY = str(GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: GUIparametersDict: " + str(GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UsePhidgetsLoggingInternalToThisClassObjectFlag" in SetupDict:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UsePhidgetsLoggingInternalToThisClassObjectFlag", SetupDict["UsePhidgetsLoggingInternalToThisClassObjectFlag"])
        else:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = 1

        print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: UsePhidgetsLoggingInternalToThisClassObjectFlag: " + str(self.UsePhidgetsLoggingInternalToThisClassObjectFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "LogFileNameFullPath" in SetupDict:
            self.LogFileNameFullPath = str(SetupDict["LogFileNameFullPath"])

            if os.path.isdir("self.LogFileNameFullPath") == 0:
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__:  Error, 'LogFileNameFullPath' must be FULL path (should include slashes).")
                self.LogFileNameFullPath = os.path.join(os.getcwd(), "PhidgetStepperControllerVINT_ReubenPython3Class_PhidgetLog.txt")

        else:
            self.LogFileNameFullPath = os.path.join(os.getcwd(), "PhidgetStepperControllerVINT_ReubenPython3Class_PhidgetLog.txt")

        print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: LogFileNameFullPath: " + str(self.LogFileNameFullPath))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "EngageMotorOnAttachFlag" in SetupDict:
            self.EngageMotorOnAttachFlag = self.PassThrough0and1values_ExitProgramOtherwise("EngageMotorOnAttachFlag", SetupDict["EngageMotorOnAttachFlag"])
        else:
            self.EngageMotorOnAttachFlag = 1

        print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: UsePhidgetsLoggingInternalToThisClassObjectFlag: " + str(self.UsePhidgetsLoggingInternalToThisClassObjectFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "WaitForAttached_TimeoutDuration_Milliseconds" in SetupDict:
            self.WaitForAttached_TimeoutDuration_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WaitForAttached_TimeoutDuration_Milliseconds", SetupDict["WaitForAttached_TimeoutDuration_Milliseconds"], 0.0, 60000.0))

        else:
            self.WaitForAttached_TimeoutDuration_Milliseconds = 5000

        print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: WaitForAttached_TimeoutDuration_Milliseconds: " + str(self.WaitForAttached_TimeoutDuration_Milliseconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VINT_DesiredSerialNumber" in SetupDict:
            try:
                self.VINT_DesiredSerialNumber = int(SetupDict["VINT_DesiredSerialNumber"])
            except:
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Error, VINT_DesiredSerialNumber invalid.")
        else:
            self.VINT_DesiredSerialNumber = -1

        print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: VINT_DesiredSerialNumber: " + str(self.VINT_DesiredSerialNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VINT_DesiredPortNumber" in SetupDict:

            try:
                self.VINT_DesiredPortNumber = int(SetupDict["VINT_DesiredPortNumber"])
            except:
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Error, VINT_DesiredPortNumber invalid.")

        else:
            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Error, must initialize object with 'VINT_DesiredPortNumber' argument.")
            return

        print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: VINT_DesiredPortNumber: " + str(self.VINT_DesiredPortNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredDeviceID" in SetupDict:

            try:
                self.DesiredDeviceID = int(SetupDict["DesiredDeviceID"])
            except:
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Error, DesiredDeviceID invalid.")

        else:
            self.DesiredDeviceID = -1

        print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: DesiredDeviceID: " + str(self.DesiredDeviceID))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in SetupDict:
            self.NameToDisplay_UserSet = str(SetupDict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: NameToDisplay_UserSet" + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in SetupDict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", SetupDict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.010

        print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings = dict([("DataStreamingFrequency_CalculatedFromPositionChangeCallback", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                                                            ("DataStreamingFrequency_CalculatedFromMainThread", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                                                            ("DataStreamingFrequency_CalculatedFromGUIthread", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1), ("ExponentialSmoothingFilterLambda", 0.05)]))])

        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_SetupDict = dict([("DictOfVariableFilterSettings", self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings)])

        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject = LowPassFilterForDictsOfLists_ReubenPython2and3Class(self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_SetupDict)
        self.LOWPASSFILTER_OPEN_FLAG = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG
        #########################################################

        #########################################################
        if self.LOWPASSFILTER_OPEN_FLAG != 1:
            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Failed to open LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.")
            return
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        self.CTRLc_RegisterHandlerFunction()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        
        #########################################################
        #########################################################
        try:

            self.Stepper_Object = Stepper()

        except PhidgetException as e:
            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Failed to create main motor object, exception:  %i: %s" % (e.code, e.details))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            if self.VINT_DesiredSerialNumber != -1:  # '-1' means we should open the device regardless of serial number.
                self.Stepper_Object.setDeviceSerialNumber(self.VINT_DesiredSerialNumber)

        except PhidgetException as e:
            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Failed to call 'setDeviceSerialNumber()', exception:  %i: %s" % (e.code, e.details))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            self.Stepper_Object.setHubPort(self.VINT_DesiredPortNumber)

        except PhidgetException as e:
            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Failed to call 'setHubPort()', exception:  %i: %s" % (e.code, e.details))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            self.Stepper_Object.setOnAttachHandler(self.StepperOnAttachCallback)
            self.Stepper_Object.setOnDetachHandler(self.StepperOnDetachCallback)
            self.Stepper_Object.setOnErrorHandler(self.StepperOnErrorCallback)
            self.Stepper_Object.setOnPositionChangeHandler(self.StepperOnPositionChangeCallback)
            self.Stepper_Object.setOnVelocityChangeHandler(self.StepperOnVelocityChangeCallback)
            self.Stepper_Object.setOnStoppedHandler(self.StepperOnStoppedCallback)

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Set callback functions.")

            self.Stepper_Object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)

            self.PhidgetsDeviceConnectedFlag = 1
            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Attached the Stepper object.")

        except PhidgetException as e:
            self.PhidgetsDeviceConnectedFlag = 0
            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Failed to call 'openWaitForAttachment()', exception:  %i: %s" % (e.code, e.details))

            try:
                self.Stepper_Object.close()
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Closed the Stepper object.")

            except PhidgetException as e:
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Failed to call 'close()', exception:  %i: %s" % (e.code, e.details))
                
        #########################################################
        #########################################################
        
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if self.PhidgetsDeviceConnectedFlag == 1:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            #########################################################
            #########################################################
            if self.UsePhidgetsLoggingInternalToThisClassObjectFlag == 1:
                try:
                    Log.enable(LogLevel.PHIDGET_LOG_INFO, self.LogFileNameFullPath)
                    print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Enabled Phidget Logging.")
                except PhidgetException as e:
                    print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Failed to enable Phidget Logging, Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceName = self.Stepper_Object.getDeviceName()
                print("DetectedDeviceName: " + self.DetectedDeviceName)

            except PhidgetException as e:
                print("Failed to call 'getDeviceName', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.VINT_DetectedSerialNumber = self.Stepper_Object.getDeviceSerialNumber()
                print("VINT_DetectedSerialNumber: " + str(self.VINT_DetectedSerialNumber))

            except PhidgetException as e:
                print("Failed to call 'getDeviceSerialNumber', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceID = self.Stepper_Object.getDeviceID()
                print("DetectedDeviceID: " + str(self.DetectedDeviceID))

            except PhidgetException as e:
                print("Failed to call 'getDeviceID', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceVersion = self.Stepper_Object.getDeviceVersion()
                print("DetectedDeviceVersion: " + str(self.DetectedDeviceVersion))

            except PhidgetException as e:
                print("Failed to call 'getDeviceVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceLibraryVersion = self.Stepper_Object.getLibraryVersion()
                print("DetectedDeviceLibraryVersion: " + str(self.DetectedDeviceLibraryVersion))

            except PhidgetException as e:
                print("Failed to call 'getLibraryVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if self.VINT_DesiredSerialNumber != -1:
                if self.VINT_DetectedSerialNumber != self.VINT_DesiredSerialNumber:
                    print("The desired VINT_DesiredSerialNumber (" + str(self.VINT_DesiredSerialNumber) + ") does not match the detected serial number (" + str(self.VINT_DetectedSerialNumber) + ").")
                    self.CloseDevice()
                    return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if self.DesiredDeviceID != -1:
                if self.DetectedDeviceID != self.DesiredDeviceID:
                    print("The DesiredDeviceID (" + str(self.DesiredDeviceID) + ") does not match the detected Device ID (" + str(self.DetectedDeviceID) + ").")
                    self.CloseDevice()
                    return
            #########################################################
            #########################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            #########################################################
            #########################################################
            if "FailsafeTime_Milliseconds" in SetupDict:
                self.FailsafeTime_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("FailsafeTime_Milliseconds",
                                                                                                         SetupDict["FailsafeTime_Milliseconds"],
                                                                                                         self.Stepper_ImmutableLimitsReadFromDevice["FailsafeTimeMinLimit_Milliseconds"],
                                                                                                         self.Stepper_ImmutableLimitsReadFromDevice["FailsafeTimeMaxLimit_Milliseconds"]))

            else:
                self.FailsafeTime_Milliseconds = self.Stepper_ImmutableLimitsReadFromDevice["FailsafeTimeMinLimit_Milliseconds"]

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: FailsafeTime_Milliseconds: " + str(self.FailsafeTime_Milliseconds))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "DegPerStep" in SetupDict:
                self.DegPerStep = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DegPerStep", SetupDict["DegPerStep"], 0.001, 100000)

            else:
                self.DegPerStep = 1.0

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: DegPerStep: " + str(self.DegPerStep))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "MicrostepsPerStep" in SetupDict:
                self.MicrostepsPerStep = 16.0 #Hardwired in the Phidgets API for now.

                #self.MicrostepsPerStep = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MicrostepsPerStep", SetupDict["MicrostepsPerStep"], 1.0, 16.0)

            else:
                self.MicrostepsPerStep = 16.0

            print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: MicrostepsPerStep: " + str(self.MicrostepsPerStep))
            #########################################################
            #########################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            if "MinAndMaxLimitsUserSetDict" in SetupDict:
                self.MinAndMaxLimitsUserSetDict = SetupDict["MinAndMaxLimitsUserSetDict"]

                #########################################################
                #########################################################
                if "Position_Min_PhidgetsUnits_UserSet" in self.MinAndMaxLimitsUserSetDict:
                    self.Position_Min_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Position_Min_PhidgetsUnits_UserSet",
                                                                                                                      self.MinAndMaxLimitsUserSetDict["Position_Min_PhidgetsUnits_UserSet"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["Position_Min_PhidgetsUnits"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["Position_Max_PhidgetsUnits"])
    
                else:
                    self.Position_Min_PhidgetsUnits_UserSet = self.ConvertAngleToAllUnits(-1.0, "Rev")["PhidgetsUnits"]
    
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Position_Min_PhidgetsUnits_UserSet: " + str(self.Position_Min_PhidgetsUnits_UserSet))
                #########################################################
                #########################################################
    
                #########################################################
                #########################################################
                if "Position_Max_PhidgetsUnits_UserSet" in self.MinAndMaxLimitsUserSetDict:
                    self.Position_Max_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Position_Max_PhidgetsUnits_UserSet",
                                                                                                                      self.MinAndMaxLimitsUserSetDict["Position_Max_PhidgetsUnits_UserSet"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["Position_Min_PhidgetsUnits"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["Position_Max_PhidgetsUnits"])
    
                else:
                    self.Position_Max_PhidgetsUnits_UserSet = self.ConvertAngleToAllUnits(1.0, "Rev")["PhidgetsUnits"]
    
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Position_Max_PhidgetsUnits_UserSet: " + str(self.Position_Max_PhidgetsUnits_UserSet))
                #########################################################
                #########################################################
    
                #########################################################
                #########################################################
                if "VelocityLimit_Min_PhidgetsUnits_UserSet" in self.MinAndMaxLimitsUserSetDict:
                    self.VelocityLimit_Min_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityLimit_Min_PhidgetsUnits_UserSet",
                                                                                                                      self.MinAndMaxLimitsUserSetDict["VelocityLimit_Min_PhidgetsUnits_UserSet"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["VelocityLimit_Min_PhidgetsUnits"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["VelocityLimit_Max_PhidgetsUnits"])
    
                else:
                    self.VelocityLimit_Min_PhidgetsUnits_UserSet = self.Stepper_ImmutableLimitsReadFromDevice["VelocityLimit_Min_PhidgetsUnits"]
    
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: VelocityLimit_Min_PhidgetsUnits_UserSet: " + str(self.VelocityLimit_Min_PhidgetsUnits_UserSet))
                #########################################################
                #########################################################
    
                #########################################################
                #########################################################
                if "VelocityLimit_Max_PhidgetsUnits_UserSet" in self.MinAndMaxLimitsUserSetDict:
                    self.VelocityLimit_Max_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityLimit_Max_PhidgetsUnits_UserSet",
                                                                                                                      self.MinAndMaxLimitsUserSetDict["VelocityLimit_Max_PhidgetsUnits_UserSet"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["VelocityLimit_Min_PhidgetsUnits"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["VelocityLimit_Max_PhidgetsUnits"])
    
                else:
                    self.VelocityLimit_Max_PhidgetsUnits_UserSet = self.Stepper_ImmutableLimitsReadFromDevice["VelocityLimit_Max_PhidgetsUnits"]
    
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: VelocityLimit_Max_PhidgetsUnits_UserSet: " + str(self.VelocityLimit_Max_PhidgetsUnits_UserSet))
                #########################################################
                #########################################################
    
                #########################################################
                #########################################################
                if "Acceleration_Min_PhidgetsUnits_UserSet" in self.MinAndMaxLimitsUserSetDict:
                    self.Acceleration_Min_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Acceleration_Min_PhidgetsUnits_UserSet",
                                                                                                                      self.MinAndMaxLimitsUserSetDict["Acceleration_Min_PhidgetsUnits_UserSet"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["Acceleration_Min_PhidgetsUnits"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["Acceleration_Max_PhidgetsUnits"])
    
                else:
                    self.Acceleration_Min_PhidgetsUnits_UserSet = self.Stepper_ImmutableLimitsReadFromDevice["Acceleration_Min_PhidgetsUnits"]
    
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Acceleration_Min_PhidgetsUnits_UserSet: " + str(self.Acceleration_Min_PhidgetsUnits_UserSet))
                #########################################################
                #########################################################
    
                #########################################################
                #########################################################
                if "Acceleration_Max_PhidgetsUnits_UserSet" in self.MinAndMaxLimitsUserSetDict:
                    self.Acceleration_Max_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Acceleration_Max_PhidgetsUnits_UserSet",
                                                                                                                      self.MinAndMaxLimitsUserSetDict["Acceleration_Max_PhidgetsUnits_UserSet"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["Acceleration_Min_PhidgetsUnits"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["Acceleration_Max_PhidgetsUnits"])
    
                else:
                    self.Acceleration_Max_PhidgetsUnits_UserSet = self.Stepper_ImmutableLimitsReadFromDevice["Acceleration_Max_PhidgetsUnits"]
    
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: Acceleration_Max_PhidgetsUnits_UserSet: " + str(self.Acceleration_Max_PhidgetsUnits_UserSet))
                #########################################################
                #########################################################
    
                #########################################################
                #########################################################
                if "CurrentLimit_Min_PhidgetsUnits_UserSet" in self.MinAndMaxLimitsUserSetDict:
                    self.CurrentLimit_Min_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CurrentLimit_Min_PhidgetsUnits_UserSet",
                                                                                                                      self.MinAndMaxLimitsUserSetDict["CurrentLimit_Min_PhidgetsUnits_UserSet"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["CurrentLimit_Min_PhidgetsUnits"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["CurrentLimit_Max_PhidgetsUnits"])
    
                else:
                    self.CurrentLimit_Min_PhidgetsUnits_UserSet = self.Stepper_ImmutableLimitsReadFromDevice["CurrentLimit_Min_PhidgetsUnits"]
    
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: CurrentLimit_Min_PhidgetsUnits_UserSet: " + str(self.CurrentLimit_Min_PhidgetsUnits_UserSet))
                #########################################################
                #########################################################
    
                #########################################################
                #########################################################
                if "CurrentLimit_Max_PhidgetsUnits_UserSet" in self.MinAndMaxLimitsUserSetDict:
                    self.CurrentLimit_Max_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CurrentLimit_Max_PhidgetsUnits_UserSet",
                                                                                                                      self.MinAndMaxLimitsUserSetDict["CurrentLimit_Max_PhidgetsUnits_UserSet"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["CurrentLimit_Min_PhidgetsUnits"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["CurrentLimit_Max_PhidgetsUnits"])
    
                else:
                    self.CurrentLimit_Max_PhidgetsUnits_UserSet = self.Stepper_ImmutableLimitsReadFromDevice["CurrentLimit_Max_PhidgetsUnits"]
    
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: CurrentLimit_Max_PhidgetsUnits_UserSet: " + str(self.CurrentLimit_Max_PhidgetsUnits_UserSet))
                #########################################################
                #########################################################
    
                #########################################################
                #########################################################
                if "HoldingCurrentLimit_Min_PhidgetsUnits_UserSet" in self.MinAndMaxLimitsUserSetDict:
                    self.HoldingCurrentLimit_Min_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("HoldingCurrentLimit_Min_PhidgetsUnits_UserSet",
                                                                                                                      self.MinAndMaxLimitsUserSetDict["HoldingCurrentLimit_Min_PhidgetsUnits_UserSet"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["HoldingCurrentLimit_Min_PhidgetsUnits"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["HoldingCurrentLimit_Max_PhidgetsUnits"])
    
                else:
                    self.HoldingCurrentLimit_Min_PhidgetsUnits_UserSet = self.Stepper_ImmutableLimitsReadFromDevice["HoldingCurrentLimit_Min_PhidgetsUnits"]
    
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: HoldingCurrentLimit_Min_PhidgetsUnits_UserSet: " + str(self.HoldingCurrentLimit_Min_PhidgetsUnits_UserSet))
                #########################################################
                #########################################################
    
                #########################################################
                #########################################################
                if "HoldingCurrentLimit_Max_PhidgetsUnits_UserSet" in self.MinAndMaxLimitsUserSetDict:
                    self.HoldingCurrentLimit_Max_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("HoldingCurrentLimit_Max_PhidgetsUnits_UserSet",
                                                                                                                      self.MinAndMaxLimitsUserSetDict["HoldingCurrentLimit_Max_PhidgetsUnits_UserSet"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["HoldingCurrentLimit_Min_PhidgetsUnits"],
                                                                                                                      self.Stepper_ImmutableLimitsReadFromDevice["HoldingCurrentLimit_Max_PhidgetsUnits"])
    
                else:
                    self.HoldingCurrentLimit_Max_PhidgetsUnits_UserSet = self.Stepper_ImmutableLimitsReadFromDevice["HoldingCurrentLimit_Max_PhidgetsUnits"]
    
                print("PhidgetStepperControllerVINT_ReubenPython3Class __init__: HoldingCurrentLimit_Max_PhidgetsUnits_UserSet: " + str(self.HoldingCurrentLimit_Max_PhidgetsUnits_UserSet))
                #########################################################
                #########################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            if "InitialSettingsDict" in SetupDict:
                InitialSettingsDict = SetupDict["InitialSettingsDict"]

                #########################################################
                #########################################################
                if "Position_ToBeSet_PhidgetsUnits" in InitialSettingsDict:
                    self.Position_ToBeSet_PhidgetsUnits = self.LimitNumber_FloatOutputOnly(self.Position_Min_PhidgetsUnits_UserSet, self.Position_Max_PhidgetsUnits_UserSet, InitialSettingsDict["Position_ToBeSet_PhidgetsUnits"])
                 #########################################################
                #########################################################
    
                #########################################################
                #########################################################
                if "VelocityLimit_ToBeSet_PhidgetsUnits" in InitialSettingsDict:
                    self.VelocityLimit_ToBeSet_PhidgetsUnits = self.LimitNumber_FloatOutputOnly(self.VelocityLimit_Min_PhidgetsUnits_UserSet, self.VelocityLimit_Max_PhidgetsUnits_UserSet, InitialSettingsDict["VelocityLimit_ToBeSet_PhidgetsUnits"])
                #########################################################
                #########################################################
                
                #########################################################
                #########################################################
                if "Acceleration_ToBeSet_PhidgetsUnits" in InitialSettingsDict:
                    self.Acceleration_ToBeSet_PhidgetsUnits = self.LimitNumber_FloatOutputOnly(self.Acceleration_Min_PhidgetsUnits_UserSet, self.Acceleration_Max_PhidgetsUnits_UserSet, InitialSettingsDict["Acceleration_ToBeSet_PhidgetsUnits"])
                #########################################################
                #########################################################
                
                #########################################################
                #########################################################
                if "CurrentLimit_ToBeSet_PhidgetsUnits" in InitialSettingsDict:
                    self.CurrentLimit_ToBeSet_PhidgetsUnits = self.LimitNumber_FloatOutputOnly(self.CurrentLimit_Min_PhidgetsUnits_UserSet, self.CurrentLimit_Max_PhidgetsUnits_UserSet, InitialSettingsDict["CurrentLimit_ToBeSet_PhidgetsUnits"])
                #########################################################
                #########################################################
                
                #########################################################
                #########################################################
                if "HoldingCurrentLimit_ToBeSet_PhidgetsUnits" in InitialSettingsDict:
                    self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits = self.LimitNumber_FloatOutputOnly(self.HoldingCurrentLimit_Min_PhidgetsUnits_UserSet, self.HoldingCurrentLimit_Max_PhidgetsUnits_UserSet, InitialSettingsDict["HoldingCurrentLimit_ToBeSet_PhidgetsUnits"])
                #########################################################
                #########################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
        self.MainThread_ThreadingObject.start()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if self.USE_GUI_FLAG == 1:
            self.StartGUI(self.root)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1

        print("#################### PhidgetStepperControllerVINT_ReubenPython3Class __init__ ending. ####################")
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def StepperOnAttachCallback(self, HandlerSelf):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:
            
            ##########################################################################################################
            ##########################################################################################################
            self.Stepper_ImmutableLimitsReadFromDevice["DataInterval_Min_Milliseconds"] = self.Stepper_Object.getMinDataInterval()
            self.Stepper_ImmutableLimitsReadFromDevice["DataInterval_Max_Milliseconds"] = self.Stepper_Object.getMaxDataInterval()

            self.Stepper_ImmutableLimitsReadFromDevice["DataRate_Min_Hz"] = self.Stepper_Object.getMinDataRate()
            self.Stepper_ImmutableLimitsReadFromDevice["DataRate_Max_Hz"] = self.Stepper_Object.getMaxDataRate()

            self.Stepper_ImmutableLimitsReadFromDevice["FailsafeTimeMinLimit_Milliseconds"] = self.Stepper_Object.getMinFailsafeTime()
            self.Stepper_ImmutableLimitsReadFromDevice["FailsafeTimeMaxLimit_Milliseconds"] = self.Stepper_Object.getMaxFailsafeTime()

            self.Stepper_ImmutableLimitsReadFromDevice["Position_Min_PhidgetsUnits"] = self.Stepper_Object.getMinPosition()
            self.Stepper_ImmutableLimitsReadFromDevice["Position_Max_PhidgetsUnits"] = self.Stepper_Object.getMaxPosition()

            self.Stepper_ImmutableLimitsReadFromDevice["VelocityLimit_Min_PhidgetsUnits"] = self.Stepper_Object.getMinVelocityLimit()
            self.Stepper_ImmutableLimitsReadFromDevice["VelocityLimit_Max_PhidgetsUnits"] = self.Stepper_Object.getMaxVelocityLimit()

            self.Stepper_ImmutableLimitsReadFromDevice["Acceleration_Min_PhidgetsUnits"] = self.Stepper_Object.getMinAcceleration()
            self.Stepper_ImmutableLimitsReadFromDevice["Acceleration_Max_PhidgetsUnits"] = self.Stepper_Object.getMaxAcceleration()

            self.Stepper_ImmutableLimitsReadFromDevice["CurrentLimit_Min_PhidgetsUnits"] = self.Stepper_Object.getMinCurrentLimit()
            self.Stepper_ImmutableLimitsReadFromDevice["CurrentLimit_Max_PhidgetsUnits"] = self.Stepper_Object.getMaxCurrentLimit()

            self.Stepper_ImmutableLimitsReadFromDevice["HoldingCurrentLimit_Min_PhidgetsUnits"] = self.Stepper_ImmutableLimitsReadFromDevice["CurrentLimit_Min_PhidgetsUnits"]
            self.Stepper_ImmutableLimitsReadFromDevice["HoldingCurrentLimit_Max_PhidgetsUnits"] = self.Stepper_ImmutableLimitsReadFromDevice["CurrentLimit_Max_PhidgetsUnits"]

            print("StepperOnAttachCallback, self.Stepper_ImmutableLimitsReadFromDevice: " + str(self.Stepper_ImmutableLimitsReadFromDevice))
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            self.Stepper_Object.setDataRate(self.Stepper_ImmutableLimitsReadFromDevice["DataRate_Max_Hz"])
            self.Stepper_ChangeableSettingsReadFromDevice["DataRate_Hz"] = self.Stepper_Object.getDataRate()

            self.Stepper_Object.setRescaleFactor(1.0)
            self.Stepper_ChangeableSettingsReadFromDevice["RescaleFactor"] = self.Stepper_Object.getRescaleFactor()

            if self.HasOnAttachEverFiredPreviouslyFlag == 1:
                self.SetPosition(self.Position_ToBeSet_PhidgetsUnits, "PhidgetsUnits")
                self.SetVelocityLimit(self.VelocityLimit_ToBeSet_PhidgetsUnits)
                self.SetAcceleration(self.Acceleration_ToBeSet_PhidgetsUnits)
                self.SetCurrentLimit(self.CurrentLimit_ToBeSet_PhidgetsUnits)
                self.SetHoldingCurrentLimit(self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits)

                if self.FailsafeEnabledFlag == 1:
                    self.Stepper_Object.enableFailsafe(int(self.FailsafeTime_Milliseconds))

                if self.EngageMotorOnAttachFlag == 1:
                    self.SetEngagedState(1)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if self.HasOnAttachEverFiredPreviouslyFlag == 0:
                self.HasOnAttachEverFiredPreviouslyFlag = 1
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            self.PhidgetsDeviceConnectedFlag = 1
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except PhidgetException as e:

            #########################################################
            print("Failed to motor limits, Phidget Exception %i: %s" % (e.code, e.details))
            #traceback.print_exc()
            return
            #########################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StepperOnDetachCallback(self, HandlerSelf):
        self.PhidgetsDeviceConnectedFlag = 0

        self.MyPrint_WithoutLogFile("$$$$$$$$$$ StepperOnDetachCallback Detached Event! $$$$$$$$$$")

        try:
            self.Stepper_Object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            time.sleep(0.250)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("StepperOnDetachCallback failed to waitForAttach, Phidget Exception %i: %s" % (e.code, e.details))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StepperOnPositionChangeCallback(self, HandlerSelf, Position_PhidgetsUnits):

        try:
            self.Position_Actual_PhidgetsUnits = Position_PhidgetsUnits

            self.Position_Actual_AllUnitsDict = self.ConvertAngleToAllUnits(self.Position_Actual_PhidgetsUnits, "PhidgetsUnits", VelocityFlag=0)

            self.UpdateFrequencyCalculation_PositionChangeCallback_Filtered()

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("StepperOnPositionChangeCallback failed to waitForAttach, Phidget Exception %i: %s" % (e.code, e.details))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StepperOnVelocityChangeCallback(self, HandlerSelf, Velocity_PhidgetsUnits):

        try:
            self.VelocityLimit_Actual_PhidgetsUnits = Velocity_PhidgetsUnits

            self.Velocity_Actual_AllUnitsDict = self.ConvertAngleToAllUnits(self.VelocityLimit_Actual_PhidgetsUnits, "PhidgetsUnitsPerSec", VelocityFlag=1)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("StepperOnVelocityChangeCallback failed to waitForAttach, Phidget Exception %i: %s" % (e.code, e.details))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StepperOnStoppedCallback(self, HandlerSelf):

        try:
            self.MotionIsStoppedFlag_Actual = 1

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("StepperOnStoppedCallback failed to waitForAttach, Phidget Exception %i: %s" % (e.code, e.details))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StepperOnErrorCallback(self, HandlerSelf, code, description):
        self.MyPrint_WithoutLogFile("----------")
        self.MyPrint_WithoutLogFile("StepperOnErrorCallback Code: " + ErrorEventCode.getName(code) + ", Description: " + str(description))
        self.MyPrint_WithoutLogFile("----------")
    ##########################################################################################################
    ##########################################################################################################

    ###########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CTRLc_RegisterHandlerFunction(self):

        signal.signal(signal.SIGINT, self.CTRLc_HandlerFunction)

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## MUST ISSUE CTRLc_RegisterHandlerFunction() AT START OF PROGRAM
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CTRLc_HandlerFunction(self, signum, frame):

        print("PhidgetStepperControllerVINT_ReubenPython3Class, CTRLc_HandlerFunction event firing!")

        self.ExitProgram_Callback()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_FloatOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = float(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber, ExitProgramIfFailureFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a numerical value, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1.0:
                return InputNumber_ConvertedToFloat

            else:

                print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. '" +
                              str(InputNameString) +
                              "' must be 0 or 1 (value was " +
                              str(InputNumber_ConvertedToFloat) +
                              "). Press any key (and enter) to exit.")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()

                else:
                    return -1
                ##########################

            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue, ExitProgramIfFailureFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        try:
            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a float value, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat_Limited = self.LimitNumber_FloatOutputOnly(RangeMinValue, RangeMaxValue, InputNumber_ConvertedToFloat)

            if InputNumber_ConvertedToFloat_Limited != InputNumber_ConvertedToFloat:
                print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be in the range [" +
                      str(RangeMinValue) +
                      ", " +
                      str(RangeMaxValue) +
                      "] (value was " +
                      str(InputNumber_ConvertedToFloat) + ")")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()
                else:
                    return -11111.0
                ##########################

            else:
                return InputNumber_ConvertedToFloat_Limited
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict()  # So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_PositionChangeCallback_Filtered(self):

        try:
            self.CurrentTime_CalculatedFromPositionChangeCallback = self.getPreciseSecondsTimeStampString()

            self.DataStreamingDeltaT_CalculatedFromPositionChangeCallback = self.CurrentTime_CalculatedFromPositionChangeCallback - self.LastTime_CalculatedFromPositionChangeCallback

            if self.DataStreamingDeltaT_CalculatedFromPositionChangeCallback != 0.0:
                DataStreamingFrequency_CalculatedFromPositionChangeCallback_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromPositionChangeCallback

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromPositionChangeCallback", DataStreamingFrequency_CalculatedFromPositionChangeCallback_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromPositionChangeCallback = ResultsDict["DataStreamingFrequency_CalculatedFromPositionChangeCallback"]["Filtered_MostRecentValuesList"][0]

            self.LoopCounter_CalculatedFromPositionChangeCallback = self.LoopCounter_CalculatedFromPositionChangeCallback + 1
            self.LastTime_CalculatedFromPositionChangeCallback = self.CurrentTime_CalculatedFromPositionChangeCallback
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_PositionChangeCallback_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread_Filtered(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                DataStreamingFrequency_CalculatedFromMainThread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromMainThread", DataStreamingFrequency_CalculatedFromMainThread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromMainThread = ResultsDict["DataStreamingFrequency_CalculatedFromMainThread"]["Filtered_MostRecentValuesList"][0]

            self.LoopCounter_CalculatedFromMainThread = self.LoopCounter_CalculatedFromMainThread + 1
            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_GUIthread_Filtered(self):

        try:
            self.CurrentTime_CalculatedFromGUIthread = self.getPreciseSecondsTimeStampString()

            self.DataStreamingDeltaT_CalculatedFromGUIthread = self.CurrentTime_CalculatedFromGUIthread - self.LastTime_CalculatedFromGUIthread

            if self.DataStreamingDeltaT_CalculatedFromGUIthread != 0.0:
                DataStreamingFrequency_CalculatedFromGUIthread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromGUIthread

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromGUIthread", DataStreamingFrequency_CalculatedFromGUIthread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromGUIthread = ResultsDict["DataStreamingFrequency_CalculatedFromGUIthread"]["Filtered_MostRecentValuesList"][0]

            self.LoopCounter_CalculatedFromDedicatedGUIthread = self.LoopCounter_CalculatedFromDedicatedGUIthread + 1
            self.LastTime_CalculatedFromGUIthread = self.CurrentTime_CalculatedFromGUIthread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_GUIthread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertAngleToAllUnits(self, InputAngle, UnitsStr, VelocityFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:             

            ##########################################################################################################
            ##########################################################################################################
            if VelocityFlag == 0:

                ##########################################################################################################
                ConvertedValuesDict =  dict([("PhidgetsUnits", -11111.0),
                                            ("Deg", -11111.0),
                                            ("Rad", -11111.0),
                                            ("Rev", -11111.0)])

                if UnitsStr not in self.Position_ListOfAcceptableUnitString:
                    print("ConvertAngleToAllUnits: Error, Units must be in " + str(self.Position_ListOfAcceptableUnitString))
                    return ConvertedValuesDict
                ##########################################################################################################
                
            else:
                ##########################################################################################################
                ConvertedValuesDict =  dict([("PhidgetsUnitsPerSec", -11111.0),
                                            ("DegPerSec", -11111.0),
                                            ("RadPerSec", -11111.0),
                                            ("RevPerSec", -11111.0)])
                
                if UnitsStr not in self.Velocity_ListOfAcceptableUnitString:
                    print("ConvertAngleToAllUnits: Error, Units must be in " + str(self.Velocity_ListOfAcceptableUnitString))
                    return ConvertedValuesDict
                ##########################################################################################################

            InputAngle = float(InputAngle)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            if UnitsStr.find("PhidgetsUnits") != -1: #Could include velocity units wqith "PerSec" in it.
                ConvertedValue_PhidgetsUnits = InputAngle
                ConvertedValue_Deg = self.DegPerStep*(ConvertedValue_PhidgetsUnits/self.MicrostepsPerStep)
                ConvertedValue_Rev = ConvertedValue_Deg / 360.0
                ConvertedValue_Rad = ConvertedValue_Rev * 2.0 * math.pi
            ##########################################################################################################

            ##########################################################################################################
            elif UnitsStr.find("Deg") != -1: #Could include velocity units wqith "PerSec" in it.
                ConvertedValue_Deg = InputAngle
                ConvertedValue_PhidgetsUnits = self.MicrostepsPerStep*(ConvertedValue_Deg/self.DegPerStep)
                ConvertedValue_Rev = ConvertedValue_Deg / 360.0
                ConvertedValue_Rad = ConvertedValue_Rev * 2.0 * math.pi
            ##########################################################################################################

            ##########################################################################################################
            elif UnitsStr.find("Rad") != -1: #Could include velocity units wqith "PerSec" in it.
                ConvertedValue_Rad = InputAngle
                ConvertedValue_Deg = ConvertedValue_Rad*180.0/math.pi
                ConvertedValue_Rev = ConvertedValue_Deg/360.0
                ConvertedValue_PhidgetsUnits = self.MicrostepsPerStep*(ConvertedValue_Deg/self.DegPerStep)
            ##########################################################################################################

            ##########################################################################################################
            elif UnitsStr.find("Rev") != -1: #Could include velocity units wqith "PerSec" in it.
                ConvertedValue_Rev = InputAngle
                ConvertedValue_Rad = ConvertedValue_Rev*2.0*math.pi
                ConvertedValue_Deg = ConvertedValue_Rev*360.0
                ConvertedValue_PhidgetsUnits = self.MicrostepsPerStep*(ConvertedValue_Deg/self.DegPerStep)
            ##########################################################################################################

            ##########################################################################################################
            else:
                pass
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if VelocityFlag == 0:
                ConvertedValuesDict = dict([("PhidgetsUnits", ConvertedValue_PhidgetsUnits),
                                            ("Deg", ConvertedValue_Deg),
                                            ("Rad", ConvertedValue_Rad),
                                            ("Rev", ConvertedValue_Rev)])
            else:
                ConvertedValuesDict = dict([("PhidgetsUnitsPerSec", ConvertedValue_PhidgetsUnits),
                                            ("DegPerSec", ConvertedValue_Deg),
                                            ("RadPerSec", ConvertedValue_Rad),
                                            ("RevPerSec", ConvertedValue_Rev)])
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            return ConvertedValuesDict
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("ConvertPositionToAllUnits InputAngle: " + str(InputAngle) + ", exceptions: %s" % exceptions)
            #traceback.print_exc()
            return ConvertedValuesDict
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SetZeroPosition(self):

        try:

            self.ZeroPosition_NeedsToBeSetFlag = 1

        except:
            exceptions = sys.exc_info()[0]
            print("SetZeroPosition, exceptions: %s" % exceptions)
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __SetZeroPosition(self, PrintInfoForDebuggingFlag = 0):

        try:
            if self.PhidgetsDeviceConnectedFlag == 1:
                
                self.Stepper_Object.addPositionOffset(-1*self.Stepper_Object.getPosition())

                self.Position_Actual_PhidgetsUnits = self.Stepper_Object.getPosition()

                self.Position_Actual_AllUnitsDict = self.ConvertAngleToAllUnits(self.Position_Actual_PhidgetsUnits, "PhidgetsUnits", VelocityFlag=0)

                self.Position_ToBeSet_PhidgetsUnits = 0
                self.Position_GUIscale_NeedsToBeSetFlag = 1

                if PrintInfoForDebuggingFlag == 1: print("__SetZeroPosition event fired for self.ZeroPosition_ToBeSet = " + str(self.ZeroPosition_ToBeSet))

        except:
            exceptions = sys.exc_info()[0]
            print("__SetZeroPosition, exceptions: %s" % exceptions)
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SetEngagedState(self, EngagedState_ToBeSet):

        try:
                EngagedState_ToBeSet_TEMP = int(EngagedState_ToBeSet)

                if EngagedState_ToBeSet_TEMP in [0, 1]:

                    self.EngagedState_ToBeSet = EngagedState_ToBeSet_TEMP
                    self.EngagedState_NeedsToBeSetFlag = 1

                else:
                    print("SetEngagedState: Error, EngagedState_ToBeSet must be 0 or 1.")

        except:
            exceptions = sys.exc_info()[0]
            print("SetEngagedState, exceptions: %s" % exceptions)
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __SetEngagedState(self, EngagedState_ToBeSet, PrintInfoForDebuggingFlag = 0):

        try:
            if self.PhidgetsDeviceConnectedFlag == 1:
                EngagedState_ToBeSet_TEMP = int(EngagedState_ToBeSet)

                if EngagedState_ToBeSet_TEMP in [0, 1]:
                    self.EngagedState_ToBeSet = EngagedState_ToBeSet_TEMP

                    self.Stepper_Object.setEngaged(self.EngagedState_ToBeSet)

                    self.EngagedState_Actual = self.Stepper_Object.getEngaged()

                    if PrintInfoForDebuggingFlag == 1: print("__SetEngagedState event fired for self.EngagedState_ToBeSet = " + str(self.EngagedState_ToBeSet))

                else:
                    print("__SetEngagedState: Error, EngagedState_ToBeSet must be 0 or 1.")

        except:
            exceptions = sys.exc_info()[0]
            print("__SetEngagedState, exceptions: %s" % exceptions)
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SetPosition(self, Position_ToBeSet, UnitsStr):

        try:

            ##########################################################################################################
            if UnitsStr not in self.Position_ListOfAcceptableUnitString:
                print("SetPosition: Error, Units must be in " + str(self.Position_ListOfAcceptableUnitString))
            ##########################################################################################################

            Position_ToBeSet_PhidgetsUnits_TEMP = self.ConvertAngleToAllUnits(Position_ToBeSet, UnitsStr, VelocityFlag=0)["PhidgetsUnits"]

            self.Position_ToBeSet_PhidgetsUnits = int(self.LimitNumber_FloatOutputOnly(self.Position_Min_PhidgetsUnits_UserSet, #based on USER limits
                                                                                             self.Position_Max_PhidgetsUnits_UserSet,
                                                                                             Position_ToBeSet_PhidgetsUnits_TEMP))
            self.Position_NeedsToBeSetFlag = 1
            self.Position_GUIscale_NeedsToBeSetFlag = 1

        except:
            exceptions = sys.exc_info()[0]
            print("SetPosition, exceptions: %s" % exceptions)
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __SetPosition(self, Position_ToBeSet_PhidgetsUnits, PrintInfoForDebuggingFlag = 0):

        try:
            if self.PhidgetsDeviceConnectedFlag == 1:

                Position_ToBeSet_PhidgetsUnits_TEMP = int(self.LimitNumber_FloatOutputOnly(self.Stepper_ImmutableLimitsReadFromDevice["Position_Min_PhidgetsUnits"], #based on DEVICE limits
                                                                                               self.Stepper_ImmutableLimitsReadFromDevice["Position_Max_PhidgetsUnits"],
                                                                                               Position_ToBeSet_PhidgetsUnits))

                self.Position_ToBeSet_PhidgetsUnits = Position_ToBeSet_PhidgetsUnits_TEMP

                self.MotionIsStoppedFlag_Actual = 0

                self.Stepper_Object.setTargetPosition(Position_ToBeSet_PhidgetsUnits_TEMP)

                if PrintInfoForDebuggingFlag == 1: print("__SetPosition event fired for self.Position_ToBeSet_PhidgetsUnits = " + str(self.Position_ToBeSet_PhidgetsUnits))

        except:
            exceptions = sys.exc_info()[0]
            print("__SetPosition, exceptions: %s" % exceptions)
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SetVelocityLimit(self, VelocityLimit_ToBeSet_PhidgetsUnits):

        try:
            self.VelocityLimit_ToBeSet_PhidgetsUnits = int(self.LimitNumber_FloatOutputOnly(self.VelocityLimit_Min_PhidgetsUnits_UserSet, #based on USER limits
                                                                                         self.VelocityLimit_Max_PhidgetsUnits_UserSet,
                                                                                         VelocityLimit_ToBeSet_PhidgetsUnits))

            self.VelocityLimit_NeedsToBeSetFlag = 1
            self.VelocityLimit_GUIscale_NeedsToBeSetFlag = 1

        except:
            exceptions = sys.exc_info()[0]
            print("SetVelocityLimit, exceptions: %s" % exceptions)
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __SetVelocityLimit(self, VelocityLimit_ToBeSet_PhidgetsUnits, PrintInfoForDebuggingFlag = 0):

        try:
            if self.PhidgetsDeviceConnectedFlag == 1:

                self.VelocityLimit_ToBeSet = int(self.LimitNumber_FloatOutputOnly(self.Stepper_ImmutableLimitsReadFromDevice["VelocityLimit_Min_PhidgetsUnits"], #based on DEVICE limits
                                                                                   self.Stepper_ImmutableLimitsReadFromDevice["VelocityLimit_Max_PhidgetsUnits"],
                                                                                   VelocityLimit_ToBeSet_PhidgetsUnits))

                self.VelocityLimit_Actual_PhidgetsUnits = self.Stepper_Object.getVelocityLimit()

                self.Stepper_Object.setVelocityLimit(self.VelocityLimit_ToBeSet)

                if PrintInfoForDebuggingFlag == 1: print("__SetVelocityLimit event fired for self.VelocityLimit_ToBeSet = " + str(self.VelocityLimit_ToBeSet))

        except:
            exceptions = sys.exc_info()[0]
            print("__SetVelocityLimit, exceptions: %s" % exceptions)
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SetAcceleration(self, Acceleration_ToBeSet_PhidgetsUnits):

        try:
            self.Acceleration_ToBeSet_PhidgetsUnits = int(self.LimitNumber_FloatOutputOnly(self.Acceleration_Min_PhidgetsUnits_UserSet, #based on USER limits
                                                                                         self.Acceleration_Max_PhidgetsUnits_UserSet,
                                                                                         Acceleration_ToBeSet_PhidgetsUnits))

            self.Acceleration_NeedsToBeSetFlag = 1
            self.Acceleration_GUIscale_NeedsToBeSetFlag = 1

        except:
            exceptions = sys.exc_info()[0]
            print("SetAcceleration, exceptions: %s" % exceptions)
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __SetAcceleration(self, Acceleration_ToBeSet_PhidgetsUnits, PrintInfoForDebuggingFlag = 0):

        try:
            if self.PhidgetsDeviceConnectedFlag == 1:

                self.Acceleration_ToBeSet = int(self.LimitNumber_FloatOutputOnly(self.Stepper_ImmutableLimitsReadFromDevice["Acceleration_Min_PhidgetsUnits"], #based on DEVICE limits
                                                                                   self.Stepper_ImmutableLimitsReadFromDevice["Acceleration_Max_PhidgetsUnits"],
                                                                                   Acceleration_ToBeSet_PhidgetsUnits))

                self.Stepper_Object.setAcceleration(self.Acceleration_ToBeSet)

                self.Acceleration_Actual_PhidgetsUnits = self.Stepper_Object.getAcceleration()

                if PrintInfoForDebuggingFlag == 1: print("__SetAcceleration event fired for self.Acceleration_ToBeSet = " + str(self.Acceleration_ToBeSet))

        except:
            exceptions = sys.exc_info()[0]
            print("__SetAcceleration, exceptions: %s" % exceptions)
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SetCurrentLimit(self, CurrentLimit_ToBeSet_PhidgetsUnits):

        try:
            self.CurrentLimit_ToBeSet_PhidgetsUnits = int(self.LimitNumber_FloatOutputOnly(self.CurrentLimit_Min_PhidgetsUnits_UserSet, #based on USER limits
                                                                                         self.CurrentLimit_Max_PhidgetsUnits_UserSet,
                                                                                         CurrentLimit_ToBeSet_PhidgetsUnits))

            self.CurrentLimit_NeedsToBeSetFlag = 1
            self.CurrentLimit_GUIscale_NeedsToBeSetFlag = 1

        except:
            exceptions = sys.exc_info()[0]
            print("SetCurrentLimit, exceptions: %s" % exceptions)
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __SetCurrentLimit(self, CurrentLimit_ToBeSet_PhidgetsUnits, PrintInfoForDebuggingFlag = 0):

        try:
            if self.PhidgetsDeviceConnectedFlag == 1:

                self.CurrentLimit_ToBeSet = self.LimitNumber_FloatOutputOnly(self.Stepper_ImmutableLimitsReadFromDevice["CurrentLimit_Min_PhidgetsUnits"], #based on DEVICE limits
                                                                                   self.Stepper_ImmutableLimitsReadFromDevice["CurrentLimit_Max_PhidgetsUnits"],
                                                                                   CurrentLimit_ToBeSet_PhidgetsUnits)

                self.Stepper_Object.setCurrentLimit(self.CurrentLimit_ToBeSet)

                self.CurrentLimit_Actual_PhidgetsUnits = self.Stepper_Object.getCurrentLimit()

                if PrintInfoForDebuggingFlag == 1: print("__SetCurrentLimit event fired for self.CurrentLimit_ToBeSet = " + str(self.CurrentLimit_ToBeSet))

        except:
            exceptions = sys.exc_info()[0]
            print("__SetCurrentLimit, exceptions: %s" % exceptions)
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SetHoldingCurrentLimit(self, HoldingCurrentLimit_ToBeSet_PhidgetsUnits):

        try:
            self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits = int(self.LimitNumber_FloatOutputOnly(self.HoldingCurrentLimit_Min_PhidgetsUnits_UserSet, #based on USER limits
                                                                                                     self.HoldingCurrentLimit_Max_PhidgetsUnits_UserSet,
                                                                                                     HoldingCurrentLimit_ToBeSet_PhidgetsUnits))

            self.HoldingCurrentLimit_NeedsToBeSetFlag = 1
            self.HoldingCurrentLimit_GUIscale_NeedsToBeSetFlag = 1

        except:
            exceptions = sys.exc_info()[0]
            print("SetHoldingCurrentLimit, exceptions: %s" % exceptions)
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __SetHoldingCurrentLimit(self, HoldingCurrentLimit_ToBeSet_PhidgetsUnits, PrintInfoForDebuggingFlag = 0):

        try:
            if self.PhidgetsDeviceConnectedFlag == 1:

                self.HoldingCurrentLimit_ToBeSet = self.LimitNumber_FloatOutputOnly(self.Stepper_ImmutableLimitsReadFromDevice["HoldingCurrentLimit_Min_PhidgetsUnits"], #based on DEVICE limits
                                                                                   self.Stepper_ImmutableLimitsReadFromDevice["HoldingCurrentLimit_Max_PhidgetsUnits"],
                                                                                   HoldingCurrentLimit_ToBeSet_PhidgetsUnits)

                self.Stepper_Object.setHoldingCurrentLimit(self.HoldingCurrentLimit_ToBeSet)

                self.HoldingCurrentLimit_Actual_PhidgetsUnits = self.Stepper_Object.getHoldingCurrentLimit()

                if PrintInfoForDebuggingFlag == 1: print("__SetHoldingCurrentLimit event fired for self.HoldingCurrentLimit_ToBeSet = " + str(self.HoldingCurrentLimit_ToBeSet))

        except:
            exceptions = sys.exc_info()[0]
            print("__SetHoldingCurrentLimit, exceptions: %s" % exceptions)
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for PhidgetStepperControllerVINT_ReubenPython3Class object.")
        self.MainThread_StillRunningFlag = 1

        self.SetPosition(self.Position_ToBeSet_PhidgetsUnits, "PhidgetsUnits")
        self.SetVelocityLimit(self.VelocityLimit_ToBeSet_PhidgetsUnits)
        self.SetAcceleration(self.Acceleration_ToBeSet_PhidgetsUnits)
        self.SetCurrentLimit(self.CurrentLimit_ToBeSet_PhidgetsUnits)
        self.SetHoldingCurrentLimit(self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits)

        if self.FailsafeEnabledFlag == 1:
            self.Stepper_Object.enableFailsafe(int(self.FailsafeTime_Milliseconds))

        if self.EngageMotorOnAttachFlag == 1:
            self.SetEngagedState(1)

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            try:

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                try:
                    self.EngagedState_Actual = self.Stepper_Object.getEngaged()
                except:
                    self.EngagedState_Actual = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.FailsafeEnabledFlag == 1:
                    try:
                        self.Stepper_Object.resetFailsafe()
                    except:
                        print("PhidgetStepperControllerVINT_ReubenPython3Class, resetFailsafe() exception")
                        self.Stepper_Object.enableFailsafe(self.FailsafeTime_Milliseconds)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.ZeroPosition_NeedsToBeSetFlag == 1:
                    self.__SetZeroPosition(PrintInfoForDebuggingFlag=0)
                    self.ZeroPosition_NeedsToBeSetFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.EngagedState_NeedsToBeSetFlag == 1:
                    self.__SetEngagedState(self.EngagedState_ToBeSet, PrintInfoForDebuggingFlag=0)
                    self.EngagedState_NeedsToBeSetFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.VelocityLimit_NeedsToBeSetFlag == 1:
                    self.__SetVelocityLimit(self.VelocityLimit_ToBeSet_PhidgetsUnits, PrintInfoForDebuggingFlag=0)
                    self.VelocityLimit_NeedsToBeSetFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.Acceleration_NeedsToBeSetFlag == 1:
                    self.__SetAcceleration(self.Acceleration_ToBeSet_PhidgetsUnits, PrintInfoForDebuggingFlag=1)
                    self.Acceleration_NeedsToBeSetFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.CurrentLimit_NeedsToBeSetFlag == 1:
                    self.__SetCurrentLimit(self.CurrentLimit_ToBeSet_PhidgetsUnits, PrintInfoForDebuggingFlag=1)
                    self.CurrentLimit_NeedsToBeSetFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.HoldingCurrentLimit_NeedsToBeSetFlag == 1:
                    self.__SetHoldingCurrentLimit(self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits, PrintInfoForDebuggingFlag=1)
                    self.HoldingCurrentLimit_NeedsToBeSetFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.Position_NeedsToBeSetFlag == 1:
                    self.__SetPosition(self.Position_ToBeSet_PhidgetsUnits, PrintInfoForDebuggingFlag=0)
                    self.Position_NeedsToBeSetFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                self.MostRecentDataDict["Time"] = self.CurrentTime_CalculatedFromMainThread

                self.MostRecentDataDict["CurrentTime_CalculatedFromMainThread"] = self.CurrentTime_CalculatedFromMainThread
                self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromMainThread"] = self.DataStreamingFrequency_CalculatedFromMainThread

                self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromPositionChangeCallback"] = self.DataStreamingFrequency_CalculatedFromPositionChangeCallback

                self.MostRecentDataDict["Stepper_ImmutableLimitsReadFromDevice"] = self.Stepper_ImmutableLimitsReadFromDevice

                self.MostRecentDataDict["Stepper_ChangeableSettingsReadFromDevice"] = self.Stepper_ChangeableSettingsReadFromDevice

                self.MostRecentDataDict["EngagedState_Actual"] = self.EngagedState_Actual
                self.MostRecentDataDict["VelocityLimit_Actual_PhidgetsUnits"] = self.VelocityLimit_Actual_PhidgetsUnits
                self.MostRecentDataDict["CurrentLimit_Actual_PhidgetsUnits"] = self.CurrentLimit_Actual_PhidgetsUnits
                self.MostRecentDataDict["HoldingCurrentLimit_Actual_PhidgetsUnits"] = self.HoldingCurrentLimit_Actual_PhidgetsUnits

                self.MostRecentDataDict["Position_ToBeSet_AllUnitsDict"] = self.ConvertAngleToAllUnits(self.Position_ToBeSet_PhidgetsUnits, "PhidgetsUnits", VelocityFlag=0)
                self.MostRecentDataDict["Position_Actual_AllUnitsDict"] = self.Position_Actual_AllUnitsDict
                self.MostRecentDataDict["Velocity_Actual_AllUnitsDict"] = self.Velocity_Actual_AllUnitsDict
                self.MostRecentDataDict["Acceleration_Actual_PhidgetsUnits"] = self.Acceleration_Actual_PhidgetsUnits

                self.MostRecentDataDict["MotionIsStoppedFlag_Actual"] = self.MotionIsStoppedFlag_Actual
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.UpdateFrequencyCalculation_MainThread_Filtered()

                if self.MainThread_TimeToSleepEachLoop > 0.0:
                    if self.MainThread_TimeToSleepEachLoop > 0.001:
                        time.sleep(self.MainThread_TimeToSleepEachLoop - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                    else:
                        time.sleep(self.MainThread_TimeToSleepEachLoop)
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("MainThread, exceptions: %s" % exceptions)
                traceback.print_exc()

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:
            self.CloseDevice()

        except:
            pass

        self.MyPrint_WithoutLogFile("Finished MainThread for PhidgetStepperControllerVINT_ReubenPython3Class object.")
        self.MainThread_StillRunningFlag = 0
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CloseDevice(self):

        try:

            self.Stepper_Object.close()

            print("PhidgetStepperControllerVINT_ReubenPython3Class: CloseDevice, event fired!")

        except:
            exceptions = sys.exc_info()[0]
            print("PhidgetStepperControllerVINT_ReubenPython3Class: CloseDevice, Exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for PhidgetStepperControllerVINT_ReubenPython3Class object")

        self.EXIT_PROGRAM_FLAG = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent):

        self.GUI_Thread(GuiParent)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent):

        print("Starting the GUI_Thread for PhidgetStepperControllerVINT_ReubenPython3Class object.")

        #################################################
        #################################################
        #################################################
        self.root = parent
        self.parent = parent
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.TkinterScaleLabelWidth = 30
        self.TkinterScaleWidth = 10
        self.TkinterScaleLength = 250
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=50)

        self.DeviceInfo_Label["text"] = self.NameToDisplay_UserSet + \
                                         "\nDevice Name: " + self.DetectedDeviceName + \
                                         "\nVINT SerialNumber: " + str(self.VINT_DetectedSerialNumber) + \
                                         "\nDeviceID: " + str(self.DetectedDeviceID) + \
                                         "\nFW Ver: " + str(self.DetectedDeviceVersion) + \
                                         "\nLibrary Ver: " + str(self.DetectedDeviceLibraryVersion)

        self.DeviceInfo_Label.grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        self.EngagedState_Button = Button(self.myFrame, text="Engaged", state="normal", width=20, command=lambda: self.EngagedState_ButtonResponse())
        self.EngagedState_Button.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################
        #################################################
        
        #################################################
        #################################################
        self.ZeroPosition_Button = Button(self.myFrame, text="ZeroPos", state="normal", width=20, command=lambda: self.ZeroPosition_ButtonResponse())
        self.ZeroPosition_Button.grid(row=1, column=1, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.Data_Label = Label(self.myFrame, text="Data_Label", width=120)
        self.Data_Label.grid(row=2, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=10, rowspan=1)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.AllScalesFrame = Frame(self.myFrame)
        self.AllScalesFrame.grid(row=3, column=0, padx=1, pady=1, columnspan=1, rowspan=1, sticky="W")
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.Position_ToBeSet_PhidgetsUnits_ScaleLabel = Label(self.AllScalesFrame, text="Position", width=20)
        self.Position_ToBeSet_PhidgetsUnits_ScaleLabel.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        self.Position_ToBeSet_PhidgetsUnits_ScaleValue = DoubleVar()
        self.Position_ToBeSet_PhidgetsUnits_Scale = Scale(self.AllScalesFrame, \
                                            from_=self.Position_Min_PhidgetsUnits_UserSet,\
                                            to= self.Position_Max_PhidgetsUnits_UserSet,\
                                            #tickinterval=(self.Position_Max_PhidgetsUnits_UserSet - self.Position_Min_PhidgetsUnits_UserSet) / 2.0,\
                                            orient=HORIZONTAL,\
                                            borderwidth=2,\
                                            showvalue=1,\
                                            width=self.TkinterScaleWidth,\
                                            length=self.TkinterScaleLength,\
                                            resolution=1.0,\
                                            variable=self.Position_ToBeSet_PhidgetsUnits_ScaleValue)
        self.Position_ToBeSet_PhidgetsUnits_Scale.bind('<Button-1>', lambda event, name="Position": self.Position_ToBeSet_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Position_ToBeSet_PhidgetsUnits_Scale.bind('<B1-Motion>', lambda event, name="Position": self.Position_ToBeSet_PhidgetsUnits_ScaleResponse(event, name))
        self.Position_ToBeSet_PhidgetsUnits_Scale.bind('<ButtonRelease-1>', lambda event, name="Position": self.Position_ToBeSet_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Position_ToBeSet_PhidgetsUnits_Scale.set(self.Position_ToBeSet_PhidgetsUnits)
        self.Position_ToBeSet_PhidgetsUnits_Scale.grid(row=0, column=1, padx=1, pady=1, columnspan=2, rowspan=1)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.VelocityLimit_ToBeSet_PhidgetsUnits_ScaleLabel = Label(self.AllScalesFrame, text="Velocity", width=20)
        self.VelocityLimit_ToBeSet_PhidgetsUnits_ScaleLabel.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        self.VelocityLimit_ToBeSet_PhidgetsUnits_ScaleValue = DoubleVar()
        self.VelocityLimit_ToBeSet_PhidgetsUnits_Scale = Scale(self.AllScalesFrame, \
                                            from_=self.VelocityLimit_Min_PhidgetsUnits_UserSet,
                                            to=self.VelocityLimit_Max_PhidgetsUnits_UserSet, \
                                            #tickinterval=(self.VelocityLimit_Max_PhidgetsUnits_UserSet - self.VelocityLimit_Min_PhidgetsUnits_UserSet) / 2.0,\
                                            orient=HORIZONTAL,\
                                            borderwidth=2,\
                                            showvalue=1,\
                                            width=self.TkinterScaleWidth,\
                                            length=self.TkinterScaleLength,\
                                            resolution=0.001,\
                                            variable=self.VelocityLimit_ToBeSet_PhidgetsUnits_ScaleValue)
        self.VelocityLimit_ToBeSet_PhidgetsUnits_Scale.bind('<Button-1>', lambda event, name="Velocity": self.VelocityLimit_ToBeSet_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.VelocityLimit_ToBeSet_PhidgetsUnits_Scale.bind('<B1-Motion>', lambda event, name="Velocity": self.VelocityLimit_ToBeSet_PhidgetsUnits_ScaleResponse(event, name))
        self.VelocityLimit_ToBeSet_PhidgetsUnits_Scale.bind('<ButtonRelease-1>', lambda event, name="Velocity": self.VelocityLimit_ToBeSet_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.VelocityLimit_ToBeSet_PhidgetsUnits_Scale.set(self.VelocityLimit_ToBeSet_PhidgetsUnits)
        self.VelocityLimit_ToBeSet_PhidgetsUnits_Scale.grid(row=1, column=1, padx=1, pady=1, columnspan=2, rowspan=1)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.Acceleration_ToBeSet_PhidgetsUnits_ScaleLabel = Label(self.AllScalesFrame, text="Acceleration", width=20)
        self.Acceleration_ToBeSet_PhidgetsUnits_ScaleLabel.grid(row=2, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        self.Acceleration_ToBeSet_PhidgetsUnits_ScaleValue = DoubleVar()
        self.Acceleration_ToBeSet_PhidgetsUnits_Scale = Scale(self.AllScalesFrame, \
                                            from_=self.Acceleration_Min_PhidgetsUnits_UserSet,\
                                            to=self.Acceleration_Max_PhidgetsUnits_UserSet, \
                                            #tickinterval=(self.Acceleration_Max_PhidgetsUnits_UserSet - self.Acceleration_Min_PhidgetsUnits_UserSet) / 2.0,\
                                            orient=HORIZONTAL,\
                                            borderwidth=2,\
                                            showvalue=1,\
                                            width=self.TkinterScaleWidth,\
                                            length=self.TkinterScaleLength,\
                                            resolution=0.001,\
                                            variable=self.Acceleration_ToBeSet_PhidgetsUnits_ScaleValue)
        self.Acceleration_ToBeSet_PhidgetsUnits_Scale.bind('<Button-1>', lambda event, name="Acceleration": self.Acceleration_ToBeSet_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Acceleration_ToBeSet_PhidgetsUnits_Scale.bind('<B1-Motion>', lambda event, name="Acceleration": self.Acceleration_ToBeSet_PhidgetsUnits_ScaleResponse(event, name))
        self.Acceleration_ToBeSet_PhidgetsUnits_Scale.bind('<ButtonRelease-1>', lambda event, name="Acceleration": self.Acceleration_ToBeSet_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Acceleration_ToBeSet_PhidgetsUnits_Scale.set(self.Acceleration_ToBeSet_PhidgetsUnits)
        self.Acceleration_ToBeSet_PhidgetsUnits_Scale.grid(row=2, column=1, padx=1, pady=1, columnspan=2, rowspan=1)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.CurrentLimit_ToBeSet_PhidgetsUnits_ScaleLabel = Label(self.AllScalesFrame, text="CurrentLimit", width=20)
        self.CurrentLimit_ToBeSet_PhidgetsUnits_ScaleLabel.grid(row=3, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        self.CurrentLimit_ToBeSet_PhidgetsUnits_ScaleValue = DoubleVar()
        self.CurrentLimit_ToBeSet_PhidgetsUnits_Scale = Scale(self.AllScalesFrame, \
                                            from_=self.CurrentLimit_Min_PhidgetsUnits_UserSet,\
                                            to=self.CurrentLimit_Max_PhidgetsUnits_UserSet, \
                                            #tickinterval=(self.CurrentLimit_Max_PhidgetsUnits_UserSet - self.CurrentLimit_Min_PhidgetsUnits_UserSet) / 2.0,\
                                            orient=HORIZONTAL,\
                                            borderwidth=2,\
                                            showvalue=1,\
                                            width=self.TkinterScaleWidth,\
                                            length=self.TkinterScaleLength,\
                                            resolution=0.001,\
                                            variable=self.CurrentLimit_ToBeSet_PhidgetsUnits_ScaleValue)
        self.CurrentLimit_ToBeSet_PhidgetsUnits_Scale.bind('<Button-1>', lambda event, name="CurrentLimit": self.CurrentLimit_ToBeSet_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.CurrentLimit_ToBeSet_PhidgetsUnits_Scale.bind('<B1-Motion>', lambda event, name="CurrentLimit": self.CurrentLimit_ToBeSet_PhidgetsUnits_ScaleResponse(event, name))
        self.CurrentLimit_ToBeSet_PhidgetsUnits_Scale.bind('<ButtonRelease-1>', lambda event, name="CurrentLimit": self.CurrentLimit_ToBeSet_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.CurrentLimit_ToBeSet_PhidgetsUnits_Scale.set(self.CurrentLimit_ToBeSet_PhidgetsUnits)
        self.CurrentLimit_ToBeSet_PhidgetsUnits_Scale.grid(row=3, column=1, padx=1, pady=1, columnspan=2, rowspan=1)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_ScaleLabel = Label(self.AllScalesFrame, text="HoldingCurrentLimit", width=20)
        self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_ScaleLabel.grid(row=3, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_ScaleValue = DoubleVar()
        self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_Scale = Scale(self.AllScalesFrame, \
                                            from_=self.HoldingCurrentLimit_Min_PhidgetsUnits_UserSet,\
                                            to=self.HoldingCurrentLimit_Max_PhidgetsUnits_UserSet, \
                                            #tickinterval=(self.HoldingCurrentLimit_Max_PhidgetsUnits_UserSet - self.HoldingCurrentLimit_Min_PhidgetsUnits_UserSet) / 2.0,\
                                            orient=HORIZONTAL,\
                                            borderwidth=2,\
                                            showvalue=1,\
                                            width=self.TkinterScaleWidth,\
                                            length=self.TkinterScaleLength,\
                                            resolution=0.001,\
                                            variable=self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_ScaleValue)
        self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_Scale.bind('<Button-1>', lambda event, name="HoldingCurrentLimit": self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_Scale.bind('<B1-Motion>', lambda event, name="HoldingCurrentLimit": self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_ScaleResponse(event, name))
        self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_Scale.bind('<ButtonRelease-1>', lambda event, name="HoldingCurrentLimit": self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_Scale.set(self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits)
        self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_Scale.grid(row=3, column=1, padx=1, pady=1, columnspan=2, rowspan=1)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=3, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=10, rowspan=10)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################
        #################################################
        #################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Position_ToBeSet_PhidgetsUnits_ScaleResponse(self, event, name):

        self.Position_ToBeSet_PhidgetsUnits = float(self.Position_ToBeSet_PhidgetsUnits_ScaleValue.get())
        self.Position_NeedsToBeSetFlag = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VelocityLimit_ToBeSet_PhidgetsUnits_ScaleResponse(self, event, name):

        self.VelocityLimit_ToBeSet_PhidgetsUnits = float(self.VelocityLimit_ToBeSet_PhidgetsUnits_ScaleValue.get())
        self.VelocityLimit_NeedsToBeSetFlag = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Acceleration_ToBeSet_PhidgetsUnits_ScaleResponse(self, event, name):

        self.Acceleration_ToBeSet_PhidgetsUnits = self.Acceleration_ToBeSet_PhidgetsUnits_ScaleValue.get()
        self.Acceleration_NeedsToBeSetFlag = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CurrentLimit_ToBeSet_PhidgetsUnits_ScaleResponse(self, event, name):

        self.CurrentLimit_ToBeSet_PhidgetsUnits = self.CurrentLimit_ToBeSet_PhidgetsUnits_ScaleValue.get()
        self.CurrentLimit_NeedsToBeSetFlag = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def HoldingCurrentLimit_ToBeSet_PhidgetsUnits_ScaleResponse(self, event, name):

        self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits = self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_ScaleValue.get()
        self.HoldingCurrentLimit_NeedsToBeSetFlag = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EngagedState_ButtonResponse(self):

        if self.EngagedState_Actual == 1:
            self.EngagedState_ToBeSet = 0
        else:
            self.EngagedState_ToBeSet = 1

        self.EngagedState_NeedsToBeSetFlag = 1

        #print("EngagedState_Button_Response: Event fired!")
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def ZeroPosition_ButtonResponse(self):

        self.ZeroPosition_NeedsToBeSetFlag = 1

        #print("ZeroPosition_Button_Response: Event fired!")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                #######################################################
                #######################################################
                try:

                    #######################################################
                    #######################################################
                    #######################################################
                    self.Data_Label["text"] = self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict)
                    #######################################################
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    if self.EngagedState_Actual == 1:
                        TextToSet = "Engaged"
                        ColorToSet = self.TKinter_LightGreenColor

                    elif self.EngagedState_Actual == 0:
                        TextToSet = "Disabled"
                        ColorToSet= self.TKinter_LightRedColor

                    else:
                        TextToSet = "Enabled Unknown"
                        ColorToSet= self.TKinter_LightYellowColor
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    self.EngagedState_Button["text"] = TextToSet
                    self.EngagedState_Button["bg"] = ColorToSet

                    self.Position_ToBeSet_PhidgetsUnits_Scale["troughcolor"] = ColorToSet
                    self.VelocityLimit_ToBeSet_PhidgetsUnits_Scale["troughcolor"] = ColorToSet
                    self.Acceleration_ToBeSet_PhidgetsUnits_Scale["troughcolor"] = ColorToSet
                    self.CurrentLimit_ToBeSet_PhidgetsUnits_Scale["troughcolor"] = ColorToSet
                    self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_Scale["troughcolor"] = ColorToSet
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    #######################################################
                    if self.Position_GUIscale_NeedsToBeSetFlag == 1:
                        self.Position_ToBeSet_PhidgetsUnits_Scale.set(self.Position_ToBeSet_PhidgetsUnits)
                        self.Position_GUIscale_NeedsToBeSetFlag = 0

                    if self.VelocityLimit_GUIscale_NeedsToBeSetFlag == 1:
                        self.VelocityLimit_ToBeSet_PhidgetsUnits_Scale.set(self.VelocityLimit_ToBeSet_PhidgetsUnits)
                        self.VelocityLimit_GUIscale_NeedsToBeSetFlag = 0
                        
                    if self.Acceleration_GUIscale_NeedsToBeSetFlag == 1:
                        self.Acceleration_ToBeSet_PhidgetsUnits_Scale.set(self.Acceleration_ToBeSet_PhidgetsUnits)
                        self.Acceleration_GUIscale_NeedsToBeSetFlag = 0
                        
                    if self.CurrentLimit_GUIscale_NeedsToBeSetFlag == 1:
                        self.CurrentLimit_ToBeSet_PhidgetsUnits_Scale.set(self.CurrentLimit_ToBeSet_PhidgetsUnits)
                        self.CurrentLimit_GUIscale_NeedsToBeSetFlag = 0
                        
                    if self.HoldingCurrentLimit_GUIscale_NeedsToBeSetFlag == 1:
                        self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits_Scale.set(self.HoldingCurrentLimit_ToBeSet_PhidgetsUnits)
                        self.HoldingCurrentLimit_GUIscale_NeedsToBeSetFlag = 0
                    #######################################################
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    #######################################################
                    self.UpdateFrequencyCalculation_GUIthread_Filtered()
                    #######################################################
                    #######################################################
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("PhidgetStepperControllerVINT_ReubenPython3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

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
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

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

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertDictToProperlyFormattedStringForPrinting(self, DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

        try:
            ProperlyFormattedStringForPrinting = ""
            ItemsPerLineCounter = 0

            for Key in DictToPrint:

                ##########################################################################################################
                if isinstance(DictToPrint[Key], dict): #RECURSION
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                         str(Key) + ":\n" + \
                                                         self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key],
                                                                                                              NumberOfDecimalsPlaceToUse,
                                                                                                              NumberOfEntriesPerLine,
                                                                                                              NumberOfTabsBetweenItems)

                else:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                         str(Key) + ": " + \
                                                         self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key],
                                                                                                                                               0,
                                                                                                                                               NumberOfDecimalsPlaceToUse)
                ##########################################################################################################

                ##########################################################################################################
                if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                    ItemsPerLineCounter = ItemsPerLineCounter + 1
                else:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                    ItemsPerLineCounter = 0
                ##########################################################################################################

            return ProperlyFormattedStringForPrinting

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertDictToProperlyFormattedStringForPrinting, Exceptions: %s" % exceptions)
            return ""
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################