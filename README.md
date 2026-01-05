###########################

PhidgetStepperControllerVINT_ReubenPython3Class

Control class (including ability to hook to Tkinter GUI) to interface with stepper motor controllers (VINT-interface only) from Phidgets.

https://www.phidgets.com/?prodid=1121

8A Stepper Phidget

ID: STC1002_0

https://www.phidgets.com/?prodid=1278

4A Stepper Phidget

ID: STC1005_0

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision F, 12/29/2025

Verified working on:

Python 3.11/12

Windows 10/11 64-bit

Note: For bipolar/2-phase 4-wire stepper motors with standard phase-wire-coloration, the color-code is: A = Red, A- = Blue, B = Green, and B- = Black.
When viewing the Phidgets controller from above with the wires going upwards into their screw-terminals, the wires appear in that order from left to right (red being left-most).

###########################

########################### Python module installation instructions, all OS's

PhidgetStepperControllerVINT_ReubenPython3Class, ListOfModuleDependencies: ['LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'numpy', 'Phidget22', 'ReubenGithubCodeModulePaths']

PhidgetStepperControllerVINT_ReubenPython3Class, ListOfModuleDependencies_TestProgram: ['EntryListWithBlinking_ReubenPython2and3Class', 'keyboard', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'ReubenGithubCodeModulePaths']

PhidgetStepperControllerVINT_ReubenPython3Class, ListOfModuleDependencies_NestedLayers: ['GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class', 'numpy', 'pexpect', 'psutil', 'pyautogui', 'ReubenGithubCodeModulePaths']

PhidgetStepperControllerVINT_ReubenPython3Class, ListOfModuleDependencies_All:['EntryListWithBlinking_ReubenPython2and3Class', 'GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class', 'keyboard', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'numpy', 'pexpect', 'Phidget22', 'psutil', 'pyautogui', 'ReubenGithubCodeModulePaths']

https://pypi.org/project/Phidget22/#files

To install the Python module using pip:

pip install Phidget22       (with "sudo" if on Linux/Raspberry Pi)

To install the Python module from the downloaded .tar.gz file, enter downloaded folder and type "python setup.py install"

###########################

########################### Library/driver installation instructions, Windows

https://www.phidgets.com/docs/OS_-_Windows

###########################

########################### Library/driver installation instructions, Linux (other than Raspberry Pi)

https://www.phidgets.com/docs/OS_-_Linux#Quick_Downloads

###########################

########################### Library/driver installation instructions, Raspberry Pi (models 2 and above)

https://www.phidgets.com/education/learn/getting-started-kit-tutorial/install-libraries/

curl -fsSL https://www.phidgets.com/downloads/setup_linux | sudo -E bash -

sudo apt-get install -y libphidget22

###########################
