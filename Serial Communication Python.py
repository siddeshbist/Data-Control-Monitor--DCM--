import serial
import sys
import time
from appJar import gui
import os.path
import matplotlib.pyplot as plt

# Global Variables
usr = ""
credentials = {}

# Assigning inital state of variables
ser = serial.Serial('COM4', 115200, timeout=1)
list_serialIn = []
list_serialOut = []
vEgram = []
aEgram = []

# Creating/Accessing User/Pass Text File
if os.path.isfile('./creds.txt'):
    f = open('creds.txt', 'r')
    credentials = eval(f.readline())
    f.close()
else:
    f = open('creds.txt', 'w')
    f.close()


# Launching the GUI to Welcome Page
def launch(win):
    app.showSubWindow(win)


# Login Page Button Controls
def login(button):
    app.hide()
    if button == "Login":
        global usr
        usr = app.getEntry("Username")
        pwd = app.getEntry("Password")
        if usr in credentials:
            if pwd == credentials[usr]:
                app.hideSubWindow("Login Screen")
                app.setLabel("Username title", usr)

                if os.path.isfile('./' + usr + '.txt'):  # Setting previously Stored Data into appropriate Text Fields
                    g = open(usr + '.txt', 'r')
                    app.setOptionBox("p_pacingMode", list_pMode[int(g.readline().rstrip('\n'))])
                    app.setEntry("p_lowrateInterval", g.readline().rstrip('\n'))
                    app.setEntry("p_vPaceAmp", g.readline().rstrip('\n'))
                    app.setEntry("p_vPaceWidth", g.readline().rstrip('\n'))
                    app.setEntry("p_vVRP", g.readline().rstrip('\n'))
                    app.setEntry("p_aPaceAmp", g.readline().rstrip('\n'))
                    app.setEntry("p_aPaceWidth", g.readline().rstrip('\n'))
                    app.setEntry("p_aVRP", g.readline().rstrip('\n'))
                    g.close()
                else:
                    g = open(usr + '.txt', 'w')
                    g.write("0")
                    g.close()
                app.hide()
                app.showSubWindow("Parameters")
                app.setEntry("Password", "")
                app.setEntry("Username", "")
                print('success')
            else:
                app.infoBox("Message", "Invalid Password")
        else:
            app.infoBox("Message", "Username Does Not Exist Please Register")
    elif button == "Cancel":
        app.hideSubWindow("Login Screen")
        app.setEntry("Password", "")
        app.setEntry("Username", "")
        app.show()


# Register Page Button Controls
def register(button):
    app.hide()
    if button == "Register":  # Validate and Registers a New User
        usr2 = app.getEntry("New Username")
        pwd2 = app.getEntry("New Password")
        if len(credentials) == 10:
            print('max user level reached')
            app.setLabel("Register Info", "max user level reached")
        elif usr2 in credentials:
            app.setLabel("Register Info", "Username already exists")
        else:
            credentials[usr2] = pwd2
            g = open('creds.txt', 'w')
            g.write(str(credentials))
            g.close()
            app.hideSubWindow("Registration")
            app.setLabel("Register Info", "")
            app.setEntry("New Password", "")
            app.setEntry("New Username", "")
            app.show()
    elif button == "Go Back":
        app.hideSubWindow("Registration")
        app.setLabel("Register Info", "")
        app.setEntry("New Password", "")
        app.setEntry("New Username", "")
        app.show()


# Validating Ever Parameter before Sending/Storing data
def validParameters():
    valid = True;
    if not app.getEntry("p_lowrateInterval").isdigit():
        return False
    if not app.getEntry("p_vPaceAmp").isdigit():
        return False
    if not app.getEntry("p_vVRP").isdigit():
        return False
    if not app.getEntry("p_aPaceAmp").isdigit():
        return False
    if not app.getEntry("p_aVRP").isdigit():
        return False

    if (int(app.getEntry("p_lowrateInterval")) < 1) or (int(app.getEntry("p_lowrateInterval")) > 65535):
        valid = False;
    pli = int(app.getEntry("p_lowrateInterval"))
    if int(app.getEntry("p_vPaceAmp")) < 0 or int(app.getEntry("p_vPaceAmp")) > 100:
        valid = False;
    try:
        if int(app.getEntry("p_vPaceWidth")) < 0 or int(app.getEntry("p_vPaceWidth")) > pli:
            valid = False;
    except ValueError:
        valid = False;
    if int(app.getEntry("p_vVRP")) < 1 or int(app.getEntry("p_vVRP")) > pli:
        valid = False;
    if int(app.getEntry("p_aPaceAmp")) < 0 or int(app.getEntry("p_aPaceAmp")) > 100:
        valid = False;
    try:
        if int(app.getEntry("p_aPaceWidth")) < 0 or int(app.getEntry("p_aPaceWidth")) > pli:
            valid = False;
    except ValueError:
        valid = False;
    if int(app.getEntry("p_aVRP")) < 1 or int(app.getEntry("p_aVRP")) > pli:
        valid = False;

    return valid


