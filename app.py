# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from SettingsWindow import Ui_SettingsWindow
import sys
import os
import translator
import google_api
import free_api

class UI(QMainWindow):

    def __init__(self):

        super(UI, self).__init__()
        uic.loadUi("MainWindow.ui", self)
        self.setWindowTitle("Программа синхронного перевода")
        self.setFixedSize(1057,806)
        self.setWindowIcon(QIcon('ico.ico'))
        
        self.startbutt = self.findChild(QPushButton, "startbutt")     
        self.clearbutt = self.findChild(QPushButton, "clearbutt")
        self.saveorigtextbutt = self.findChild(QPushButton, "saveorigtextbutt")
        self.savetranstextbutt = self.findChild(QPushButton, "savetranstextbutt")
        self.settingsbutt = self.findChild(QPushButton, "settingsbutt")
        self.saveorigsoundbutt = self.findChild(QPushButton, 'saveorigsoundbutt')
        self.savetranssoundbutt = self.findChild(QPushButton, 'savetranssoundbutt')

        self.origlangcombo = self.findChild(QComboBox, "origlangcombo")
        self.translangcombo = self.findChild(QComboBox, "translangcombo")

        self.textboxorig = self.findChild(QTextEdit, "textboxorig")
        self.textboxorig.setReadOnly(True)
        self.textboxtrans = self.findChild(QTextEdit, "textboxtrans")
        self.textboxtrans.setReadOnly(True)
        
        self.saveindicator = self.findChild(QLabel, "saveindicator")

        self.tabwidget = self.findChild(QTabWidget, "tabWidget")

        self.startbutt.clicked.connect(self.start)
        self.clearbutt.clicked.connect(self.clear)
        self.saveorigtextbutt.clicked.connect(self.saveorigtext)
        self.savetranstextbutt.clicked.connect(self.savetranstext)
        self.settingsbutt.clicked.connect(self.opensettings)
        self.saveorigsoundbutt.clicked.connect(self.saveorigaudio)
        self.savetranssoundbutt.clicked.connect(self.savetranssound)

        self.timer = QTimer()
        self.timer.timeout.connect(self.addorigtext)
        self.timer.timeout.connect(self.addtranstext)

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.updateapps)
        self.timer2.start(3000)

        self.started = False

        self.tr = translator.Translator(free_api.FreeApi())

        self.languages = self.tr.get_languages()

        self.origlangcombo.addItems(self.languages.get('languages_to_recognize').keys())
        self.translangcombo.addItems(self.languages.get('languages_to_voice').keys())
        
        self.soundinputcombo.addItems(self.tr.get_applications())

        self.origlangcombo.setCurrentText("russian")
        self.translangcombo.setCurrentText("english")
        
        self.settings_window = SettingsWindow()

        self.settings_window.ui.serviceaccbutt.clicked.connect(self.open_file)

        self.settings_window.ui.transslider.setMinimum(2)
        self.settings_window.ui.transslider.setMaximum(20)
        self.settings_window.ui.transslider.setValue(20)
        self.settings_window.ui.transslider.valueChanged[int].connect(self.changevolume)

        self.settings_window.ui.checkBox_2.setChecked(True)
        self.settings_window.ui.checkBox_2.clicked.connect(self.google_api)
        self.settings_window.ui.checkBox.clicked.connect(self.google_api)

        self.google_api = False
        self.credentials_path = None

        self.msg = QMessageBox()
        self.msg.setWindowTitle('Внимание!')
        self.msg.setText('Не выбран источник звука')
        self.msg.setStandardButtons(QMessageBox.Ok)

        self.msg_2 = QMessageBox()
        self.msg_2.setWindowTitle('Внимание!')
        self.msg_2.setText('Не добавлен service account ключ')
        self.msg_2.setStandardButtons(QMessageBox.Ok)

        self.msg_3 = QMessageBox()
        self.msg_3.setWindowTitle('Внимание!')
        self.msg_3.setText('Неправильный service account ключ')
        self.msg_3.setStandardButtons(QMessageBox.Ok)

        if os.path.exists('session_store.json'):
            self.restore_session()

        self.show()

    def start(self):
        if not self.started:
            if self.soundinputcombo.currentIndex() == -1:
                self.msg.show()
            else:
                self.tr.start(source_language=self.origlangcombo.currentText(),
                            target_language=self.translangcombo.currentText(),
                            application=self.soundinputcombo.currentText())
                self.timer.start(1000)
                self.started = True
                self.startbutt.setText('Стоп')
        else:
            self.stop()

    def stop(self):
        self.settings_window.ui.transslider.setValue(20)
        self.tr.stop()
        self.started = False
        self.startbutt.setText('Старт')

    def open_file(self):
        self.credentials_path = QFileDialog.getOpenFileName(self, "Открыть файл", "", "JSON файлы (*.json)")[0]
        self.tr.credentials_path = self.credentials_path

    def opensettings(self):
        self.settings_window.window.show()

    def changevolume(self):
        self.tr.control_volume(self.settings_window.ui.transslider.value())

    def clear(self):
        self.tr.clear()
        self.textboxorig.setText("")
        self.textboxtrans.setText("")

    def addorigtext(self):
        scroll_position = self.textboxorig.verticalScrollBar().value()
        self.textboxorig.setText(self.tr.get_original_text())
        self.textboxorig.moveCursor(QTextCursor.End)
        self.textboxorig.verticalScrollBar().setValue(scroll_position)

    def addtranstext(self):
        self.textboxtrans.setText(self.tr.get_translation())

    def updateapps(self):
        current_app = self.soundinputcombo.currentIndex()
        self.soundinputcombo.clear()
        self.soundinputcombo.addItems(self.tr.get_applications())
        try:
            self.soundinputcombo.setCurrentIndex(current_app)
        except:
            pass

    def saveorigtext(self):
        try:
            filename = QFileDialog.getSaveFileName(self.textboxorig, "Сохранить текст", filter="Text files (*.txt)")
            with open(filename[0], 'w') as f:
                textfile = self.tr.get_original_text()
                f.write(textfile)
        except FileNotFoundError:
            pass

    def savetranstext(self):
        try:
            filename = QFileDialog.getSaveFileName(self.textboxorig, "Сохранить текст", filter="Text files (*.txt)")
            with open(filename[0], 'w', encoding='utf-8') as f:
                textfile = self.tr.get_translation()
                f.write(textfile)
        except FileNotFoundError:
            pass

    def saveorigaudio(self):
        try:
            filename = QFileDialog.getSaveFileName(self, "Сохранить ориг. звук", filter="Audio Files (*.wav)")
            self.tr.get_original_audio(filename[0])
        except (FileNotFoundError, AttributeError):
            pass

    def savetranssound(self):
        try:
            filename = QFileDialog.getSaveFileName(self, "Сохранить пер. звук", filter="Audio Files (*.mp3)")
            self.tr.get_translation_audio(filename[0])
        except (FileNotFoundError, ValueError):
            pass

    def google_api(self):
        if self.google_api:
            if self.started:
                self.stop()
            self.tr = translator.Translator(free_api.FreeApi())
            self.google_api = False
            self.settings_window.ui.checkBox_2.setChecked(True)
            self.settings_window.ui.checkBox.setChecked(False)
        elif not self.google_api and (self.tr.credentials_path or self.credentials_path):
            if self.started:
                self.stop()
            try:
                if self.credentials_path:
                    self.tr.credentials_path = self.credentials_path
                self.tr = translator.Translator(google_api.GoogleApi(self.tr.credentials_path))
            except:
                self.settings_window.ui.checkBox.setChecked(False)
                self.msg_3.show()
                return
            self.google_api = True
            self.settings_window.ui.checkBox_2.setChecked(False)
            self.settings_window.ui.checkBox.setChecked(True)
        else:
            self.settings_window.ui.checkBox.setChecked(False)
            self.msg_2.show()

    def closeEvent(self, event):
        self.settings_window.window.close()
        audio_files_path = os.path.join(os.getcwd(), 'speech')
        prefix = 'speech_'
        try:
            files = os.listdir(audio_files_path)
            for file in files:
                if file.startswith(prefix):
                    audio_file_path = os.path.join(audio_files_path, file)
                    os.remove(audio_file_path)
        except FileNotFoundError:
            pass    
        if self.started:
            self.tr.stop()
        self.tr.disable_devices()
        self.tr.session_store(self.origlangcombo.currentText(), self.translangcombo.currentText(), self.settings_window.ui.checkBox.isChecked())
        event.accept()

    def restore_session(self):
        source_language, target_language, volume, credentials_path, google_checkbox = self.tr.restore_session()
        self.settings_window.ui.transslider.setValue(volume)
        self.tr.control_volume(volume)
        self.origlangcombo.setCurrentText(source_language)
        self.translangcombo.setCurrentText(target_language)
        if google_checkbox and credentials_path:
            try:
                self.tr = translator.Translator(google_api.GoogleApi(credentials_path))
            except:
                self.msg_3.show()
                self.settings_window.ui.checkBox.setChecked(False)
                self.settings_window.ui.checkBox_2.setChecked(True)
                return
            self.settings_window.ui.checkBox.setChecked(google_checkbox)
            self.settings_window.ui.checkBox_2.setChecked(False)
            self.google_api = True

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.window = QDialog()
        self.window.setWindowIcon(QIcon('ico.ico'))
        self.window.setWindowModality(Qt.ApplicationModal)

        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self.window)
    
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()