import os
import sys
import time
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import QThread, pyqtSignal, QEventLoop, QTimer, QProcess
from PyQt5.QtGui import QPixmap, QImage, QDoubleValidator, QIntValidator

import gui
import set_parameters_gui
import param_confirm
from gui import *
from set_parameters_gui import *

class ConfirmWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = param_confirm.Ui_Dialog()
        self.ui.setupUi(self)
        flag = QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowCloseButtonHint
        self.setWindowFlags(flag)
        self.setWindowState(QtCore.Qt.WindowMinimized)
        self.setWindowTitle('Dialog')
        self.ui.pushButton_ok.clicked.connect(self.close)


class ParameterWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = set_parameters_gui.Ui_Dialog()
        self.ui.setupUi(self)
        flag = QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowCloseButtonHint
        self.setWindowFlags(flag)
        self.setWindowState(QtCore.Qt.WindowMinimized)

        self.setWindowTitle('Set Parameters')

        self.className = str()
        self.classNumber = str()
        self.testNumber = str()
        self.epochMax = str()
        self.epochInterval = str()
        self.learningRate = str()
        self.gpuSample = str()
        self.gpuWorker = str()

        self.parameterConfig = str()
        self.maskRcnnSwinFpn = 'configs/_base_/models/mask_rcnn_swin_fpn.py'
        self.defaultRuntime = 'configs/_base_/default_runtime.py'
        self.cocoInstance = 'configs/_base_/datasets/coco_instance.py'
        self.coco = 'mmdet/datasets/coco.py'

        self.ui.pushButton_apply_parameters.setEnabled(False)

        self.ui.lineEdit_class_name.editingFinished.connect(self.updateClassName)
        self.ui.lineEdit_class_number.editingFinished.connect(self.updateClassNumber)
        self.ui.lineEdit_test_images.editingFinished.connect(self.updateTestNumber)
        self.ui.lineEdit_epoch_max.editingFinished.connect(self.updateEpochMax)
        self.ui.lineEdit_epoch_interval.editingFinished.connect(self.updateEpochInterval)
        self.ui.lineEdit_lr.editingFinished.connect(self.updateLearningRate)
        self.ui.lineEdit_samples.editingFinished.connect(self.updateGpuSample)
        self.ui.lineEdit_workers.editingFinished.connect(self.updateGpuWorker)

        self.ui.pushButton_select_config_file.clicked.connect(self.chooseParameterConfig)
        self.ui.pushButton_clear.clicked.connect(self.clearWindow)
        self.ui.pushButton_apply_parameters.clicked.connect(self.applyParameters)
        self.ui.pushButton_close.clicked.connect(self.close)



    def chooseParameterConfig(self, FilePath):########################################################################
        config = QtWidgets.QFileDialog.getOpenFileName(self,  "Select your config", "./py")[0]
        if config == '':
            self.clearWindow()
            self.ui.pushButton_select_config_file.setText('        Select config file        ')
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
            self.clearWindow()
            self.ui.pushButton_select_config_file.setText('Selected file is not a valid config (.py)!')
            return

        configFile = open(config, 'r')
        readConfigFile = configFile.read()
        configFile.close()
        lr_index_start = readConfigFile.find(', lr=') + 5
        if lr_index_start == 4:
            self.clearWindow()
            self.ui.pushButton_select_config_file.setText('Selected file is not a valid config!')
            return
        else:
            self.ui.pushButton_select_config_file.setText(config[pos:])
            self.parameterConfig = config

        max_epoch_start = readConfigFile.find('max_epochs=') + 11
        if max_epoch_start == 10:
            self.clearWindow()
            self.ui.pushButton_select_config_file.setText('Selected file is not a valid config!')
            return
        else:
            self.ui.pushButton_select_config_file.setText(config[pos:])
            self.parameterConfig = config


        if self.parameterConfig != '':
            self.checkParameters()





    def checkParameters(self):

        # Read Parameters from Config File
        configFile = open(self.parameterConfig, 'r')
        readConfigFile = configFile.read()
        configFile.close()

        lr_index_start = readConfigFile.find(', lr=') + 5
        lr_index_end = readConfigFile.find(',', lr_index_start)
        self.learningRate = readConfigFile[lr_index_start:lr_index_end]
        self.ui.lineEdit_lr.setText(self.learningRate)

        max_epoch_start = readConfigFile.find('max_epochs=') + 11
        max_epoch_end = readConfigFile.find(')', max_epoch_start)
        self.epochMax = readConfigFile[max_epoch_start:max_epoch_end]
        self.ui.lineEdit_epoch_max.setText(self.epochMax)

        # Read Parameters from mask_rcnn_swin_fpn.py
        maskRcnnFile = open(self.maskRcnnSwinFpn, 'r')
        readMaskRcnnFile = maskRcnnFile.read()
        maskRcnnFile.close()

        num_classes_1_start = readMaskRcnnFile.find('num_classes=') + 12
        num_classes_1_end = readMaskRcnnFile.find(',', num_classes_1_start)
        self.classNumber = readMaskRcnnFile[num_classes_1_start:num_classes_1_end]
        self.ui.lineEdit_class_number.setText(self.classNumber)

        # Read Parameters from default_runtime.py
        defaultRuntimeFile = open(self.defaultRuntime, 'r')
        readDefaultRuntimeFile = defaultRuntimeFile.read()
        defaultRuntimeFile.close()

        epoch_interval_start = readDefaultRuntimeFile.find('checkpoint_config = dict(interval=') + 34
        epoch_interval_end = readDefaultRuntimeFile.find(')', epoch_interval_start)
        self.epochInterval = readDefaultRuntimeFile[epoch_interval_start:epoch_interval_end]
        self.ui.lineEdit_epoch_interval.setText(self.epochInterval)

        test_image_number_start = readDefaultRuntimeFile.find('interval=', epoch_interval_end) + 9
        test_image_number_end = readDefaultRuntimeFile.find(',', test_image_number_start)
        self.testNumber = readDefaultRuntimeFile[test_image_number_start:test_image_number_end]
        self.ui.lineEdit_test_images.setText(self.testNumber)


        # Read Parameters from coco_instance.py
        cocoInstanceFile = open(self.cocoInstance, 'r')
        readCocoInstanceFile = cocoInstanceFile.read()
        cocoInstanceFile.close()

        samples_per_gpu_start = readCocoInstanceFile.find('samples_per_gpu=') + 16
        samples_per_gpu_end = readCocoInstanceFile.find(',', samples_per_gpu_start)
        self.gpuSample = readCocoInstanceFile[samples_per_gpu_start:samples_per_gpu_end]
        self.ui.lineEdit_samples.setText(self.gpuSample)

        workers_per_gpu_start = readCocoInstanceFile.find('workers_per_gpu=') + 16
        workers_per_gpu_end = readCocoInstanceFile.find(',', workers_per_gpu_start)
        self.gpuWorker = readCocoInstanceFile[workers_per_gpu_start:workers_per_gpu_end]
        self.ui.lineEdit_workers.setText(self.gpuWorker)

        # Read Parameters from coco.py
        cocoFile = open(self.coco, 'r')
        readCocoFile = cocoFile.read()
        cocoFile.close()

        name_classes_start = readCocoFile.find('CLASSES = ') + 10
        name_classes_end = readCocoFile.find('## check mark ##', name_classes_start)
        self.className = readCocoFile[name_classes_start:name_classes_end]
        self.ui.lineEdit_class_name.setText(self.className)
        if self.className != '' and self.classNumber != '' and self.testNumber != '' and self.epochMax != '' and self.epochInterval != '' and self.learningRate != '' and self.gpuSample != '' and self.gpuWorker != '' and self.parameterConfig != '':
            self.ui.pushButton_apply_parameters.setEnabled(True)


    def updateClassName(self): ##############################################################
        self.className = self.ui.lineEdit_class_name.text()
        if self.className != '' and self.classNumber != '' and self.testNumber != '' and self.epochMax != '' and self.epochInterval != '' and self.learningRate != '' and self.gpuSample != '' and self.gpuWorker != '' and self.parameterConfig != '':
            self.ui.pushButton_apply_parameters.setEnabled(True)
        else:
            self.ui.pushButton_apply_parameters.setEnabled(False)

    def updateClassNumber(self): ##############################################################
        self.classNumber = self.ui.lineEdit_class_number.text()
        if self.className != '' and self.classNumber != '' and self.testNumber != '' and self.epochMax != '' and self.epochInterval != '' and self.learningRate != '' and self.gpuSample != '' and self.gpuWorker != '' and self.parameterConfig != '':
            self.ui.pushButton_apply_parameters.setEnabled(True)
        else:
            self.ui.pushButton_apply_parameters.setEnabled(False)

    def updateTestNumber(self): ##############################################################
        self.testNumber = self.ui.lineEdit_test_images.text()
        if self.className != '' and self.classNumber != '' and self.testNumber != '' and self.epochMax != '' and self.epochInterval != '' and self.learningRate != '' and self.gpuSample != '' and self.gpuWorker != '' and self.parameterConfig != '':
            self.ui.pushButton_apply_parameters.setEnabled(True)
        else:
            self.ui.pushButton_apply_parameters.setEnabled(False)

    def updateEpochMax(self): ##############################################################
        self.epochMax = self.ui.lineEdit_epoch_max.text()
        if self.className != '' and self.classNumber != '' and self.testNumber != '' and self.epochMax != '' and self.epochInterval != '' and self.learningRate != '' and self.gpuSample != '' and self.gpuWorker != '' and self.parameterConfig != '':
            self.ui.pushButton_apply_parameters.setEnabled(True)
        else:
            self.ui.pushButton_apply_parameters.setEnabled(False)

    def updateEpochInterval(self): ##############################################################
        self.epochInterval = self.ui.lineEdit_epoch_interval.text()
        if self.className != '' and self.classNumber != '' and self.testNumber != '' and self.epochMax != '' and self.epochInterval != '' and self.learningRate != '' and self.gpuSample != '' and self.gpuWorker != '' and self.parameterConfig != '':
            self.ui.pushButton_apply_parameters.setEnabled(True)
        else:
            self.ui.pushButton_apply_parameters.setEnabled(False)

    def updateLearningRate(self): ##############################################################
        self.learningRate = self.ui.lineEdit_lr.text()
        if self.className != '' and self.classNumber != '' and self.testNumber != '' and self.epochMax != '' and self.epochInterval != '' and self.learningRate != '' and self.gpuSample != '' and self.gpuWorker != '' and self.parameterConfig != '':
            self.ui.pushButton_apply_parameters.setEnabled(True)
        else:
            self.ui.pushButton_apply_parameters.setEnabled(False)

    def updateGpuSample(self): ##############################################################
        self.gpuSample = self.ui.lineEdit_samples.text()
        if self.className != '' and self.classNumber != '' and self.testNumber != '' and self.epochMax != '' and self.epochInterval != '' and self.learningRate != '' and self.gpuSample != '' and self.gpuWorker != '' and self.parameterConfig != '':
            self.ui.pushButton_apply_parameters.setEnabled(True)
        else:
            self.ui.pushButton_apply_parameters.setEnabled(False)

    def updateGpuWorker(self): ##############################################################
        self.gpuWorker = self.ui.lineEdit_workers.text()
        if self.className != '' and self.classNumber != '' and self.testNumber != '' and self.epochMax != '' and self.epochInterval != '' and self.learningRate != '' and self.gpuSample != '' and self.gpuWorker != '' and self.parameterConfig != '':
            self.ui.pushButton_apply_parameters.setEnabled(True)
        else:
            self.ui.pushButton_apply_parameters.setEnabled(False)



    def applyParameters(self): ##############################################################
        className = self.className
        classNumber = self.classNumber
        testNumber = self.testNumber
        epochMax = self.epochMax
        epochInterval = self.epochInterval
        learningRate = self.learningRate
        gpuSample = self.gpuSample
        gpuWorker = self.gpuWorker


        # Rewrite config file
        configFile = open(self.parameterConfig, 'r+')
        readConfigFile = configFile.read()

        lr_index_start = readConfigFile.find(', lr=') + 5
        lr_index_end = readConfigFile.find(',', lr_index_start)
        readConfigFile_new1 = readConfigFile.replace(', lr=' + readConfigFile[lr_index_start:lr_index_end], ', lr=' + learningRate)

        max_epoch_start = readConfigFile_new1.find('max_epochs=') + 11
        max_epoch_end = readConfigFile_new1.find(')', max_epoch_start)
        readConfigFile_new2 = readConfigFile_new1.replace('max_epochs=' + readConfigFile_new1[max_epoch_start:max_epoch_end], 'max_epochs=' + epochMax)

        configFile.seek(0)
        configFile.truncate()
        configFile.write(readConfigFile_new2)
        configFile.close()

        # Rewrite mask_rcnn_swin_fpn.py
        maskRcnnFile = open(self.maskRcnnSwinFpn, 'r+')
        readMaskRcnnFile = maskRcnnFile.read()

        num_classes_1_start = readMaskRcnnFile.find('num_classes=') + 12
        num_classes_1_end = readMaskRcnnFile.find(',', num_classes_1_start)
        readMaskRcnnFile_new1 = readMaskRcnnFile.replace('num_classes=' + readMaskRcnnFile[num_classes_1_start:num_classes_1_end], 'num_classes=' + classNumber)

        num_classes_2_start = readMaskRcnnFile_new1.find('num_classes=', num_classes_1_end) + 12
        num_classes_2_end = readMaskRcnnFile_new1.find(',', num_classes_2_start)
        readMaskRcnnFile_new2 = readMaskRcnnFile_new1.replace('num_classes=' + readMaskRcnnFile_new1[num_classes_2_start:num_classes_2_end], 'num_classes=' + classNumber)

        maskRcnnFile.seek(0)
        maskRcnnFile.truncate()
        maskRcnnFile.write(readMaskRcnnFile_new2)
        maskRcnnFile.close()


        # Rewrite default_runtime.py
        defaultRuntimeFile= open(self.defaultRuntime, 'r+')
        readDefaultRuntimeFile = defaultRuntimeFile.read()

        epoch_interval_start = readDefaultRuntimeFile.find('checkpoint_config = dict(interval=') + 34
        epoch_interval_end = readDefaultRuntimeFile.find(')', epoch_interval_start)
        readDefaultRuntimeFile_new1 = readDefaultRuntimeFile.replace('checkpoint_config = dict(interval=' + readDefaultRuntimeFile[epoch_interval_start:epoch_interval_end], 'checkpoint_config = dict(interval=' + epochInterval)

        test_image_number_start = readDefaultRuntimeFile_new1.find('interval=', epoch_interval_end) + 9
        test_image_number_end = readDefaultRuntimeFile_new1.find(',', test_image_number_start)
        readDefaultRuntimeFile_new2 = readDefaultRuntimeFile_new1.replace('interval=' + readDefaultRuntimeFile_new1[test_image_number_start:test_image_number_end], 'interval=' + testNumber)

        defaultRuntimeFile.seek(0)
        defaultRuntimeFile.truncate()
        defaultRuntimeFile.write(readDefaultRuntimeFile_new2)
        defaultRuntimeFile.close()

        # Rewrite coco_instance.py
        cocoInstanceFile = open(self.cocoInstance, 'r+')
        readCocoInstanceFile = cocoInstanceFile.read()

        samples_per_gpu_start = readCocoInstanceFile.find('samples_per_gpu=') + 16
        samples_per_gpu_end = readCocoInstanceFile.find(',', samples_per_gpu_start)
        readCocoInstanceFile_new1 = readCocoInstanceFile.replace('samples_per_gpu=' + readCocoInstanceFile[samples_per_gpu_start:samples_per_gpu_end], 'samples_per_gpu=' + gpuSample)

        workers_per_gpu_start = readCocoInstanceFile_new1.find('workers_per_gpu=') + 16
        workers_per_gpu_end = readCocoInstanceFile_new1.find(',', workers_per_gpu_start)
        readCocoInstanceFile_new2 = readCocoInstanceFile_new1.replace('workers_per_gpu=' + readCocoInstanceFile_new1[workers_per_gpu_start:workers_per_gpu_end], 'workers_per_gpu=' + gpuWorker)

        cocoInstanceFile.seek(0)
        cocoInstanceFile.truncate()
        cocoInstanceFile.write(readCocoInstanceFile_new2)
        cocoInstanceFile.close()


        # Rewrite coco.py
        cocoFile = open(self.coco, 'r+')
        readCocoFile = cocoFile.read()

        name_classes_start = readCocoFile.find('CLASSES = ') + 10
        name_classes_end = readCocoFile.find('## check mark ##', name_classes_start)
        readCocoFile_new = readCocoFile.replace('CLASSES = ' + readCocoFile[name_classes_start:name_classes_end], 'CLASSES = ' + className)

        cocoFile.seek(0)
        cocoFile.truncate()
        cocoFile.write(readCocoFile_new)
        cocoFile.close()

        # Close subwindow
        self.showConfirmWindow()

    def showConfirmWindow(self):
        myConfirmWindow = ConfirmWindow()
        myConfirmWindow.exec()


    def clearWindow(self):
        self.ui.pushButton_select_config_file.setText('        Select config file        ')
        self.ui.lineEdit_class_name.setText('')
        self.ui.lineEdit_class_number.setText('')
        self.ui.lineEdit_test_images.setText('')
        self.ui.lineEdit_epoch_max.setText('')
        self.ui.lineEdit_epoch_interval.setText('')
        self.ui.lineEdit_lr.setText('')
        self.ui.lineEdit_samples.setText('')
        self.ui.lineEdit_workers.setText('')
        self.className = str()
        self.classNumber = str()
        self.testNumber = str()
        self.epochMax = str()
        self.epochInterval = str()
        self.learningRate = str()
        self.gpuSample = str()
        self.gpuWorker = str()
        self.parameterConfig = str()
        self.ui.pushButton_apply_parameters.setEnabled(False)

