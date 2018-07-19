from Adafruit_MotorHAT import Adafruit_DCMotor
from Adafruit_MotorHAT import Adafruit_MotorHAT
import Tkinter
import datetime

class MyGUI:
    
    def __init__(self):
        #creates a new window
        self.window = Tkinter.Tk()
        self.window.title("Succ Support")
        self.window.geometry("800x480")
        self.window.configure(background="#F4F4F2")
        #self.window.attributes("-fullscreen", True)

        #widgets
        self.photo = Tkinter.PhotoImage(file="SuccSupportBanner.gif")
        self.label0 = Tkinter.Label(self.window, image=self.photo)
        self.label0.pack()

        self.label1Text = 'Time: '
        self.label1 = Tkinter.Label(self.window, text=self.label1Text, fg="#4C4C4C", bg="#F4F4F2")
        self.label1.config(font=("Arial", 15))
        self.label1.place(relx=0.5, rely=0.375, anchor='center')

        #self.label2Text = 'Watered: '
        #self.label2 = Tkinter.Label(self.window, text=self.label2Text, fg="#4C4C4C", bg="#F4F4F2")
        #self.label2.config(font=("Arial", 15))
        #self.label2.place(relx=0.5, rely=0.625, anchor='center')

        self.label3Text = 'Next Water: '
        self.label3 = Tkinter.Label(self.window, text=self.label3Text, fg="#4C4C4C", bg="#F4F4F2")
        self.label3.config(font=("Arial", 15))
        self.label3.place(relx=0.5, rely=0.5, anchor='center')

        self.scheduleEntry = Tkinter.Entry(self.window, width=2, fg="#4C4C4C")
        self.scheduleEntry.config(font=("Arial", 15))
        self.scheduleEntry.place(relx=0.45, rely=0.625, anchor='e')
        
        self.label4 = Tkinter.Label(self.window, text='Days Between Water: ', fg="#4C4C4C", bg="#F4F4F2")
        self.label4.config(font=("Arial", 15))
        self.label4.place(relx=0.4, rely=0.625, anchor='e')
        
        #400ml/min
        #500ml in a bottle
        self.waterVolumeSlider = Tkinter.Scale(self.window, from_=0, to=500, orient='horizontal', length=200, fg="#4C4C4C", bg="#F4F4F2")
        self.waterVolumeSlider.config(font=("Arial", 12))
        self.waterVolumeSlider.place(relx=0.55, rely=0.625, anchor='w')
        
        self.label5 = Tkinter.Label(self.window, text='ML', fg="#4C4C4C", bg="#F4F4F2")
        self.label5.config(font=("Arial", 15))
        self.label5.place(relx=0.825, rely=0.625, anchor='w')
        
        self.submitButton = Tkinter.Button(self.window, command=self.submitButtonPress, text='Submit', fg="#4C4C4C", bg="#F4F4F2")
        self.submitButton.config(font=("Arial", 12))
        self.submitButton.place(relx=0.475, rely=0.75, anchor='e')
        
        self.cancelButton = Tkinter.Button(self.window, command=self.cancelButtonPress, text='Cancel', fg="#4C4C4C", bg="#F4F4F2")
        self.cancelButton.config(font=("Arial", 12))
        self.cancelButton.place(relx=0.525, rely=0.75, anchor='w')
        
        self.waterButton = Tkinter.Button(self.window, command=self.waterButtonPress, text='Water', fg="#001ECC", bg="#F4F4F2")
        self.waterButton.config(font=("Arial", 12))
        self.waterButton.place(relx=0.5, rely=0.875, anchor='center')

        #opens file
        self.openFile()
        
        #sets scheduleEntry to current schedule if no widget is selected
        self.window.bind("<FocusIn>", self.updateScheduleEntry)
        
        #draw the window
        self.updateTime()
        self.window.mainloop()

    def updateTime(self):
        #called every second, updates clock
        self.currentTime = str(datetime.datetime.now())[:-7]
        self.label1.configure(text='Time: ' + self.currentTime)
        self.window.after(1, self.updateTime)
        self.checkTimeForWater()

    def water(self):
        #waters plant, updates then calls for updating next water time
        self.wateredTime = str(datetime.datetime.now())[:-7]
        print "watering..." + " | " + str(self.wateredTime) 
        
        #self.label2.configure(text = 'Watered: ' + self.wateredTime)
        self.updateWaterDateFile()
        self.updateNextWater()
        self.window.configure(background="#A8C5EF")
        self.window.after(3, self.window.configure(background="#F4F4F2"))
        
        #adds water time to waterLog file
        file = open("waterLog.txt", "a")
        file.write(str(self.wateredTime) + " | watered " + str(self.waterVolume) + " ml" + "\n")
    
    def openFile(self):
        #opens or creates a new file
        file = open("waterDate.txt", "r")
        #if there is not a previous water date, waters and records date
        if len(str(file.read())) < 5:
            file.close()
            self.water()
            file = open("waterDate.txt", "w")
            file.write(str(datetime.datetime.now())[:-7])
            print "no water date detected, setting to now"
            file.close()
        else:
            file = open("waterDate.txt", "r")
            self.wateredTime = str(file.read())
            #self.label2.configure(text = 'Watered: ' + self.wateredTime)
            file.close()
            print "water date loaded"
        
        #if there is not a water schedule, sets it to 7
        file = open("waterSchedule.txt", "r")
        if(len(file.read()) == 0):
            file.close()
            file = open("waterSchedule.txt", "w")
            file.write('7')
            print "no schedule detected, set to 7"
        else:
            print "schedule loaded"
        file.close()
        
        self.updateNextWater()
        
        #sets water volume slider to file
        file = open("waterVolume.txt", "r")
        file.seek(0,0)
        self.wvo = file.read()
        print "water volume file: " + self.wvo
        if(len(self.wvo) > 0):
            print "water volume loaded"
            if(int(self.wvo) >= 0 and int(self.wvo) < 401):
                self.waterVolume = int(self.wvo)
                print "WATER VOLUME WAS SET BABY " + self.wvo
            else:
                print self.wvo + " water volume value extraneous, set to 200"
                self.waterVolume = 200
                self.updateWaterVolumeFile()
        else:
            print "not volume found, set to 200"
            self.waterVolume = 200
            self.updateWaterVolumeFile()
            
        self.waterVolumeSlider.set(self.waterVolume)
        
    def updateNextWater(self):
        #updates next water time
        wateredSecond = self.wateredTime[-2:] 
        wateredMinute = self.wateredTime[-5:-3]
        wateredHour = self.wateredTime[-8:-6]

        wateredDay = self.wateredTime[8:10]
        wateredMonth = self.wateredTime[5:7]
        wateredYear = self.wateredTime[0:4]

        #sets timedelta based off of schedule file
        file = open("waterSchedule.txt", 'r')
        self.scheduleFileOutput = file.read()
        print "schedule file: " + self.scheduleFileOutput
        if(len(self.scheduleFileOutput) >= 1):
            self.daysDelta = int(self.scheduleFileOutput)
        else:
            print "no schedule file, set to 7"
            self.daysDelta = 7
        file.close()

        self.wateredDateTime = datetime.datetime.strptime(str(wateredYear + '-' + wateredMonth + '-' + wateredDay + ' ' + wateredHour + ':' + wateredMinute + ':' + wateredSecond), "%Y-%m-%d %H:%M:%S")
        self.nextWaterDateTime = self.wateredDateTime + datetime.timedelta(days=self.daysDelta)
        self.label3.configure(text='Next Water: ' + str(self.nextWaterDateTime))

    def updateWaterDateFile(self):
        #updates file with last watered date
        file = open("waterDate.txt", "w")
        file.write(str(self.wateredTime))
        file.close()

    def checkTimeForWater(self):
        #checks if the current time matches / is greater than next water time, if it does waters the plant
        dateDifference = self.nextWaterDateTime - datetime.datetime.now()
        if(dateDifference <= datetime.timedelta(seconds=0)):
            self.water()
        
    def submitButtonPress(self):
        #when the submit button is pressed, saves the watering schedule to file
        file = open("waterSchedule.txt", "r")
        if(len(self.scheduleEntry.get()) > 0):
            if(int(file.read()) > 0):
                file.close()
                file = open("waterSchedule.txt", "w")
                file.write(self.scheduleEntry.get())
        file.close()
        self.updateNextWater()
        self.updateWaterVolume()
        self.window.focus_set()
        
    def waterButtonPress(self):
        #manual water when water button is pressed
        self.water()
        
    def cancelButtonPress(self):
        #returns water schedule and volume to their respective values
        self.scheduleEntry.delete(0, 'end')
        self.scheduleEntry.insert(0, self.schedule)
        self.waterVolumeSlider.set(self.waterVolume)
        self.window.focus_set()
         
    def updateScheduleEntry(self, event):
        #changes schedule entry to current schedule
        file = open("waterSchedule.txt", "r")
        self.schedule = file.read()
        self.scheduleEntry.delete(0, 'end')
        self.scheduleEntry.insert(0, self.schedule)
        file.close()
        
    def updateWaterVolumeFile(self):
        file = open("waterVolume.txt", "w")
        print "writing volume to file: " + str(self.waterVolume)
        file.write(str(self.waterVolume))
        file.close()
        
    def updateWaterVolume(self):
        self.waterVolume = int(self.waterVolumeSlider.get())
        self.updateWaterVolumeFile()
    
MyGUI()