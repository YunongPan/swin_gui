import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, QEventLoop, QTimer
from PyQt5.QtGui import QPixmap, QImage, QDoubleValidator, QIntValidator


import gui
from gui import *

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)

        self.ui = gui.Ui_MainWindow()

        self.ui.setupUi(self)
        flag = QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint
        self.setWindowFlags(flag)
        self.setWindowState(QtCore.Qt.WindowMinimized)
        self.setWindowTitle('SWIN - GUI')
        self.pretrainedModel = str()
        self.trainingConfig = str()
        self.imageFile = str()
        self.imageModel = str()
        self.imageConfig = str()
        self.videoFile = str()
        self.videoModel = str()
        self.videoConfig = str()
        self.videoSaveName = 'result'

        self.ui.pushButton_image_test.setEnabled(False)
        self.ui.pushButton_train.setEnabled(False)
        self.ui.pushButton_video_test.setEnabled(False)


        # Training
        self.t = TrainingThread()
        self.ui.pushButton_select_model_pretrained.clicked.connect(self.choosePretrainedModel)
        self.ui.pushButton_select_config.clicked.connect(self.chooseTrainingConfig)
        self.ui.pushButton_train.clicked.connect(self.triggerTraining)
        #
        # Image Test
        self.e = EvaluationThread()
        self.ui.pushButton_select_model_image.clicked.connect(self.chooseImageModel)
        self.ui.pushButton_select_image.clicked.connect(self.chooseImageFile)
        self.ui.pushButton_select_config_image.clicked.connect(self.chooseImageConfig)
        self.ui.pushButton_image_test.clicked.connect(self.triggerImageTest)
        #
        # Video Test
        self.d = DisplayThread()
