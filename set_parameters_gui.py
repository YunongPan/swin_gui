# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'set_parameters_gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(685, 395)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem)
        self.pushButton_select_config_file = QtWidgets.QPushButton(Dialog)
        self.pushButton_select_config_file.setMinimumSize(QtCore.QSize(40, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_select_config_file.setFont(font)
        self.pushButton_select_config_file.setObjectName("pushButton_select_config_file")
        self.horizontalLayout_10.addWidget(self.pushButton_select_config_file)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit_class_number = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_class_number.setFont(font)
        self.lineEdit_class_number.setObjectName("lineEdit_class_number")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_class_number)
        self.label_9 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.lineEdit_test_images = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_test_images.setFont(font)
        self.lineEdit_test_images.setObjectName("lineEdit_test_images")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_test_images)
        self.label_4 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_epoch_max = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_epoch_max.setFont(font)
        self.lineEdit_epoch_max.setObjectName("lineEdit_epoch_max")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_epoch_max)
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_epoch_interval = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_epoch_interval.setFont(font)
        self.lineEdit_epoch_interval.setObjectName("lineEdit_epoch_interval")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_epoch_interval)
        self.label_5 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_lr = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_lr.setFont(font)
        self.lineEdit_lr.setObjectName("lineEdit_lr")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_lr)
        self.label_6 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_samples = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_samples.setFont(font)
        self.lineEdit_samples.setObjectName("lineEdit_samples")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.lineEdit_samples)
        self.label_7 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.lineEdit_workers = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_workers.setFont(font)
        self.lineEdit_workers.setObjectName("lineEdit_workers")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.lineEdit_workers)
        self.lineEdit_class_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_class_name.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_class_name.setFont(font)
        self.lineEdit_class_name.setObjectName("lineEdit_class_name")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_class_name)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem2)
        self.pushButton_close = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout_11.addWidget(self.pushButton_close)
        self.pushButton_clear = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_clear.setFont(font)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.horizontalLayout_11.addWidget(self.pushButton_clear)
        self.pushButton_apply_parameters = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_apply_parameters.setFont(font)
        self.pushButton_apply_parameters.setObjectName("pushButton_apply_parameters")
        self.horizontalLayout_11.addWidget(self.pushButton_apply_parameters)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_select_config_file.setText(_translate("Dialog", "        Select config file        "))
        self.label_3.setText(_translate("Dialog", "Names of classes: "))
        self.label.setText(_translate("Dialog", "Number of classes: "))
        self.label_9.setText(_translate("Dialog", "Number of test images in dataset: "))
        self.label_4.setText(_translate("Dialog", "Max. number of epochs: "))
        self.label_2.setText(_translate("Dialog", "Epoch interval of checkpoint saving:  "))
        self.label_5.setText(_translate("Dialog", "Learing rate: "))
        self.label_6.setText(_translate("Dialog", "Samples per GPU: "))
        self.label_7.setText(_translate("Dialog", "Workers per GPU: "))
        self.pushButton_close.setText(_translate("Dialog", "Close"))
        self.pushButton_clear.setText(_translate("Dialog", "Clear"))
        self.pushButton_apply_parameters.setText(_translate("Dialog", "Apply"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