# Parameters Page Button Controls
def parameters(button):
    app.hide()
    if button == "Update":
        if not validParameters():
            app.infoBox("Message", "Please Enter Parameters According to the Appropriate Range\nMake Sure to Enter "
                                   "Every Parameter")
        elif validParameters():
            list_serialOut = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22]
            g = open(usr + '.txt', 'w')
            # Storing Parameter Data for a specific User into a Text File
            g.writelines([str(list_pMode.index(app.getOptionBox("p_pacingMode"))), '\n',
                          app.getEntry("p_lowrateInterval"), '\n',
                          app.getEntry("p_vPaceAmp"), '\n',
                          app.getEntry("p_vPaceWidth"), '\n',
                          app.getEntry("p_vVRP"), '\n',
                          app.getEntry("p_aPaceAmp"), '\n',
                          app.getEntry("p_aPaceWidth"), '\n',
                          app.getEntry("p_aVRP"), '\n'])
            app.infoBox("Message", "Parameters Updated")
            g.close()

            # Converting Integer values to appropriate serial transmitting data input (1 or 2 bytes UINT8 & UINT16)
            list_serialOut[2] = list_pMode.index(app.getOptionBox("p_pacingMode"))

            list_serialOut[4] = int(int(app.getEntry("p_lowrateInterval")) / 256)
            list_serialOut[3] = int(int(app.getEntry("p_lowrateInterval")) - (list_serialOut[4] * 256))

            list_serialOut[6] = int(int(app.getEntry("p_vPaceAmp")) / 256)
            list_serialOut[5] = int(int(app.getEntry("p_vPaceAmp")) - (list_serialOut[6] * 256))

            list_serialOut[8] = int(int(app.getEntry("p_vPaceWidth")) / 256)
            list_serialOut[7] = int(int(app.getEntry("p_vPaceWidth")) - (list_serialOut[8] * 256))

            list_serialOut[10] = int(int(app.getEntry("p_vVRP")) / 256)
            list_serialOut[9] = int(int(app.getEntry("p_vVRP")) - (list_serialOut[10] * 256))

            list_serialOut[12] = int(int(app.getEntry("p_aPaceAmp")) / 256)
            list_serialOut[11] = int(int(app.getEntry("p_aPaceAmp")) - (list_serialOut[12] * 256))

            list_serialOut[14] = int(int(app.getEntry("p_aPaceWidth")) / 256)
            list_serialOut[13] = int(int(app.getEntry("p_aPaceWidth")) - (list_serialOut[14] * 256))

            list_serialOut[16] = int(int(app.getEntry("p_aVRP")) / 256)
            list_serialOut[15] = int(int(app.getEntry("p_aVRP")) - (list_serialOut[16] * 256))

            print(list_serialOut)

            # Executing Serial Write of Parameter Data
            for i in list_serialOut:
                ser.write(bytes([i]))
            time.sleep(0.5)

    elif button == "Request Parameters":
        list_serialIn = []
        arr = []
        arr.append(b'\x01')
        arr.append(b'\x00')
        for i in range(19):
            arr.append(b'\x01')
        arr.append(b'\x16')

        # Requesting Serial Data In
        for j in arr:
            ser.write(j)

        i = 1
        while i:  # Reading Serial Data of the requested in-device Parameteres

            s = ser.read()
            s = int.from_bytes(s, byteorder=sys.byteorder)
            list_serialIn.append(s)
            i += 1
            if i > 22:
                i = 0

        # Setting Text Fields with data recieved by converting data to appropriate Integer values.
        app.setOptionBox("p_pacingMode", list_pMode[int(list_serialIn[2])])
        app.setEntry("p_lowrateInterval", int(list_serialIn[3] + (list_serialIn[4] * 256)))
        app.setEntry("p_vPaceAmp", int(list_serialIn[5] + (list_serialIn[6] * 256)))
        app.setEntry("p_vPaceWidth", (list_serialIn[7] + (list_serialIn[8] * 256)))
        app.setEntry("p_vVRP", int(list_serialIn[9] + (list_serialIn[10] * 256)))
        app.setEntry("p_aPaceAmp", int(list_serialIn[11] + (list_serialIn[12] * 256)))
        app.setEntry("p_aPaceWidth", int(list_serialIn[13] + (list_serialIn[14] * 256)))
        app.setEntry("p_aVRP", int(list_serialIn[15] + (list_serialIn[16] * 256)))

    elif button == "E-GRAM":
        vEgram = []
        aEgram = []
        for x in range(10):  # Looping 10 times to obtain 10 distinct Data Points for E-GRAM Plots
            list_serialIn = []
            arr = []

            arr.append(b'\x01')
            arr.append(b'\x00')
            for i in range(19):
                arr.append(b'\x01')
            arr.append(b'\x16')

            # Requesting E-GRAM data values serially
            for j in arr:
                ser.write(j)

            i = 1
            while i:  # Reading Vent. and Atr. serial data

                s = ser.read()
                s = int.from_bytes(s, byteorder=sys.byteorder)
                list_serialIn.append(s)

                i += 1
                if i > 22:
                    i = 0
            time.sleep(0.5)

            # Storing converting and storing Serial Data into appropriate arrays
            vEgram.append((list_serialIn[17] + (list_serialIn[18] * 256)))
            aEgram.append((list_serialIn[19] + (list_serialIn[20] * 256)))

        # Ploting Ventricle and Atrium Array Data Points
        plt.figure(1)
        plt.subplot(211)
        plt.ylabel("Vent. Egram")
        plt.plot(vEgram)

        plt.subplot(212)
        plt.ylabel("Atr. Egram")
        plt.plot(aEgram)
        plt.show()

    # Logging Off User's Account
    elif button == "Log Off":
        app.hideSubWindow("Parameters")
        app.clearOptionBox("p_pacingMode", callFunction=True)
        app.setEntry("p_lowrateInterval", "")
        app.setEntry("p_vPaceAmp", "")
        app.setEntry("p_vPaceWidth", "")
        app.setEntry("p_vVRP", "")
        app.setEntry("p_aPaceAmp", "")
        app.setEntry("p_aPaceWidth", "")
        app.setEntry("p_aVRP", "")
        app.show()


