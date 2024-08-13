from PyQt5 import QtCore, QtGui, QtWidgets
import random, serial, time
import os
from datetime import datetime
 
 
arduino = serial.Serial('/dev/ttyUSB0', 9600)
 
class FinalUiWindow(object):
 
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyUSB0', 9600)  # Replace with your Arduino serial port
        self.reset_accelerometer = False
        self.last_voltage = None
        self.last_punch_speed = None
        self.last_punch_weight = None
        self.score = 0
        self.scorestart = False
        self.energy_harvested_value = 0.0
        self.scored_punch = False
        self.submit1 = False
 
    def update_readings(self):
        while self.serial.in_waiting > 0:
            line = self.serial.readline().decode().strip()
            if line:
                if line.startswith("V:"):
                    try:
                        voltage = float(line.split(':')[1])
                        if voltage != self.last_voltage:
                            self.update_label(voltage)
                            self.last_voltage = voltage
                            if voltage >= 0.5:
                                self.update_energy_harvested_value(voltage)
                                self.current_reading()
                    except ValueError:
                        pass
                elif line.startswith("S:"):
                    try:
                        punch_speed = float(line.split(":")[1])
                        if punch_speed != self.last_punch_speed:
                            self.last_punch_speed = punch_speed
                            self.labelPunchSpeedValue.setText(f"{punch_speed:.2f}M/S")
                            self.increment_score()
                    except ValueError:
                        pass
 
    def increment_score(self):
        if self.scorestart:
            if self.last_punch_speed is not None:
                if self.last_punch_speed  >= 2.0 and not self.scored_punch:
                    self.score += 1
                    self.labelScore.setText(str(self.score).zfill(4))
                    self.scored_punch = True
                elif self.last_punch_speed < 2.0:
                    self.scored_punch = False
 
    def current_reading (self):
        if self.last_voltage is not None and self.last_voltage >= 0.5:
            punch_weight = random.uniform(0.50, 0.60)
            if punch_weight != self.last_punch_weight:
                self.last_punch_weight = punch_weight
                self.labelPunchWeightValue.setText(f"{punch_weight:.2f}Ah")
 
 
    def update_label(self, voltage):
        self.labelVoltageReadingValue.setText(f"{voltage:.2f} V")
 
 
    def update_energy_harvested_value(self, voltage):
        if self.last_punch_weight is not None:
            power = voltage * self.last_punch_weight
            self.energy_harvested_value += power
            self.labelEnergyHarvestedValue.setText(f"{self.energy_harvested_value:.2f} w")
 
    def start_timer(self):
        if not self.is_timer_running:
            self.start_time.start()
            self.timer.start()
            self.is_timer_running = True
            self.scorestart = True
            self.energy_harvested_value = 0.0
            self.scored_punch = False
 
    def stop_timer(self):
        if self.is_timer_running:
            self.timer.stop()
            self.is_timer_running = False
            self.scorestart = False
            self.scored_punch = False
            self.submit1 = True
            self.Submit1.setEnabled(True)
            self.final_energy_harvested_value = self.energy_harvested_value
            self.final_punch_score = self.score
 
    def update_timer(self):
        if self.is_timer_running:
            elapsed_time = self.start_time.elapsed()
            time = QtCore.QTime(0, 0)
            time = time.addMSecs(elapsed_time)
            self.labelTimer.setText(time.toString("hh:mm:ss.zzz"))
 
    def refresh_window(self):
        self.update_timer()
        self.labelTimer.setText("00:00:00.0000")
        self.score = 0
        self.labelScore.setText(str(self.score).zfill(4))
        self.Submit1.setEnabled(False)
 
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1024, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainWindow.sizePolicy().hasHeightForWidth())
        mainWindow.setSizePolicy(sizePolicy)
        mainWindow.setMinimumSize(QtCore.QSize(1024, 600))
        mainWindow.setMaximumSize(QtCore.QSize(1024, 600))
        mainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1021, 601))
        self.stackedWidget.setObjectName("stackedWidget")
 
        self.BackgroundImage = QtWidgets.QLabel(self.centralwidget)
        self.BackgroundImage.setGeometry(QtCore.QRect(0, 0, 1024, 600))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BackgroundImage.sizePolicy().hasHeightForWidth())
        self.BackgroundImage.setSizePolicy(sizePolicy)
        self.BackgroundImage.setMinimumSize(QtCore.QSize(1024, 600))
        self.BackgroundImage.setMaximumSize(QtCore.QSize(1024, 600))
        self.BackgroundImage.setText("")
        self.BackgroundImage.setPixmap(QtGui.QPixmap("/home/caremeat/Desktop/backgroundimage.jpg"))
        self.BackgroundImage.setScaledContents(True)
        self.BackgroundImage.setObjectName("BackgroundImage")
        self.BackgroundImage.lower()
 
        # Initialize answers dictionary
        self.answers = {1: None, 2: None, 3: None, 4: None, 5: None}
        self.answerData = {'punch_score': 'N/A', 'energy_harvested': 'N/A'}
 
        # Setup pages
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.setupPage1(mainWindow)
        self.stackedWidget.addWidget(self.page_1)
 
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.setupPage2(mainWindow)
        self.stackedWidget.addWidget(self.page_2)
 
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.setupPage3(mainWindow)
        self.stackedWidget.addWidget(self.page_3)
 
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.setupPage4(mainWindow)
        self.stackedWidget.addWidget(self.page_4)
 
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.setupPage5(mainWindow)
        self.stackedWidget.addWidget(self.page_5)
 
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.setupPage6(mainWindow)
        self.stackedWidget.addWidget(self.page_6)
 
        self.page_7 = QtWidgets.QWidget()
        self.page_7.setObjectName("page_7")
        self.setupPage7(mainWindow)
        self.stackedWidget.addWidget(self.page_7)
 
        self.page_8 = QtWidgets.QWidget()
        self.page_8.setObjectName("page_8")
        self.setupPage8(mainWindow)
        self.stackedWidget.addWidget(self.page_8)
 
 
        mainWindow.setCentralWidget(self.centralwidget)
 
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)
 
        self.ButtonRefresh = QtWidgets.QPushButton(self.page_1)
        self.ButtonRefresh.setGeometry(QtCore.QRect(870, 490, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(13)
        self.ButtonRefresh.setFont(font)
        self.ButtonRefresh.setObjectName("ButtonRefresh")
        self.ButtonRefresh.setText("Refresh")
        self.ButtonRefresh.clicked.connect(self.refresh_window)
 
        self.ButtonStopTimer = QtWidgets.QPushButton(self.page_1)
        self.ButtonStopTimer.setGeometry(QtCore.QRect(580, 470, 131, 41))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        self.ButtonStopTimer.setFont(font)
        self.ButtonStopTimer.setCheckable(False)
        self.ButtonStopTimer.setAutoRepeat(False)
        self.ButtonStopTimer.setObjectName("ButtonStopTimer")
        self.ButtonStopTimer.setText("Stop Timer")
        self.ButtonStopTimer.clicked.connect(self.stop_timer)
 
 
    def setupPage1(self, mainWindow):
 
        self.groupBox = QtWidgets.QGroupBox(self.page_1)
        self.groupBox.setGeometry(QtCore.QRect(70, 50, 211, 441))
        font = QtGui.QFont()
        font.setFamily("Perpetua Titling MT")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("")
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.labelPunchWeight = QtWidgets.QLabel(self.groupBox)
        self.labelPunchWeight.setGeometry(QtCore.QRect(30, 30, 161, 21))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
 
        self.labelPunchWeight = QtWidgets.QLabel(self.groupBox)
        self.labelPunchWeight.setGeometry(QtCore.QRect(40, 30, 131, 21))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        font.setPointSize(1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.labelPunchWeight.setFont(font)
        self.labelPunchWeight.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPunchWeight.setObjectName("labelPunchWeight")
 
        self.timer_punch_weight = QtCore.QTimer(mainWindow)
        self.timer_punch_weight.timeout.connect(self.current_reading)
        self.timer_punch_weight.start(2000)
 
        self.labelPunchSpeed = QtWidgets.QLabel(self.groupBox)
        self.labelPunchSpeed.setGeometry(QtCore.QRect(40, 130, 131, 21))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.labelPunchSpeed.setFont(font)
        self.labelPunchSpeed.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPunchSpeed.setObjectName("labelPunchSpeed")
 
        self.timer_punch_speed = QtCore.QTimer(mainWindow)
        self.timer_punch_speed.timeout.connect(self.update_readings)
        self.timer_punch_speed.start(100)
 
        self.labelVoltageReading = QtWidgets.QLabel(self.groupBox)
        self.labelVoltageReading.setGeometry(QtCore.QRect(20, 230, 151, 21))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.labelVoltageReading.setFont(font)
        self.labelVoltageReading.setAlignment(QtCore.Qt.AlignCenter)
        self.labelVoltageReading.setObjectName("labelVoltageReading")
 
        self.timer_voltage = QtCore.QTimer(mainWindow)
        self.timer_voltage.timeout.connect(self.update_readings)
        self.timer_voltage.start(100)
 
        self.labelEnergyHarvested = QtWidgets.QLabel(self.groupBox)
        self.labelEnergyHarvested.setGeometry(QtCore.QRect(10, 330, 171, 21))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.labelEnergyHarvested.setFont(font)
        self.labelEnergyHarvested.setAlignment(QtCore.Qt.AlignCenter)
        self.labelEnergyHarvested.setObjectName("labelEnergyHarvested")
        self.frameEnergyHarvested = QtWidgets.QFrame(self.groupBox)
        self.frameEnergyHarvested.setGeometry(QtCore.QRect(30, 360, 151, 61))
        self.frameEnergyHarvested.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frameEnergyHarvested.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameEnergyHarvested.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frameEnergyHarvested.setObjectName("frameEnergyHarvested")
        self.labelEnergyHarvestedValue = QtWidgets.QLabel(self.frameEnergyHarvested)
        self.labelEnergyHarvestedValue.setGeometry(QtCore.QRect(10, 10, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.labelEnergyHarvestedValue.setFont(font)
        self.labelEnergyHarvestedValue.setAlignment(QtCore.Qt.AlignCenter)
        self.labelEnergyHarvestedValue.setObjectName("labelEnergyHarvestedValue")
 
        self.timer_voltage = QtCore.QTimer(mainWindow)
        self.timer_voltage.timeout.connect(self.update_readings)
        self.timer_voltage.start(100)
 
        self.framePunchWeight = QtWidgets.QFrame(self.groupBox)
        self.framePunchWeight.setGeometry(QtCore.QRect(30, 60, 151, 61))
        self.framePunchWeight.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.framePunchWeight.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framePunchWeight.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.framePunchWeight.setObjectName("framePunchWeight")
        self.labelPunchWeightValue = QtWidgets.QLabel(self.framePunchWeight)
        self.labelPunchWeightValue.setGeometry(QtCore.QRect(10, 10, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.labelPunchWeightValue.setFont(font)
        self.labelPunchWeightValue.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.labelPunchWeightValue.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPunchWeightValue.setObjectName("labelPunchWeightValue")
        self.framePunchSpeed = QtWidgets.QFrame(self.groupBox)
        self.framePunchSpeed.setGeometry(QtCore.QRect(30, 160, 151, 61))
        self.framePunchSpeed.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.framePunchSpeed.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framePunchSpeed.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.framePunchSpeed.setObjectName("framePunchSpeed")
        self.labelPunchSpeedValue = QtWidgets.QLabel(self.framePunchSpeed)
        self.labelPunchSpeedValue.setGeometry(QtCore.QRect(10, 10, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.labelPunchSpeedValue.setFont(font)
        self.labelPunchSpeedValue.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.labelPunchSpeedValue.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPunchSpeedValue.setObjectName("labelPunchSpeedValue")
        self.frameVoltageSpeed = QtWidgets.QFrame(self.groupBox)
        self.frameVoltageSpeed.setGeometry(QtCore.QRect(30, 260, 151, 61))
        self.frameVoltageSpeed.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frameVoltageSpeed.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameVoltageSpeed.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frameVoltageSpeed.setObjectName("frameVoltageSpeed")
        self.labelVoltageReadingValue = QtWidgets.QLabel(self.frameVoltageSpeed)
        self.labelVoltageReadingValue.setGeometry(QtCore.QRect(10, 10, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.labelVoltageReadingValue.setFont(font)
        self.labelVoltageReadingValue.setAlignment(QtCore.Qt.AlignCenter)
        self.labelVoltageReadingValue.setObjectName("labelVoltageReadingValue")
 
 
 
        # label okay na
        self.labelScore = QtWidgets.QLabel(self.page_1)
        self.labelScore.setGeometry(QtCore.QRect(320, 180, 431, 271))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(100)
        font.setBold(False)
        font.setWeight(50)
        self.labelScore.setFont(font)
        self.labelScore.setFrameShape(QtWidgets.QFrame.Box)
        self.labelScore.setFrameShadow(QtWidgets.QFrame.Plain)
        self.labelScore.setMidLineWidth(0)
        self.labelScore.setText("")
        self.labelScore.setAlignment(QtCore.Qt.AlignCenter)
        self.labelScore.setIndent(-1)
        self.labelScore.setObjectName("labelScore")
        self.labelScore.setText(str(self.score).zfill(4))
 
 
 
        # timer okay na
        self.frameTimer = QtWidgets.QFrame(self.page_1)
        self.frameTimer.setGeometry(QtCore.QRect(400, 110, 271, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.frameTimer.setFont(font)
        self.frameTimer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameTimer.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frameTimer.setObjectName("frameTimer")
        self.labelTimer = QtWidgets.QLabel(self.frameTimer)
        self.labelTimer.setGeometry(QtCore.QRect(10, 10, 251, 31))
        self.labelTimer.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTimer.setObjectName("labelTimer")
        self.timer = QtCore.QTimer(mainWindow)
        self.timer.timeout.connect(self.update_timer)
        self.timer.setInterval(10)  # Update every 10 milliseconds
        self.is_timer_running = False
        self.start_time = QtCore.QTime()
 
        # start okay na
        self.ButtonStartTimer = QtWidgets.QPushButton(self.page_1)
        self.ButtonStartTimer.setGeometry(QtCore.QRect(350, 470, 131, 41))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        self.ButtonStartTimer.setFont(font)
        self.ButtonStartTimer.setObjectName("ButtonStartTimer")
        self.ButtonStartTimer.clicked.connect(self.start_timer)
 
        self.Submit1 = QtWidgets.QPushButton(self.page_1)
        self.Submit1.setGeometry(QtCore.QRect(850, 270, 121, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.Submit1.setFont(font)
        self.Submit1.setObjectName("Submit1")
        self.Submit1.setEnabled(False)
        self.Submit1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.page_2)))
 
 
    def setupPage2(self, mainWindow):
 
        self.scrollArea = QtWidgets.QScrollArea(self.page_2)
        self.scrollArea.setGeometry(QtCore.QRect(50, 50, 924, 400))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 922, 398))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.disclaimerText = QtWidgets.QLabel(self.scrollArea)
        self.disclaimerText.setGeometry(QtCore.QRect(10, 10, 900, 380))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.disclaimerText.setFont(font)
        self.disclaimerText.setAlignment(QtCore.Qt.AlignLeft)
        self.disclaimerText.setWordWrap(True)
        self.disclaimerText.setText(
            "\n\n\nThe following questions will determine if the punching machine helps you release some tension and lessen or reduced the stress you're experiencing."
        )
 
        self.ButtonDisclaimerNext = QtWidgets.QPushButton(self.page_2)
        self.ButtonDisclaimerNext.setGeometry(QtCore.QRect(870, 470, 131, 41))
        self.ButtonDisclaimerNext.setObjectName("ButtonDisclaimerNext")
        self.ButtonDisclaimerNext.setText("Next")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonDisclaimerNext.setFont(font)
        self.ButtonDisclaimerNext.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.page_3)))
 
        self.ButtonDisclaimerBack = QtWidgets.QPushButton(self.page_2)
        self.ButtonDisclaimerBack.setGeometry(QtCore.QRect(20, 470, 131, 41))
        self.ButtonDisclaimerBack.setObjectName("ButtonDisclaimerBack")
        self.ButtonDisclaimerBack.setText("Back")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonDisclaimerBack.setFont(font)
        self.ButtonDisclaimerBack.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
 
    def setupPage3(self, mainWindow):
 
        self.labelName = QtWidgets.QLabel(self.page_3)
        self.labelName.setGeometry(QtCore.QRect(200, 150, 621, 31))
        self.labelName.setText("Please Enter Your Name: ")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.labelName.setFont(font)
        self.labelName.setAlignment(QtCore.Qt.AlignCenter)
        self.labelName.setObjectName("labelName")
 
        self.lineEditName = QtWidgets.QLineEdit(self.page_3)
        self.lineEditName.setGeometry(QtCore.QRect(300, 200, 400, 31))
        self.lineEditName.setFont(font)
        self.lineEditName.setObjectName("lineEditName")
 
        self.ButtonNameNext = QtWidgets.QPushButton(self.page_3)
        self.ButtonNameNext.setGeometry(QtCore.QRect(870, 470, 131, 41))
        self.ButtonNameNext.setObjectName("ButtonNameNext")
        self.ButtonNameNext.setText("Next")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonNameNext.setFont(font)
        self.ButtonNameNext.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.page_4)))
 
        self.ButtonNameBack = QtWidgets.QPushButton(self.page_3)
        self.ButtonNameBack.setGeometry(QtCore.QRect(20, 470, 131, 41))
        self.ButtonNameBack.setObjectName("ButtonNameBack")
        self.ButtonNameBack.setText("Back")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonNameBack.setFont(font)
        self.ButtonNameBack.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
 
    def setupPage4(self, mainWindow):
 
        self.labelQuestion1 = QtWidgets.QLabel(self.page_4)
        self.labelQuestion1.setGeometry(QtCore.QRect(50, 200, 900, 81))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.labelQuestion1.setFont(font)
        self.labelQuestion1.setAlignment(QtCore.Qt.AlignCenter)
        self.labelQuestion1.setWordWrap(True)
        self.labelQuestion1.setText("1. Since using the punching bag, have you felt any noticeable shift in your mood or emotional state?")
        self.labelQuestion1.setObjectName(f"labelQuestion1")
 
        self.ButtonYes1= QtWidgets.QPushButton(self.page_4)
        self.ButtonYes1.setGeometry(QtCore.QRect(290, 350, 131, 71))
        self.ButtonYes1.setObjectName("ButtonYes1")
        self.ButtonYes1.setText("Yes")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonYes1.setFont(font)
        self.ButtonYes1.clicked.connect(lambda: self.setAnswer(1, "Yes"))
 
        self.ButtonNo1 = QtWidgets.QPushButton(self.page_4)
        self.ButtonNo1.setGeometry(QtCore.QRect(590, 350, 131, 71))
        self.ButtonNo1.setObjectName("ButtonNo1")
        self.ButtonNo1.setText("No")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonNo1.setFont(font)
        self.ButtonNo1.clicked.connect(lambda: self.setAnswer(1, "No"))
 
        self.ButtonSubmit1 = QtWidgets.QPushButton(self.page_4)
        self.ButtonSubmit1.setGeometry(QtCore.QRect(870, 470, 131, 41))
        self.ButtonSubmit1.setObjectName("ButtonSubmit1")
        self.ButtonSubmit1.setText("Next")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonSubmit1.setFont(font)
        self.ButtonSubmit1.clicked.connect(lambda: self.submitAnswer(1))
        self.ButtonSubmit1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.page_5)))
 
        self.ButtonBack1 = QtWidgets.QPushButton(self.page_4)
        self.ButtonBack1.setGeometry(QtCore.QRect(20, 470, 131, 41))
        self.ButtonBack1.setObjectName("ButtonBack1")
        self.ButtonBack1.setText("Back")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonBack1.setFont(font)
        self.ButtonBack1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
 
    def setupPage5(self, mainWindow):
 
        self.labelQuestion2 = QtWidgets.QLabel(self.page_5)
        self.labelQuestion2.setGeometry(QtCore.QRect(50, 200, 900, 81))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.labelQuestion2.setFont(font)
        self.labelQuestion2.setAlignment(QtCore.Qt.AlignCenter)
        self.labelQuestion2.setWordWrap(True)
        self.labelQuestion2.setText("2. Do you feel like using the punching bag helped you to release pent-up energy or frustration?")
        self.labelQuestion2.setObjectName(f"labelQuestion2")
 
        self.ButtonYes2= QtWidgets.QPushButton(self.page_5)
        self.ButtonYes2.setGeometry(QtCore.QRect(290, 350, 131, 71))
        self.ButtonYes2.setObjectName("ButtonYes2")
        self.ButtonYes2.setText("Yes")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonYes2.setFont(font)
        self.ButtonYes2.clicked.connect(lambda: self.setAnswer(2, "Yes"))
 
 
        self.ButtonNo2 = QtWidgets.QPushButton(self.page_5)
        self.ButtonNo2.setGeometry(QtCore.QRect(590, 350, 131, 71))
        self.ButtonNo2.setObjectName("ButtonNo2")
        self.ButtonNo2.setText("No")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonNo2.setFont(font)
        self.ButtonNo2.clicked.connect(lambda: self.setAnswer(2, "No"))
 
        self.ButtonSubmit2 = QtWidgets.QPushButton(self.page_5)
        self.ButtonSubmit2.setGeometry(QtCore.QRect(870, 470, 131, 41))
        self.ButtonSubmit2.setObjectName("ButtonSubmit2")
        self.ButtonSubmit2.setText("Next")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonSubmit2.setFont(font)
        self.ButtonSubmit2.clicked.connect(lambda: self.submitAnswer(2))
        self.ButtonSubmit2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.page_6)))
 
        self.ButtonBack2 = QtWidgets.QPushButton(self.page_5)
        self.ButtonBack2.setGeometry(QtCore.QRect(20, 470, 131, 41))
        self.ButtonBack2.setObjectName("ButtonBack2")
        self.ButtonBack2.setText("Back")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonBack2.setFont(font)
        self.ButtonBack2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
 
    def setupPage6(self, mainWindow):
 
        self.labelQuestion3 = QtWidgets.QLabel(self.page_6)
        self.labelQuestion3.setGeometry(QtCore.QRect(50, 200, 900, 81))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.labelQuestion3.setFont(font)
        self.labelQuestion3.setAlignment(QtCore.Qt.AlignCenter)
        self.labelQuestion3.setWordWrap(True)
        self.labelQuestion3.setText("3. Did you find it easier to wind down and relax after using the punching bag?")
        self.labelQuestion3.setObjectName(f"labelQuestion3")
 
        self.ButtonYes3= QtWidgets.QPushButton(self.page_6)
        self.ButtonYes3.setGeometry(QtCore.QRect(290, 350, 131, 71))
        self.ButtonYes3.setObjectName("ButtonYes3")
        self.ButtonYes3.setText("Yes")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonYes3.setFont(font)
        self.ButtonYes3.clicked.connect(lambda: self.setAnswer(3, "Yes"))
 
        self.ButtonNo3 = QtWidgets.QPushButton(self.page_6)
        self.ButtonNo3.setGeometry(QtCore.QRect(590, 350, 131, 71))
        self.ButtonNo3.setObjectName("ButtonNo1")
        self.ButtonNo3.setText("No")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonNo3.setFont(font)
        self.ButtonNo3.clicked.connect(lambda: self.setAnswer(3, "No"))
 
        self.ButtonBack3 = QtWidgets.QPushButton(self.page_6)
        self.ButtonBack3.setGeometry(QtCore.QRect(20, 470, 131, 41))
        self.ButtonBack3.setObjectName("ButtonBack5")
        self.ButtonBack3.setText("Back")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonBack3.setFont(font)
        self.ButtonBack3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
 
 
        self.ButtonSubmit3 = QtWidgets.QPushButton(self.page_6)
        self.ButtonSubmit3.setGeometry(QtCore.QRect(870, 470, 131, 41))
        self.ButtonSubmit3.setObjectName("ButtonSubmit1")
        self.ButtonSubmit3.setText("Next")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonSubmit3.setFont(font)
        self.ButtonSubmit3.clicked.connect(lambda: self.submitAnswer(3))
        self.ButtonSubmit3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.page_7)))
 
 
 
    def setupPage7(self, mainWindow):
 
        self.labelQuestion4 = QtWidgets.QLabel(self.page_7)
        self.labelQuestion4.setGeometry(QtCore.QRect(50, 200, 900, 81))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.labelQuestion4.setFont(font)
        self.labelQuestion4.setAlignment(QtCore.Qt.AlignCenter)
        self.labelQuestion4.setWordWrap(True)
        self.labelQuestion4.setText("4. On a scale of 1 to 10, how effective do you think the punching bag was at helping you manage your stress?")
        self.labelQuestion4.setObjectName(f"labelQuestion4")
 
 
        self.ButtonBack4 = QtWidgets.QPushButton(self.page_7)
        self.ButtonBack4.setGeometry(QtCore.QRect(20, 470, 131, 41))
        self.ButtonBack4.setObjectName("ButtonBack5")
        self.ButtonBack4.setText("Back")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonBack4.setFont(font)
        self.ButtonBack4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
 
 
        self.ButtonSubmit4 = QtWidgets.QPushButton(self.page_7)
        self.ButtonSubmit4.setGeometry(QtCore.QRect(870, 470, 131, 41))
        self.ButtonSubmit4.setObjectName("ButtonSubmit5")
        self.ButtonSubmit4.setText("Next")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonSubmit4.setFont(font)
 
        self.ButtonSubmit4.clicked.connect(lambda: self.submitAnswer(4))
        self.ButtonSubmit4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.page_8)))
 
 
        self.scaleButtons = []
        for i in range(10):
            button = QtWidgets.QPushButton(self.page_7)
            button.setGeometry(QtCore.QRect(80 + i * 90, 350, 81, 71))
            button.setFont(font)
            button.setText(str(i + 1))
            button.setObjectName(f"scaleButton_{i + 1}")
            button.clicked.connect(lambda checked, idx=i+1: self.scaleAnswer(4, idx))
            self.scaleButtons.append(button)
 
 
    def setupPage8(self, mainWindow):
 
        self.labelQuestion5 = QtWidgets.QLabel(self.page_8)
        self.labelQuestion5.setGeometry(QtCore.QRect(50, 200, 900, 81))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.labelQuestion5.setFont(font)
        self.labelQuestion5.setAlignment(QtCore.Qt.AlignCenter)
        self.labelQuestion5.setWordWrap(True)
        self.labelQuestion5.setText("5. Would you be interested in using the punching bag again as a way to manage stress?")
        self.labelQuestion5.setObjectName(f"labelQuestion5")
 
        self.ButtonYes5 = QtWidgets.QPushButton(self.page_8)
        self.ButtonYes5.setGeometry(QtCore.QRect(290, 350, 131, 71))
        self.ButtonYes5.setObjectName("ButtonYes5")
        self.ButtonYes5.setText("Yes")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonYes5.setFont(font)
        self.ButtonYes5.clicked.connect(lambda: self.setAnswer(5, "Yes"))
 
        self.ButtonNo5 = QtWidgets.QPushButton(self.page_8)
        self.ButtonNo5.setGeometry(QtCore.QRect(590, 350, 131, 71))
        self.ButtonNo5.setObjectName("ButtonNo5")
        self.ButtonNo5.setText("No")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonNo5.setFont(font)
        self.ButtonNo5.clicked.connect(lambda: self.setAnswer(5, "No"))
 
        self.ButtonSubmit5 = QtWidgets.QPushButton(self.page_8)
        self.ButtonSubmit5.setGeometry(QtCore.QRect(870, 470, 131, 41))
        self.ButtonSubmit5.setObjectName("ButtonSubmit6")
        self.ButtonSubmit5.setText("Submit")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonSubmit5.setFont(font)
 
        self.ButtonBack5 = QtWidgets.QPushButton(self.page_8)
        self.ButtonBack5.setGeometry(QtCore.QRect(20, 470, 131, 41))
        self.ButtonBack5.setObjectName("ButtonBack6")
        self.ButtonBack5.setText("Back")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.ButtonBack5.setFont(font)
 
        self.ButtonSubmit5.clicked.connect(self.submit)
        self.ButtonBack5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))
 
 
    def setAnswer(self, question_index, answer):
        self.answers[question_index] = answer
        if question_index == 1:
            self.ButtonYes1.setEnabled(answer != "Yes")
            self.ButtonNo1.setEnabled(answer != "No")    
        elif question_index == 2:
            self.ButtonYes2.setEnabled(answer != "Yes")
            self.ButtonNo2.setEnabled(answer != "No")
        elif question_index == 3:
            self.ButtonYes3.setEnabled(answer != "Yes")
            self.ButtonNo3.setEnabled(answer != "No")
        elif question_index == 5:
            self.ButtonYes5.setEnabled(answer != "Yes")
            self.ButtonNo5.setEnabled(answer != "No")
 
    def submitAnswer(self, question_index):
        if question_index != 2:
            if self.answers[question_index] is None:
                QtWidgets.QMessageBox.information(None, "Incomplete Answer","Please return to this page and provide an answer.")
                return
        self.stackedWidget.setCurrentIndex(question_index)
 
    def scaleAnswer(self, question_index, answer):
        self.answers[question_index] = answer
        for button in self.scaleButtons:
            if int(button.text()) == answer:
                button.setEnabled(False)
            else:
                button.setEnabled(True)
 
    def submit(self):
 
        user_name = self.lineEditName.text().strip()
 
        user_name = user_name if user_name else "anonymous"
 
        # Check if all questions are answered
        unanswered_questions = [i for i, answer in self.answers.items() if answer is None]
        if unanswered_questions:
            unanswered_str = ", ".join(map(str, unanswered_questions))
            QtWidgets.QMessageBox.information(None, "Survey Incomplete", f"Please answer all questions. Unanswered question(s): {unanswered_str}")
            return
 
        self.answerData['punch_score'] = str(self.final_punch_score)
        decimal_energy_harvested = f'{self.final_energy_harvested_value:.2f}W'
        self.answerData['energy_harvested'] = decimal_energy_harvested
        file_name = f"{user_name}_post-test_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        folder_path = "Post-Test Results"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, file_name)
 
        with open(file_path, 'w') as file:
            file.write(f"Name: {user_name}\n")
            file.write(f"Punch Score: {self.answerData['punch_score']}\n")
            file.write(f"Energy Harvested: {self.answerData['energy_harvested']}\n")
            for i, answer in self.answers.items():
                file.write(f"Q{i}: {answer}\n")
 
        QtWidgets.QMessageBox.information(None, "Survey Submitted", "Thank you for your participation!")
        QtWidgets.qApp.quit()
 
    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "PunchOUT!"))
        self.groupBox.setTitle(_translate("mainWindow", "PROFILE DETAIL"))
        self.labelPunchWeight.setText(_translate("mainWi ndow", "Current"))
        self.labelPunchSpeed.setText(_translate("mainWindow", "Punch Speed"))
        self.labelVoltageReading.setText(_translate("mainWindow", "Voltage Reading"))
        self.labelEnergyHarvested.setText(_translate("mainWindow", "Energy Harvested"))
        self.labelEnergyHarvestedValue.setText(_translate("mainWindow", "00.00V"))
        self.labelPunchWeightValue.setText(_translate("mainWindow", "0.00 Ah"))
        self.labelPunchSpeedValue.setText(_translate("mainWindow", "00 M/S"))
        self.labelVoltageReadingValue.setText(_translate("mainWindow", "00.00V"))
        #  self.ButtonStopTimer.setText(_translate("mainWindow", "Stop Timer"))
       # self.ButtonRefresh.setText(_translate("mainWindow", "Refresh"))
        self.labelScore.setText(_translate("mainWindow", "0000"))
        self.labelTimer.setText(_translate("mainWindow", "00:00:00:000"))
        self.ButtonStartTimer.setText(_translate("mainWindow", "Start Timer"))
        self.Submit1.setText(_translate("mainWindow", "Submit"))
 
 
 
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = FinalUiWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())