#############################################################################################################################################
#############################################################################################################################################

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

        self.outString = "Out:"
        self.errString = "Err:"
        self.process = QProcess()
        self.setup_ui()


        self.ui.pushButton_image_test.setEnabled(False)
        self.ui.pushButton_train.setEnabled(False)
        self.ui.pushButton_video_test.setEnabled(False)

        # Set Parameters Subwindow
        self.ui.pushButton_set_parameters.clicked.connect(self.showParameterWindow)

        # Training
        # self.t = TrainingThread()
        self.ui.pushButton_select_model_pretrained.clicked.connect(self.choosePretrainedModel)
        self.ui.pushButton_select_config.clicked.connect(self.chooseTrainingConfig)
        self.ui.pushButton_train.clicked.connect(self.triggerTraining)

        #
        # Image Test
        # self.e = EvaluationThread()
        self.ui.pushButton_select_model_image.clicked.connect(self.chooseImageModel)
        self.ui.pushButton_select_image.clicked.connect(self.chooseImageFile)
        self.ui.pushButton_select_config_image.clicked.connect(self.chooseImageConfig)
        self.ui.pushButton_image_test.clicked.connect(self.triggerImageTest)
        #
        # Video Test
        # self.d = DisplayThread()
        self.ui.pushButton_select_model_video.clicked.connect(self.chooseVideoModel)
        self.ui.pushButton_select_video.clicked.connect(self.chooseVideoFile)
        self.ui.pushButton_select_config_video.clicked.connect(self.chooseVideoConfig)
        self.ui.lineEdit_video_save_name.editingFinished.connect(self.updateSaveName)
        self.ui.pushButton_video_test.clicked.connect(self.triggerVideoTest)


        # Clear
        self.ui.pushButton_reset.clicked.connect(self.resetWindow)
        self.ui.pushButton_clear_terminal.clicked.connect(self.clearTerminal)
        self.ui.pushButton_stop.clicked.connect(self.terminateThread)
        # self.clearWindow()

    #######################################################################################################
    def setup_ui(self):
        self.process.readyReadStandardOutput.connect(self.update_stdout)
        self.process.readyReadStandardError.connect(self.update_stderr)


    def updateTextBrowser(self, text):
        cursor = self.ui.textBrowser_terminal.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.textBrowser_terminal.setTextCursor(cursor)
        self.ui.textBrowser_terminal.ensureCursorVisible()

    def update_stdout(self):
        data = self.process.readAllStandardOutput().data()
        # self.outString += " " + data.decode("utf-8").rstrip()
        self.outString = data.decode("utf-8").rstrip()
        self.ui.textBrowser_terminal.append(self.outString)

    def update_stderr(self):
        data = self.process.readAllStandardError().data()
        self.errString = data.decode("utf-8").rstrip()
        self.ui.textBrowser_terminal.append(self.errString)
        # self.ui.textBrowser_terminal.setText(self.errString)

    #######################################################################################################

    def showParameterWindow(self):
        myParameterWindow = ParameterWindow()
        myParameterWindow.exec()


    def choosePretrainedModel(self, FilePath): ########################################################################
        model = QtWidgets.QFileDialog.getOpenFileName(self, "Select your pretrained model", "./weights")[0]
        if model == '':
            self.ui.pushButton_select_model_pretrained.setText('Select pretrained model')
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
        # pretrainedModel = self.pretrainedModel
        # trainingConfig = self.trainingConfig

        cmd = "tools/train.py " + self.trainingConfig + " --cfg-options model.pretrained=" + self.pretrainedModel

        self.process.start("python", cmd.split())
        # self.process.start("python", "program.py".split())



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
        if os.path.exists("image_test_result.jpg"):
            os.remove("image_test_result.jpg")
        cmd = "demo/image_demo.py " + self.imageFile + " " + self.imageConfig + " " + self.imageModel
        self.process.start("python", cmd.split())
        timer = 0
        while timer < 200:
            if os.path.exists("image_test_result.jpg"):
                pixmap = QtGui.QPixmap("image_test_result.jpg")
                width = self.ui.display.frameGeometry().width()
                height = self.ui.display.frameGeometry().height()
                pixmap4 = pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio)

                self.ui.display.setPixmap(pixmap4)
                # self.ui.display.setScaledContents(True)
                break
            timer += 1
            time.sleep(0.1)


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
        if self.videoSaveName == '':
            self.ui.display.setText('Please enter the name of the file to be saved!')
        else:
            cmd = "demo/video_demo.py " + self.videoFile + " " + self.videoConfig + " " + self.videoModel + " --out " + self.videoSaveName + ".mp4"
            self.process.start("python", cmd.split())




    def clearTerminal(self):
        self.ui.textBrowser_terminal.clear()



    def terminateThread(self):
        if self.pretrainedModel != '' and self.trainingConfig != '':
            os.system("pkill -f \"" + self.trainingConfig + " --cfg-options model.pretrained=" + self.pretrainedModel + "\"")
        if self.imageModel != '' and self.imageFile != '' and self.imageConfig != '':
            os.system("pkill -f \"" + self.imageFile + " " + self.imageConfig + " " + self.imageModel + "\"")
        if self.videoModel != '' and self.videoFile != '' and self.videoConfig != '':
            os.system("pkill -f \"" + self.videoFile + " " + self.videoConfig + " " + self.videoModel + " --out " + self.videoSaveName + ".mp4" + "\"")


    def resetWindow(self):
        self.terminateThread()
        self.clearTerminal()
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