#        self.d.signalForText.connect(self.updateTextBrowser)
#        sys.stdout = self.d
        self.ui.pushButton_select_model_video.clicked.connect(self.chooseVideoModel)
        self.ui.pushButton_select_video.clicked.connect(self.chooseVideoFile)
        self.ui.pushButton_select_config_video.clicked.connect(self.chooseVideoConfig)
        self.ui.lineEdit_video_save_name.editingFinished.connect(self.updateSaveName)
        self.ui.pushButton_video_test.clicked.connect(self.triggerVideoTest)


        # self.ui.lineEdit_video_save_name.editingFinished.connect(self.updateTrainConfig)
        #
        #
        # Clear
        self.ui.pushButton_reset.clicked.connect(self.resetWindow)
        # self.ui.pushButton_clear_terminal.clicked.connect(self.clearTerminal)
        self.ui.pushButton_stop.clicked.connect(self.terminateThread)
        # self.clearWindow()

    def choosePretrainedModel(self, FilePath): ########################################################################
        model = QtWidgets.QFileDialog.getOpenFileName(self, "Select your pretrained model", "./weights")[0]
        if model == '':
            self.ui.pushButton_select_model_pretrained.setText('Select model')
            self.ui.pushButton_train.setEnabled(False)
            return

        pos = model.find('swin_gui')
        model = model[pos + 9:]
        pos = len(model)
        for ch in model[::-1]:
            if ch == '/':
                break
            pos = pos - 1

        post = str()
        for ch in model[::-1]:
            if ch == '.':
                break
            post += ch

        if post != 'htp':
            self.ui.display.setText('Selected file is not valid model file (.pth)!')
            self.ui.pushButton_train.setEnabled(False)
            return

        self.ui.pushButton_select_model_pretrained.setText(model[pos:])
        self.pretrainedModel = model
        if self.pretrainedModel != '' and self.trainingConfig != '':
            self.ui.pushButton_train.setEnabled(True)


    def chooseTrainingConfig(self, FilePath):########################################################################
        config = QtWidgets.QFileDialog.getOpenFileName(self,  "Select your config", "./py")[0]
        if config == '':
            self.ui.pushButton_select_config.setText('Select config')
            self.ui.pushButton_train.setEnabled(False)
            return
        pos = config.find('swin_gui')
        config = config[pos + 9:]

        pos = len(config)
        for ch in config[::-1]:
            if ch == '/':
                break
            pos = pos - 1

        post = str()
        for ch in config[::-1]:
            if ch == '.':
                break
            post += ch

        if post != 'yp':
            self.ui.display.setText('Selected file is not a valid config (.py)!')
            self.ui.pushButton_train.setEnabled(False)
            return
        self.ui.pushButton_select_config.setText(config[pos:])
        self.trainingConfig = config
        if self.pretrainedModel != '' and self.trainingConfig != '':
            self.ui.pushButton_train.setEnabled(True)

    def triggerTraining(self): ########################################################################
        pretrainedModel = self.pretrainedModel
        trainingConfig = self.trainingConfig

        self.t = TrainingThread(pretrainedModel, trainingConfig)
        self.t.start()



    def chooseImageModel(self, FilePath): ########################################################################
        model = QtWidgets.QFileDialog.getOpenFileName(self, "Select your model", "./weights")[0]
        if model == '':
            self.ui.pushButton_select_model_image.setText('Select model')
            self.ui.pushButton_image_test.setEnabled(False)
            return

        pos = model.find('swin_gui')
        model = model[pos + 9:]
        pos = len(model)
        for ch in model[::-1]:
            if ch == '/':
                break
            pos = pos - 1

        post = str()
        for ch in model[::-1]:
            if ch == '.':
                break
            post += ch

        if post != 'htp':
            self.ui.display.setText('Selected file is not valid model file (.pth)!')
            self.ui.pushButton_image_test.setEnabled(False)
            return

        self.ui.pushButton_select_model_image.setText(model[pos:])
        self.imageModel = model
        if self.imageModel != '' and self.imageFile != '' and self.imageConfig != '':
            self.ui.pushButton_image_test.setEnabled(True)

    def chooseImageFile(self, FilePath): ########################################################################
        image = QtWidgets.QFileDialog.getOpenFileName(self,  "Select your image", "./img")[0]
        if image == '':
            self.ui.pushButton_select_image.setText('Select image')
            self.ui.pushButton_image_test.setEnabled(False)
            return
        pos = image.find('swin_gui')
        image = image[pos + 9:]

        pos = len(image)
        for ch in image[::-1]:
            if ch == '/':
                break
            pos = pos - 1

        post = str()
        for ch in image[::-1]:
            if ch == '.':
                break
            post += ch

        if post != 'gpj' and post != 'gnp':
            self.ui.display.setText('Selected file is not a valid image (.jpg or .png)!')
            self.ui.pushButton_image_test.setEnabled(False)
            return
        self.ui.pushButton_select_image.setText(image[pos:])
        self.imageFile = image
        if self.imageModel != '' and self.imageFile != '' and self.imageConfig != '':
            self.ui.pushButton_image_test.setEnabled(True)

    def chooseImageConfig(self, FilePath):########################################################################
        config = QtWidgets.QFileDialog.getOpenFileName(self,  "Select your config", "./py")[0]
        if config == '':
            self.ui.pushButton_select_config_image.setText('Select config')
            self.ui.pushButton_image_test.setEnabled(False)
            return
        pos = config.find('swin_gui')
        config = config[pos + 9:]

        pos = len(config)
        for ch in config[::-1]:
            if ch == '/':
                break
            pos = pos - 1

        post = str()
        for ch in config[::-1]:
            if ch == '.':
                break
            post += ch

        if post != 'yp':
            self.ui.display.setText('Selected file is not a valid config (.py)!')
            self.ui.pushButton_image_test.setEnabled(False)
            return
        self.ui.pushButton_select_config_image.setText(config[pos:])
        self.imageConfig = config
        if self.imageModel != '' and self.imageFile != '' and self.imageConfig != '':
            self.ui.pushButton_image_test.setEnabled(True)


    def triggerImageTest(self): ########################################################################
        imageFile = self.imageFile
        imageModel = self.imageModel
        imageConfig = self.imageConfig

        self.e = EvaluationThread(imageFile, imageModel, imageConfig)
        self.e.start()



    def chooseVideoModel(self, FilePath): ########################################################################
        model = QtWidgets.QFileDialog.getOpenFileName(self, "Select your model", "./weights")[0]
        if model == '':
            self.ui.pushButton_select_model_video.setText('Select model')
            self.ui.pushButton_video_test.setEnabled(False)
            return

        pos = model.find('swin_gui')
        model = model[pos + 9:]
        pos = len(model)
        for ch in model[::-1]:
            if ch == '/':
                break
            pos = pos - 1

        post = str()
        for ch in model[::-1]:
            if ch == '.':
                break
            post += ch

        if post != 'htp':
            self.ui.display.setText('Selected file is not valid model file (.pth)!')
            self.ui.pushButton_video_test.setEnabled(False)
            return

        self.ui.pushButton_select_model_video.setText(model[pos:])
        self.videoModel = model
        if self.videoModel != '' and self.videoFile != '' and self.videoConfig != '':
            self.ui.pushButton_video_test.setEnabled(True)

    def chooseVideoFile(self, FilePath): ########################################################################
        video = QtWidgets.QFileDialog.getOpenFileName(self,  "Select your video", "./video")[0]
        if video == '':
            self.ui.pushButton_select_video.setText('Select video')
            self.ui.pushButton_video_test.setEnabled(False)
            return
        pos = video.find('swin_gui')
        video = video[pos + 9:]

        pos = len(video)
        for ch in video[::-1]:
            if ch == '/':
                break
            pos = pos - 1

        post = str()
        for ch in video[::-1]:
            if ch == '.':
                break
            post += ch

        if post != '4pm':
            self.ui.display.setText('Selected file is not a valid video (.mp4)!')
            self.ui.pushButton_video_test.setEnabled(False)
            return
        self.ui.pushButton_select_video.setText(video[pos:])
        self.videoFile = video
        if self.videoModel != '' and self.videoFile != '' and self.videoConfig != '':
            self.ui.pushButton_video_test.setEnabled(True)

    def chooseVideoConfig(self, FilePath):########################################################################
        config = QtWidgets.QFileDialog.getOpenFileName(self,  "Select your config", "./py")[0]
        if config == '':
            self.ui.pushButton_select_config_video.setText('Select config')
            self.ui.pushButton_video_test.setEnabled(False)
            return
        pos = config.find('swin_gui')
        config = config[pos + 9:]

        pos = len(config)
        for ch in config[::-1]:
            if ch == '/':
                break
            pos = pos - 1

        post = str()
        for ch in config[::-1]:
            if ch == '.':
                break
            post += ch

        if post != 'yp':
            self.ui.display.setText('Selected file is not a valid config (.py)!')
            self.ui.pushButton_video_test.setEnabled(False)
            return
        self.ui.pushButton_select_config_video.setText(config[pos:])
        self.videoConfig = config
        if self.videoModel != '' and self.videoFile != '' and self.videoConfig != '':
            self.ui.pushButton_video_test.setEnabled(True)

    def updateSaveName(self): ##############################################################
        self.videoSaveName = self.ui.lineEdit_video_save_name.text()

    def triggerVideoTest(self): ########################################################################
        videoFile = self.videoFile
        videoModel = self.videoModel
        videoConfig = self.videoConfig
        videoSaveName = self.videoSaveName
        if self.videoSaveName == '':
            self.ui.display.setText('Please enter the name of the file to be saved!')
        else:
            self.d = DisplayThread(videoFile, videoModel, videoConfig, videoSaveName)
            self.d.start()

            # loop = QEventLoop()
            # QTimer.singleShot(2000, loop.quit)

    def terminateThread(self):
        if self.pretrainedModel != '' and self.trainingConfig != '':
            self.t.kill()
        if self.imageModel != '' and self.imageFile != '' and self.imageConfig != '':
            self.e.kill()
        if self.videoModel != '' and self.videoFile != '' and self.videoConfig != '':
            self.d.kill()
        self.clearWindow()

    def resetWindow(self):
        # self.ui.textBrowser_terminal.clear()
        self.clearWindow()

    def clearWindow(self):
        self.ui.display.clear()
        self.pretrainedModel = str()
        self.trainingConfig = str()
        self.imageFile = str()
        self.imageModel = str()
        self.imageConfig = str()
        self.videoFile = str()
        self.videoModel = str()
        self.videoConfig = str()
        self.ui.pushButton_select_model_pretrained.setText('Select pretrained model')
        self.ui.pushButton_select_config.setText('Select config')
        self.ui.pushButton_select_image.setText('Select image')
        self.ui.pushButton_select_model_image.setText('Select model')
        self.ui.pushButton_select_config_image.setText('Select config')
        self.ui.pushButton_select_video.setText('Select video')
        self.ui.pushButton_select_model_video.setText('Select model')
        self.ui.pushButton_select_config_video.setText('Select config')
        self.ui.pushButton_image_test.setEnabled(False)
        self.ui.pushButton_video_test.setEnabled(False)
        self.ui.lineEdit_video_save_name.setText('result')
        self.videoSaveName = 'result'

    # def updateTextBrowser(self, text):########################################################################
    #     cursor = self.ui.textBrowser.textCursor()
    #     cursor.movePosition(QtGui.QTextCursor.End)
    #     cursor.insertText(text)
    #     self.ui.textBrowser.setTextCursor(cursor)
    #     self.ui.textBrowser.ensureCursorVisible()


