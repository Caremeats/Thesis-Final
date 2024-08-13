from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os
 
sys.path.append("/home/caremeat/Desktop/Thesis/")
from FinalUi import FinalUiWindow
 
class PretestWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 600))
        MainWindow.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
 
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
 
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1024, 600))
        self.stackedWidget.setObjectName("stackedWidget")
 
        # Disclaimer Page 1
        self.disclaimerPage = QtWidgets.QWidget()
        self.disclaimerPage.setObjectName("disclaimerPage")
 
        self.scrollArea = QtWidgets.QScrollArea(self.disclaimerPage)
        self.scrollArea.setGeometry(QtCore.QRect(40, 25, 950, 525))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 922, 500))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
 
        self.disclaimerText = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.disclaimerText.setGeometry(QtCore.QRect(10, 10, 900, 500))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.disclaimerText.setFont(font)
        self.disclaimerText.setAlignment(QtCore.Qt.AlignLeft)
        self.disclaimerText.setWordWrap(True)
        self.disclaimerText.setText(
                        "𝐃𝐀𝐓𝐀 𝐏𝐑𝐈𝐕𝐀𝐂𝐘\n"
            "In compliance with RA 10173 or the Data Protection Act of 2012 (DPA of 2012) and its Implementing Rules and Regulations, we are detailing here the processing of the data you will provide to us.\n\n"
            "𝐏𝐮𝐫𝐩𝐨𝐬𝐞. This form will serve as the basis for the Computer Engineering students for their CPE Project and Design 2 Thesis entitled “From Stress to Power: An Integrated Approach to Student Stress Relief and Sustainable Energy Generation through a Smart Punching Machine.”\n"
            "𝗥𝗲𝘁𝗲𝗻𝘁𝗶𝗼𝗻, 𝗦𝘁𝗼𝗿𝗮𝗴𝗲, 𝗮𝗻𝗱 𝗗𝗶𝘀𝗽𝗼𝘀𝗮𝗹. Personal data collected shall be stored in the protected folder in google drive using Adamson University e-mail for a period of one academic year. Upon expiration of such period, all personal data shall be disposed of in a secure manner that forbids further processing, unauthorized disclosure, and editing.\n"
            "𝗗𝗮𝘁𝗮 𝗣𝗿𝗼𝘁𝗲𝗰𝘁𝗶𝗼𝗻. The University shall implement reasonable and appropriate organizational, physical, and technical security measures to protect your personal data. Only authorized personnel shall have access to the data collected and processed.\n"
            "𝗗𝗮𝘁𝗮 𝗦𝘂𝗯𝗷𝗲𝗰𝘁 𝗥𝗶𝗴𝗵𝘁𝘀. Under RA 10173, the following are some of the rights the data subject may exercise\n\n"
            "1. Right to be informed on the collection and processing of personal data through this consent form;\n"
            "2. Right to object to the processing of personal data or to restrict the processing of personal data upon request;\n"
            "3. Right to access the personal data collected and processed upon request;\n"
            "4. Right to request for rectification of personal data; and\n"
            "5. Right to withdraw his or her consent."
        )
 
        self.nextButtonDisclaimer = QtWidgets.QPushButton(self.disclaimerPage)
        self.nextButtonDisclaimer.setGeometry(QtCore.QRect(850, 500, 111, 41))
        font.setPointSize(15)
        self.nextButtonDisclaimer.setFont(font)
        self.nextButtonDisclaimer.setText("Accept")
        self.nextButtonDisclaimer.setObjectName("nextButtonDisclaimer")
        self.nextButtonDisclaimer.clicked.connect(self.nextPage)
 
 
        self.stackedWidget.addWidget(self.disclaimerPage)
 
 
        # Disclaimer Page 2
        self.disclaimerPage = QtWidgets.QWidget()
        self.disclaimerPage.setObjectName("disclaimerPage")
 
        self.scrollArea = QtWidgets.QScrollArea(self.disclaimerPage)
        self.scrollArea.setGeometry(QtCore.QRect(50, 50, 924, 400))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 922, 398))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
 
        self.disclaimerText = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.disclaimerText.setGeometry(QtCore.QRect(10, 10, 900, 380))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.disclaimerText.setFont(font)
        self.disclaimerText.setAlignment(QtCore.Qt.AlignLeft)
        self.disclaimerText.setWordWrap(True)
        self.disclaimerText.setText(
            "The following questions are a self-assessment test to determine whether or not you are experiencing stress. "
            "If so, the level of stress that you are experiencing will be determined by answering the questions.\n\n"
            "Answer the following questions based on the given metrics:\n"
            "0 - never\n"
            "1 - almost never\n"
            "2 - sometimes\n"
            "3 - fairly often\n"
            "4 - very often\n\n"
        )
 
        self.nextButtonDisclaimer = QtWidgets.QPushButton(self.disclaimerPage)
        self.nextButtonDisclaimer.setGeometry(QtCore.QRect(850, 500, 111, 41))
        font.setPointSize(15)
        self.nextButtonDisclaimer.setFont(font)
        self.nextButtonDisclaimer.setText("Next")
        self.nextButtonDisclaimer.setObjectName("nextButtonDisclaimer")
        self.nextButtonDisclaimer.clicked.connect(self.nextPage)
 
 
        self.stackedWidget.addWidget(self.disclaimerPage)
 
        # Page 1: Instructions
        self.page1 = QtWidgets.QWidget()
        self.page1.setObjectName("page1")
 
        self.labelInstructions = QtWidgets.QLabel(self.page1)
        self.labelInstructions.setGeometry(QtCore.QRect(50, 50, 900, 200))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
 
        self.nameLabel = QtWidgets.QLabel(self.page1)
        self.nameLabel.setGeometry(QtCore.QRect(380, 150, 621, 31))
        self.nameLabel.setFont(font)
        self.nameLabel.setText("Please enter your name: ")
 
        self.nameLineEdit = QtWidgets.QLineEdit(self.page1)
        self.nameLineEdit.setGeometry(QtCore.QRect(300, 200, 400, 31))
        self.nameLineEdit.setFont(font)
 
        self.ageLabel = QtWidgets.QLabel(self.page1)
        self.ageLabel.setGeometry(QtCore.QRect(380, 250, 621, 31))
        self.ageLabel.setFont(font)
        self.ageLabel.setText("Age: ")
 
        self.ageLineEdit = QtWidgets.QLineEdit(self.page1)
        self.ageLineEdit.setGeometry(QtCore.QRect(450, 250, 100, 31))
        self.ageLineEdit.setFont(font)
        self.ageLineEdit.setValidator(QtGui.QIntValidator())
 
        self.genderLabel = QtWidgets.QLabel(self.page1)
        self.genderLabel.setGeometry(QtCore.QRect(380, 300, 621, 31))
        self.genderLabel.setFont(font)
        self.genderLabel.setText("Gender: ")
 
        self.genderComboBox = QtWidgets.QComboBox(self.page1)
        self.genderComboBox.setGeometry(QtCore.QRect(480, 300, 200, 31))
        self.genderComboBox.setFont(font)
        self.genderComboBox.addItems(["Male", "Female", "Prefer not to say"])
 
 
 
 
        self.nextButtonPage1 = QtWidgets.QPushButton(self.page1)
        self.nextButtonPage1.setGeometry(QtCore.QRect(850, 500, 111, 41))
        font.setPointSize(15)
        self.nextButtonPage1.setFont(font)
        self.nextButtonPage1.setText("Next")
        self.nextButtonPage1.setObjectName("nextButtonPage1")
        self.nextButtonPage1.clicked.connect(self.nextPage)
 
        self.stackedWidget.addWidget(self.page1)
 
        questions = [
            "1. In the last month, how often have you been upset because of something that happened unexpectedly?",
            "2. In the last month, how often have you felt that you were unable to control the important things in your life?",
            "3. In the last month, how often have you felt nervous and stressed?",
            "4. In the last month, how often have you felt confident about your ability to handle your personal problems? (Your scores are reversed in this question ex: 4=0, 3=1 and so on)",
            "5. In the last month, how often have you felt that things were going your way? (Your scores are reversed in this question ex: 4=0, 3=1 and so on)",
            "6. In the last month, how often have you found that you could not cope with all the things that you had to do?",
            "7. In the last month, how often have you been able to control irritations in your life? (Your scores are reversed in this question ex: 4=0, 3=1 and so on)",
            "8. In the last month, how often have you felt that you were on top of things? (Your scores are reversed in this question ex: 4=0, 3=1 and so on)",
            "9. In the last month, how often have you been angered because of things that happened that were outside of your control?",
            "10. In the last month, how often have you felt difficulties were piling up so high that you could not overcome them?"
        ]
 
        self.answerData = {'answers': []}
        self.questionPages = []
        self.reversedQuestions = [3, 4, 6, 7]  # Indexes of questions with reversed scoring
 
        for i, question in enumerate(questions):
            page = QtWidgets.QWidget()
            page.setObjectName(f"page{i + 2}")
 
            labelQuestion = QtWidgets.QLabel(page)
            labelQuestion.setGeometry(QtCore.QRect(50, 100, 900, 81))
            font.setPointSize(20)
            labelQuestion.setFont(font)
            labelQuestion.setAlignment(QtCore.Qt.AlignCenter)
            labelQuestion.setWordWrap(True)
            labelQuestion.setText(question)
            labelQuestion.setObjectName(f"labelQuestion{i + 2}")
 
            backButton = QtWidgets.QPushButton(page)
            backButton.setGeometry(QtCore.QRect(80, 500, 111, 41))
            backButton.setFont(font)
            backButton.setText("Back")
            backButton.setObjectName(f"backButton{i + 2}")
            backButton.clicked.connect(self.previousPage)
 
            self.scaleButtons = []
            for j in range(5):
                button = QtWidgets.QPushButton(page)
                button.setGeometry(QtCore.QRect(180 + j * 140, 350, 121, 71))
                button.setFont(font)
                button.setText(str(j))
                button.setObjectName(f"scaleButton{i + 2}_{j}")
                button.clicked.connect(lambda _, x=i, y=j: self.recordAnswer(x, y))
                self.scaleButtons.append(button)
 
            if i < len(questions) - 1:
                nextButton = QtWidgets.QPushButton(page)
                nextButton.setGeometry(QtCore.QRect(850, 500, 111, 41))
                nextButton.setFont(font)
                nextButton.setText("Next")
                nextButton.setObjectName(f"nextButton{i + 2}")
                nextButton.clicked.connect(self.nextPage)
            else:
                submitButton = QtWidgets.QPushButton(page)
                submitButton.setGeometry(QtCore.QRect(850, 500, 111, 41))
                submitButton.setFont(font)
                submitButton.setText("Submit")
                submitButton.setObjectName(f"submitButton{i + 2}")
                submitButton.clicked.connect(self.submit)
 
            self.stackedWidget.addWidget(page)
            self.questionPages.append(page)
 
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
 
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pre-Test Result"))
 
    def nextPage(self):
        currentIndex = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(currentIndex + 1)
 
    def previousPage(self):
        currentIndex = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(currentIndex - 1)
 
    def recordAnswer(self, questionIndex, score):
        # Disable the clicked scale button
        currentButtonName = f"scaleButton{questionIndex + 2}_{score}"
        currentButton = self.questionPages[questionIndex].findChild(QtWidgets.QPushButton, currentButtonName)
        currentButton.setEnabled(False)
 
        # Enable the previously clicked scale button (if any)
        if hasattr(self, "lastScaleButton"):
            self.lastScaleButton.setEnabled(True)
 
        # Update the last scale button reference
        self.lastScaleButton = currentButton
 
        # Record the answer in the answerData dictionary
        while len(self.answerData['answers']) <= questionIndex:
            self.answerData['answers'].append(None)
        self.answerData['answers'][questionIndex] = score
 
    def submit(self):
        unanswered_questions = []
        for i, score in enumerate(self.answerData['answers']):
            if score is None:
                unanswered_questions.append(i + 1)
 
        if unanswered_questions:
            unanswered_message = "You have not answered the following questions:\n" + \
                                 "\n".join([f"Question {q}" for q in unanswered_questions])
            QtWidgets.QMessageBox.warning(None, "Incomplete Survey", unanswered_message)
            return
 
        total_score = 0
        scale_choices = {}
 
        for i, score in enumerate(self.answerData['answers']):
            if i in self.reversedQuestions:
                total_score += 4 - score
            else:
                total_score += score
            scale_choices[i] = score
 
        if total_score <= 13:
            stress_level = "low stress"
        elif total_score <= 26:
            stress_level = "moderate stress"
        else:
            stress_level = "high stress"
 
        name = self.nameLineEdit.text()
        if not name:
            name = "anonymous"
 
        age = self.ageLineEdit.text()
        gender = self.genderComboBox.currentText()
 
        folder_path = "Pre-test"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
 
        file_name = f"{name}_pre-test_{QtCore.QDateTime.currentDateTime().toString('yyyyMMddhhmmss')}.txt"
 
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w') as file:
            file.write(f"Name: {name}\n")
            file.write(f"Age: {age}\n")
            file.write(f"Gender: {gender}\n")
            file.write(f"\nTotal Score: {total_score}\n")
            file.write(f"Stress Level: {stress_level}\n")
            file.write("\nScale Choices:\n")
            for question_number, choice in scale_choices.items():
                file.write(f"Question {question_number + 1}: {choice}\n")
 
        QtWidgets.QMessageBox.information(None, "Survey Submitted",
                                          f"Thank you for your participation!\n\nYour total score is {total_score}, which indicates {stress_level}.")
        self.FinalUi = QtWidgets.QMainWindow()
        ui_survey = FinalUiWindow()
        ui_survey.setupUi(self.FinalUi)
        self.FinalUi.show()
 
 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = PretestWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())