# these go in the main window
app = gui()
app.addLabel("title", "Welcome to Kingdom Hearts")
app.setLabelBg("title", "red")
app.addButtons(["Login Screen", "Registration"], launch)
app.setSize(400, 200)

# Login Sub-Window
app.startSubWindow("Login Screen", modal=True)
app.setSticky("ew")
app.addLabel("Login title", "Please Login Screen")
app.setLabelBg("Login title", "red")
app.addLabelEntry("Username")
app.addLabelSecretEntry("Password")
app.addButtons(["Login", "Cancel"], login)
app.setSize(500, 500)
app.stopSubWindow()

# Register Sub-Window
app.startSubWindow("Registration", modal=True)
app.setSticky("ew")
app.addLabel("Register title", "Enter a New Username and Password")
app.setLabelBg("Register title", "red")
app.addLabelEntry("New Username")
app.addLabelSecretEntry("New Password")
app.addButtons(["Register", "Go Back"], register)
app.addLabel("Register Info", "")
app.setSize(500, 500)
app.stopSubWindow()

# Programmable Parameters Sub-Window
app.startSubWindow("Parameters", modal=True)
app.setSticky("ew")
app.addLabel("Username title", "")
app.setLabelBg("Username title", "red")
app.addLabel("Parameters title", "These are Your Programmable Parameters")
app.setLabelBg("Parameters title", "red")
list_pMode = ["off", "AAT", "VVT",
              "AOO", "AAI", "VOO", "VVI", "VDD",
              "DOO", "DDI", "DDD", "AOOR", "AAIR",
              "VOOR", "VVIR", "VDDR", "DOOR", "DDIR",
              "DDDR"]
app.addLabel("")
app.addLabelOptionBox("p_pacingMode", list_pMode)
app.addLabel(" ")
app.addLabelEntry("p_lowrateInterval")
app.addLabel("Value 1 - 65535 ms")
app.addLabel("  ")
app.addLabelEntry("p_vPaceAmp")
app.addLabel(" Value 0 - 100")
app.addLabel("   ")
app.addLabelEntry("p_vPaceWidth")
app.addLabel(" Value 0 - p_lowerInterval ms")
app.addLabel("    ")
app.addLabelEntry("p_vVRP")
app.addLabel(" Value 1 - p_lowerInterval ms")
app.addLabel("     ")
app.addLabelEntry("p_aPaceAmp")
app.addLabel("Value 0 - 100 ")
app.addLabel("      ")
app.addLabelEntry("p_aPaceWidth")
app.addLabel("Value 0 - p_lowerInterval ms")
app.addLabel("       ")
app.addLabelEntry("p_aVRP")
app.addLabel("Value 1 - p_lowerInterval ms")
app.addButtons(["Log Off", "E-GRAM", "Request Parameters", "Update"], parameters)
app.setSize(700, 700)
app.stopSubWindow()

app.go()
ser.close()
