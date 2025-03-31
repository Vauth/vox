# ---------------------------- #
# --- github.com/Vauth/vox --- #
# ---------------------------- #


import os
import re
import sys
import ctypes
import winreg
import atexit
import platform
import subprocess
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPalette, QColor, QTextCursor
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QCheckBox, QLineEdit, QListWidget, QListWidgetItem, QLabel, QSpinBox, QAbstractSpinBox, QGroupBox, QGridLayout, QHBoxLayout, QTextEdit, QSplitter)


# System Configs
class Config(object):
    VERSION_NUMBER = 'v1.2'
    DRAFT = 'false'  # Lowercase [true, false]
    PRE_RELEASE = 'false'  # Lowercase [true, false]
    OS = 'Windows-x64'
    COPYRIGHT = 2025
    CREDIT = 'github.com/vauth'


# Get file path
def GetPath(pathex):
    if hasattr(sys, '_MEIPASS'):
        return str(os.path.join(sys._MEIPASS, pathex)).replace('\\', '/')
    return str(os.path.join(os.path.abspath("."), pathex)).replace('\\', '/')


# Set Proxy
def SetProxy(proxy_host, proxy_port):
    try:
        if 'Windows-10' in platform.platform(): final_proxy = f'socks={proxy_host}:{proxy_port}'  # Windows-10 proxy structure
        else: final_proxy = f'{proxy_host}:{proxy_port}'
        internet_settings_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings', 0, winreg.KEY_WRITE)
        winreg.SetValueEx(internet_settings_key, 'ProxyEnable', 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(internet_settings_key, 'ProxyServer', 0, winreg.REG_SZ,final_proxy)  # final_proxy referencing to L33-34
        winreg.CloseKey(internet_settings_key)
        print("SOCKS5 proxy set successfully.")
    except Exception as e:
        print(f"Error setting SOCKS5 proxy: {e}")


# Unset Proxy
def UnsetProxy():
    try:
        internet_settings_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Internet Settings', 0, winreg.KEY_WRITE)
        winreg.SetValueEx(internet_settings_key, 'ProxyEnable', 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(internet_settings_key)
        print("SOCKS5 proxy unset successfully.")
    except Exception as e:
        print(f"Error unsetting SOCKS5 proxy: {e}")


# Shut the proxy on exit
def OnExit():
    UnsetProxy()
    os.system('taskkill /F /IM VoxCore.exe')
    return print('Bye:)')


# Custom QTextEdit that captures stdout
class ConsoleOutput(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setReadOnly(True)
        self.setStyleSheet("QTextEdit {background-color: #111;color: #ffffff;border-radius: 8px;font-family: Consolas, monospace;padding: 8px;selection-background-color: #474747;}QScrollBar:vertical {background: #111;border-radius: 8px;}QScrollBar::handle:vertical {background: #474747;border-radius: 8px;}QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {background: #111;}QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: none;border: none;}")


# Worker thread for VoxCore
class VoxWorker(QThread):
    new_log = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
        for line in iter(process.stdout.readline, ''): self.new_log.emit(line.strip())
        process.stdout.close()
        process.wait()


# VPN main class
class VPNApp(QWidget):
    def __init__(self):
        super().__init__()
        self.dark_titlebar()
        self.initUI()
        atexit.register(OnExit)
        self.worker_thread = None

    def dark_titlebar(self):
        try:
            hwnd = self.winId().__int__()
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            DWMWA_CAPTION_COLOR = 35
            if hasattr(ctypes, 'windll'):
                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(ctypes.c_int(1)),ctypes.sizeof(ctypes.c_int(1)))
                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_CAPTION_COLOR, ctypes.byref(ctypes.c_int(0x000000)), ctypes.sizeof(ctypes.c_int(1)))
        except Exception as e:
            print(f"Dark title bar not supported: {e}")

    def initUI(self):
        print('VOX LOGS - FREEDOM')
        self.setWindowTitle('Vox VPN')

        self.splitter = QSplitter(Qt.Horizontal)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        self.setFixedWidth(800)
        self.setFixedHeight(500)

        icon = QIcon(GetPath('media/vpn.png'))
        self.setWindowIcon(icon)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.setPalette(palette)

        self.connect_button = QPushButton('Connect', self)
        self.connect_button.clicked.connect(self.connect_clicked)
        self.connect_button.setStyleSheet("QPushButton:pressed {background-color: rgb(30, 30, 30);border: 2px solid white;}QPushButton {background-color: #111;border-radius: 8px;color: white;height: 30%;} QPushButton:disabled {color: #4caf50;background-color: rgb(30, 30, 30)}")
        left_layout.addWidget(self.connect_button)

        self.disconnect_button = QPushButton('Disconnect', self)
        self.disconnect_button.clicked.connect(self.disconnect_clicked)
        self.disconnect_button.setStyleSheet("QPushButton:pressed {background-color: rgb(30, 30, 30);border: 2px solid white;}QPushButton {background-color: #111;border-radius: 8px;color: white;height: 30%;} QPushButton:disabled {color: #f44336;background-color: rgb(30, 30, 30)}")
        left_layout.addWidget(self.disconnect_button)

        self.cfon_checkbox = QCheckBox('CFON Mode', self)
        self.cfon_checkbox.setStyleSheet("QCheckBox {color: white;text-align: center;}QCheckBox::indicator {width: 20px;height: 20px;}QCheckBox::indicator:checked {image: url({CHECK});}QCheckBox::indicator:unchecked {image: url({REMOVE});}".replace('{REMOVE}', GetPath('media/remove.png')).replace('{CHECK}', GetPath('media/check.png')))
        self.cfon_checkbox.setChecked(True)
        left_layout.addWidget(self.cfon_checkbox, alignment=Qt.AlignCenter)
        self.cfon_checkbox.stateChanged.connect(self.cfon_state)

        self.scan_checkbox = QCheckBox('SCAN Mode', self)
        self.scan_checkbox.setStyleSheet("QCheckBox {color: white;text-align: center;}QCheckBox::indicator {width: 20px;height: 20px;}QCheckBox::indicator:checked {image: url({CHECK});}QCheckBox::indicator:unchecked {image: url({REMOVE});}".replace('{REMOVE}', GetPath('media/remove.png')).replace('{CHECK}', GetPath('media/check.png')))
        left_layout.addWidget(self.scan_checkbox, alignment=Qt.AlignCenter)

        self.port_textbox = QSpinBox(self)
        self.port_textbox.setAlignment(Qt.AlignCenter)
        self.port_textbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.port_textbox.setRange(1024, 65535)
        self.port_textbox.setValue(8086)
        self.port_textbox.setStyleSheet("QSpinBox {border-radius: 8px;width: 1px;background-color: #111;border-radius: 8px;height: 30%;selection-background-color: #474747;color: white;}QSpinBox:focus {border: 2px solid white;}")
        self.port_textbox.setFixedWidth(80)

        self.warpkey_textbox = QLineEdit(self)
        self.warpkey_textbox.setPlaceholderText('Insert WARP+ Key')
        self.warpkey_textbox.setAlignment(Qt.AlignCenter)
        self.warpkey_textbox.setStyleSheet("QLineEdit {background-color: #111;border-radius: 8px;height: 30%;selection-background-color: #474747;color: white;}QLineEdit:focus {border: 2px solid white;}")

        grouper = QGroupBox("Grid TextBox")
        grouper.setStyleSheet("QGroupBox { border: 0px; }")
        self.textbox_grid = QGridLayout()
        self.textbox_grid.setSpacing(8)
        self.textbox_grid.setContentsMargins(0, 0, 0, 0)
        self.textbox_grid.addWidget(self.warpkey_textbox, 0, 0)
        self.textbox_grid.addWidget(self.port_textbox, 0, 1)
        grouper.setLayout(self.textbox_grid)
        left_layout.addWidget(grouper)

        self.country_list = QListWidget(self)
        self.country_list.setStyleSheet("QListWidget {border: 4px solid #111;color: white;background-color: #111;border-radius: 8px;}QListWidget:focus {outline: none;}QListWidget::item:hover {background-color: #474747;color: black;border-radius: 8px;}QListView::item:selected {border-radius: 8px;background-color:#474747;color: black;}QScrollBar:vertical {background: #111;border-radius: 8px;}QScrollBar::handle:vertical {background: #474747;border-radius: 8px;}QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {background: #111;}QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: none;border: none;}")
        self.populate_country_list()
        left_layout.addWidget(self.country_list)
        self.country_list.setCurrentRow(0)

        self.made_by = QLabel(f"{Config.COPYRIGHT} | {Config.CREDIT} | {Config.VERSION_NUMBER}", self)
        self.made_by.setStyleSheet("QLabel {color: white;}")
        left_layout.addWidget(self.made_by, alignment=Qt.AlignCenter)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.console_output = ConsoleOutput()
        right_layout.addWidget(self.console_output)

        clear_logs_button = QPushButton('Clear Logs')
        clear_logs_button.setStyleSheet("QPushButton:pressed {background-color: rgb(30, 30, 30);border: 2px solid white;}QPushButton {background-color: #111;border-radius: 8px;color: white;height: 30%;}QScrollBar:vertical {background: #111;border-radius: 8px;}QScrollBar::handle:vertical {background: #474747;border-radius: 8px;}QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {background: #111;}QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: none;border: none;}")
        clear_logs_button.clicked.connect(self.clear_logs)
        right_layout.addWidget(clear_logs_button)

        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        self.splitter.setSizes([350, 450])

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.splitter)
        self.setLayout(main_layout)

        sys.stdout = self
        self.show()

    # Write method to capture stdout
    def write(self, text):
        self.console_output.moveCursor(QTextCursor.End)
        self.console_output.insertPlainText(text)
        self.console_output.moveCursor(QTextCursor.End)

    # Clear logs
    def clear_logs(self):
        self.console_output.clear()

    # Check cfon box
    def cfon_state(self, state):
        if state == 0: self.country_list.hide()
        else: self.country_list.show()

    # Countries
    def populate_country_list(self):
        countries = ["Automatic", "Austria (AT)", "Belgium (BE)", "Bulgaria (BG)", "Brazil (BR)", "Canada (CA)", "Switzerland (CH)", "Czech Republic (CZ)", "Germany (DE)", "Denmark (DK)", "Estonia (EE)", "Spain (ES)", "Finland (FI)", "France (FR)", "United Kingdom (GB)", "Hungary (HU)", "Ireland (IE)", "India (IN)", "Italy (IT)", "Japan (JP)", "Latvia (LV)", "Netherlands (NL)", "Norway (NO)", "Poland (PL)", "Romania (RO)", "Serbia (RS)", "Sweden (SE)", "Singapore (SG)", "Slovakia (SK)", "Ukraine (UA)", "United States (US)"]
        for country in countries:
            item = QListWidgetItem(country)
            self.country_list.addItem(item)

    # Connect Button
    def connect_clicked(self):
        cmd = GetPath('tool\\VoxCore.exe') + f' -b 127.0.0.1:{self.port_textbox.value()}'
        if self.warpkey_textbox.text() != "":  cmd += f' -k "{self.warpkey_textbox.text()}"'
        else: cmd += ' -k "notset"'
        if self.scan_checkbox.isChecked(): cmd += ' -scan'
        if self.cfon_checkbox.isChecked(): cmd += ' -cfon'
        if self.country_list.isVisible() == True and self.country_list.selectedItems() and self.country_list.selectedItems()[0].text() != 'Automatic': cmd += f" -country {re.search(r'\((\w+)\)', self.country_list.selectedItems()[0].text()).group(1)}"
        self.disconnect_button.setEnabled(True)
        self.connect_button.setEnabled(False)
        self.worker_thread = VoxWorker(cmd)
        self.worker_thread.new_log.connect(self.handle_new_log)
        self.worker_thread.start()
        SetProxy('127.0.0.1', self.port_textbox.value())

    # Write new logs
    def handle_new_log(self, log_text):
        self.write(log_text + '\n')

    # Disconnect button
    def disconnect_clicked(self):
        self.disconnect_button.setEnabled(False)
        self.connect_button.setEnabled(True)
        UnsetProxy()
        os.system('taskkill /F /IM VoxCore.exe')
        if self.worker_thread:
            self.worker_thread.terminate()
            self.worker_thread = None


# Run
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VPNApp()
    sys.exit(app.exec_())
