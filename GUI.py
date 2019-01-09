from appJar import gui
import os.path

usr = ""
credentials = {}
if os.path.isfile('./creds.txt'):
    f = open('creds.txt', 'r')
    credentials = eval(f.readline())
    f.close()
else:
    f = open('creds.txt', 'w')
    f.close()


def launch(win):
    app.showSubWindow(win)


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

                if os.path.isfile('./'+usr+'.txt'):
                    g = open(usr+'.txt', 'r')
                    app.setEntry("p_pacingState", g.readline().rstrip('\n'))
                    app.setEntry("p_pacingMode", g.readline().rstrip('\n'))
                    app.setEntry("p_hysteresis", g.readline().rstrip('\n'))
                    app.setEntry("p_hysteresisInterval", g.readline().rstrip('\n'))
                    app.setEntry("p_lowrateInterval", g.readline().rstrip('\n'))
                    app.setEntry("p_vPaceAmp", g.readline().rstrip('\n'))
                    app.setEntry("p_vPaceWidth", g.readline().rstrip('\n'))
                    app.setEntry("p_vVRP", g.readline().rstrip('\n'))
                    g.close()
                else:
                    g = open(usr+'.txt', 'w')
                    g.close()
                app.hide()
                app.showSubWindow("Parameters")
                app.setEntry("Password", "")
                app.setEntry("Username", "")
                print('success')
            else:
                print('invalid username/password')
        else:
            print("username doesn't exist please register ")
    elif button == "Cancel":
        app.hideSubWindow("Login Screen")
        app.setEntry("Password", "")
        app.setEntry("Username", "")
        app.show()


def register(button):
    app.hide()
    if button == "Register":
        usr2 = app.getEntry("New Username")
        pwd2 = app.getEntry("New Password")
        if len(credentials) == 10:
            print('max user level reached')
            app.setLabel("Register Info", "max user level reached")
        elif usr2 in credentials:
            print('user name already exists')
            app.setLabel("Register Info", "user name already exists")
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


def parameters(button):
    app.hide()
    if button == "Update":
        g = open(usr+'.txt', 'w')
        g.writelines([app.getEntry("p_pacingState"), '\n',
                      app.getEntry("p_pacingMode"), '\n',
                      app.getEntry("p_hysteresis"), '\n',
                      app.getEntry("p_hysteresisInterval"), '\n',
                      app.getEntry("p_lowrateInterval"), '\n',
                      app.getEntry("p_vPaceAmp"), '\n',
                      app.getEntry("p_vPaceWidth"), '\n',
                      app.getEntry("p_vVRP"), '\n'])
        g.close()
        app.infoBox("Message", "Parameters Updated")
    elif button == "Log Off":
        app.hideSubWindow("Parameters")
        app.setEntry("p_pacingState", "")
        app.setEntry("p_pacingMode", "")
        app.setEntry("p_hysteresis", "")
        app.setEntry("p_hysteresisInterval", "")
        app.setEntry("p_lowrateInterval", "")
        app.setEntry("p_vPaceAmp", "")
        app.setEntry("p_vPaceWidth", "")
        app.setEntry("p_vVRP", "")
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
app.addLabelEntry("p_pacingState")
app.addLabelEntry("p_pacingMode")
app.addLabelEntry("p_hysteresis")
app.addLabelEntry("p_hysteresisInterval")
app.addLabelEntry("p_lowrateInterval")
app.addLabelEntry("p_vPaceAmp")
app.addLabelEntry("p_vPaceWidth")
app.addLabelEntry("p_vVRP")
app.addButtons(["Log Off", "Update"], parameters)
app.setSize(500, 500)
app.stopSubWindow()

app.go()