# class TrainingThread(QThread):
#     signalForText = pyqtSignal(str)
#
#     def __init__(self, pretrainedModel=None, trainingConfig=None, parent=None):
#         super(TrainingThread, self).__init__(parent)
#         self.pretrainedModel = pretrainedModel
#         self.trainingConfig = trainingConfig
#         self.process = QProcess()
#
#
#     def run(self):
#         cmd = "tools/train.py" + self.trainingConfig + " --cfg-options model.pretrained=" + self.pretrainedModel
#         self.process.start("python", cmd.split())
#         # os.system("python tools/train.py " + self.trainingConfig + " --cfg-options model.pretrained=" + self.pretrainedModel)
#
#     def kill(self):
#         os.system("pkill -f \"" + self.trainingConfig + " --cfg-options model.pretrained=" + self.pretrainedModel + "\"")
#
# class DisplayThread(QThread):
#     signalForText = pyqtSignal(str)
#
#     def __init__(self, videoFile=None, videoModel=None, videoConfig=None, videoSaveName=None, parent=None):
#         super(DisplayThread, self).__init__(parent)
#         self.videoFile = videoFile
#         self.videoModel = videoModel
#         self.videoConfig = videoConfig
#         self.videoSaveName = videoSaveName
#
#     def run(self):
#         os.system("python demo/video_demo.py " + self.videoFile + " " + self.videoConfig + " " + self.videoModel + " --out " + self.videoSaveName + ".mp4")
#
#     def kill(self):
#         os.system("pkill -f \"" + self.videoFile + " " + self.videoConfig + " " + self.videoModel + " --out " + self.videoSaveName + ".mp4" + "\"")
#
#
# class EvaluationThread(QThread):
#     signalForText = pyqtSignal(str)
#
#     def __init__(self, imageFile=None, imageModel=None, imageConfig=None, parent=None):
#         super(EvaluationThread, self).__init__(parent)
#         self.imageFile = imageFile
#         self.imageModel = imageModel
#         self.imageConfig = imageConfig
#
#     def run(self):
#         os.system("python demo/image_demo.py " + self.imageFile + " " + self.imageConfig + " " + self.imageModel)
#
#     def kill(self):
#         os.system("pkill -f \"" + self.imageFile + " " + self.imageConfig + " " + self.imageModel + "\"")



if __name__ == '__main__':
    myapp = QtWidgets.QApplication(sys.argv)

    myMainWindow = MainWindow()
    myParameterWindow = ParameterWindow

    myMainWindow.show()

    sys.exit(myapp.exec_())