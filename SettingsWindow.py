# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(444, 348)
        SettingsWindow.setStyleSheet("background-color: #333333;")
        self.label_2 = QtWidgets.QLabel(SettingsWindow)
        self.label_2.setGeometry(QtCore.QRect(40, 20, 361, 61))
        self.label_2.setStyleSheet("background-color: #333333;\n"
"color: #ffffff;\n"
"font-size: 20px;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.transslider = QtWidgets.QSlider(SettingsWindow)
        self.transslider.setGeometry(QtCore.QRect(30, 90, 381, 20))
        self.transslider.setStyleSheet("QSlider {\n"
"min-height: 20px;\n"
"max-height: 20px;\n"
"}\n"
"QSlider::handle:horizontal {\n"
"  background-color: #ff1100;\n"
"  border-radius: 4px;\n"
"}\n"
"QSlider::add-page:horizontal {\n"
"  border: 1px solid #ffffff;\n"
"  background-color: #737373;\n"
"}\n"
"QSlider::sub-page:horizontal {\n"
"  border: 1px solid #ffffff;\n"
"  background-color: #cc0818;\n"
"}\n"
"")
        self.transslider.setOrientation(QtCore.Qt.Horizontal)
        self.transslider.setObjectName("transslider")
        self.label_3 = QtWidgets.QLabel(SettingsWindow)
        self.label_3.setGeometry(QtCore.QRect(40, 130, 361, 41))
        self.label_3.setStyleSheet("background-color: #333333;\n"
"color: #ffffff;\n"
"font-size: 20px;")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.serviceaccbutt = QtWidgets.QPushButton(SettingsWindow)
        self.serviceaccbutt.setGeometry(QtCore.QRect(60, 190, 141, 51))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(115, 115, 115))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(115, 115, 115))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(115, 115, 115))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(115, 115, 115))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(115, 115, 115))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(115, 115, 115))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(115, 115, 115))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(115, 115, 115))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(115, 115, 115))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.serviceaccbutt.setPalette(palette)
        self.serviceaccbutt.setStyleSheet("QPushButton {\n"
"  font-family: Arial;\n"
"  font-size: 16px;  \n"
"  border-radius: 6px;\n"
"  color: rgb(255, 255, 255);\n"
"  background-color: rgb(115, 115, 115);\n"
"}\n"
"QPushButton:pressed {\n"
"background-color: #383838;\n"
"}")
        self.serviceaccbutt.setObjectName("serviceaccbutt")
        self.checkBox = QtWidgets.QCheckBox(SettingsWindow)
        self.checkBox.setGeometry(QtCore.QRect(230, 200, 31, 41))
        self.checkBox.setStyleSheet("QCheckBox::indicator {\n"
"    width: 25px;\n"
"    height: 25px;\n"
"    background-color: rgb(115, 115, 115);\n"
"    border-radius: 6px;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-color: #333333;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background-color: lime;\n"
"}")
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.label_4 = QtWidgets.QLabel(SettingsWindow)
        self.label_4.setGeometry(QtCore.QRect(270, 190, 131, 61))
        self.label_4.setStyleSheet("background-color: #333333;\n"
"color: #ffffff;\n"
"font-size: 16px;")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.checkBox_2 = QtWidgets.QCheckBox(SettingsWindow)
        self.checkBox_2.setGeometry(QtCore.QRect(230, 260, 31, 41))
        self.checkBox_2.setStyleSheet("QCheckBox::indicator {\n"
"    width: 25px;\n"
"    height: 25px;\n"
"    background-color: rgb(115, 115, 115);\n"
"    border-radius: 6px;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-color: #333333;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background-color: lime;\n"
"}")
        self.checkBox_2.setText("")
        self.checkBox_2.setObjectName("checkBox_2")
        self.label_5 = QtWidgets.QLabel(SettingsWindow)
        self.label_5.setGeometry(QtCore.QRect(270, 250, 131, 61))
        self.label_5.setStyleSheet("background-color: #333333;\n"
"color: #ffffff;\n"
"font-size: 16px;")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Настройки"))
        self.label_2.setText(_translate("SettingsWindow", "Громкость синхронного перевода"))
        self.label_3.setText(_translate("SettingsWindow", "Сервис аккаунт Google"))
        self.serviceaccbutt.setText(_translate("SettingsWindow", "Загрузить ключ"))
        self.label_4.setText(_translate("SettingsWindow", "Google API"))
        self.label_5.setText(_translate("SettingsWindow", "Бесплатный API"))