class TrainingThread(QThread):
    signalForText = pyqtSignal(str)

    def __init__(self, pretrainedModel=None, trainingConfig=None, parent=None):
        super(TrainingThread, self).__init__(parent)
        self.pretrainedModel = pretrainedModel
        self.trainingConfig = trainingConfig

    # def write(self, text):
    #     self.signalForText.emit(str(text))

    def run(self):
        os.system("python tools/train.py " + self.trainingConfig + " --cfg-options model.pretrained=" + self.pretrainedModel)

    def kill(self):
        os.system("pkill -f \"" + self.trainingConfig + " --cfg-options model.pretrained=" + self.pretrainedModel + "\"")

class DisplayThread(QThread):
    signalForText = pyqtSignal(str)

    def __init__(self, videoFile=None, videoModel=None, videoConfig=None, videoSaveName=None, parent=None):
        super(DisplayThread, self).__init__(parent)
        self.videoFile = videoFile
        self.videoModel = videoModel
        self.videoConfig = videoConfig
        self.videoSaveName = videoSaveName

    # def write(self, text):
    #     self.signalForText.emit(str(text))

    def run(self):
        os.system("python demo/video_demo.py " + self.videoFile + " " + self.videoConfig + " " + self.videoModel + " --out " + self.videoSaveName + ".mp4")

    def kill(self):
        os.system("pkill -f \"" + self.videoFile + " " + self.videoConfig + " " + self.videoModel + " --out " + self.videoSaveName + ".mp4" + "\"")


class EvaluationThread(QThread):
    signalForText = pyqtSignal(str)

    def __init__(self, imageFile=None, imageModel=None, imageConfig=None, parent=None):
        super(EvaluationThread, self).__init__(parent)
        self.imageFile = imageFile
        self.imageModel = imageModel
        self.imageConfig = imageConfig

    # def write(self, text):
    #     self.signalForText.emit(str(text))

    def run(self):
        os.system("python demo/image_demo.py " + self.imageFile + " " + self.imageConfig + " " + self.imageModel)

    def kill(self):
        os.system("pkill -f \"" + self.imageFile + " " + self.imageConfig + " " + self.imageModel + "\"")



if __name__ == '__main__':
    myapp = QtWidgets.QApplication(sys.argv)
    myMainWindow = MainWindow()

    myMainWindow.show()
    sys.exit(myapp.exec_())