#Powered By feelded.t.me#

import os
import sys
import re
import time
import json
import winreg
import atexit
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QCheckBox, QLineEdit, QListWidget, QListWidgetItem, QLabel, QSpinBox, QAbstractSpinBox, QGroupBox, QGridLayout, QVBoxLayout

#Version and Build
VERSION = 'v1.0'
BUILD = 'Windows(x64)'

#Get file path
def GetPath(pathex):
    if hasattr(sys, '_MEIPASS'):
        return str(os.path.join(sys._MEIPASS, pathex)).replace('\\', '/')
    return str(os.path.join(os.path.abspath("."), pathex)).replace('\\', '/')

#Set Proxy
def SetProxy(proxy_host, proxy_port):
    try:
        internet_settings_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings', 0, winreg.KEY_WRITE)
        winreg.SetValueEx(internet_settings_key, 'ProxyEnable', 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(internet_settings_key, 'ProxyServer', 0, winreg.REG_SZ, f'socks={proxy_host}:{proxy_port}')
        winreg.CloseKey(internet_settings_key)
        print("SOCKS5 proxy set successfully.")
    except Exception as e:
        print(f"Error setting SOCKS5 proxy: {e}")

#Unset Proxy
def UnsetProxy():
    try:
        internet_settings_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings', 0, winreg.KEY_WRITE)
        winreg.SetValueEx(internet_settings_key, 'ProxyEnable', 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(internet_settings_key)
        print("SOCKS5 proxy unset successfully.")
    except Exception as e:
        print(f"Error unsetting SOCKS5 proxy: {e}")


#Shut the proxy on exit
def OnExit(): UnsetProxy(); os.system('taskkill /F /IM VoxCore.exe'); return print('Bye:)')


#VPN CLASS
class VPNApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        atexit.register(OnExit)

    def initUI(self):
        print('VOX LOGS - FREEDOM')
        self.setWindowTitle('Vox VPN')

        layout = QVBoxLayout()

        self.setFixedWidth(500)
        self.setFixedHeight(400)

        icon = QIcon(GetPath('media/vpn.png'))
        self.setWindowIcon(icon)
        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.setPalette(palette)

        self.worker_thread = QThread()

        self.connect_button = QPushButton('Connect', self)
        self.connect_button.clicked.connect(self.connect_clicked)
        self.connect_button.setStyleSheet("QPushButton:pressed {background-color: rgb(30, 30, 30);border: 2px solid white;}QPushButton {background-color: #111;border-radius: 8px;color: white;height: 30%;} QPushButton:disabled {color: #4caf50;background-color: rgb(30, 30, 30)}")
        layout.addWidget(self.connect_button)

        self.disconnect_button = QPushButton('Disconnect', self)
        self.disconnect_button.clicked.connect(self.disconnect_clicked)
        self.disconnect_button.setStyleSheet("QPushButton:pressed {background-color: rgb(30, 30, 30);border: 2px solid white;}QPushButton {background-color: #111;border-radius: 8px;color: white;height: 30%;} QPushButton:disabled {color: #f44336;background-color: rgb(30, 30, 30)}")
        layout.addWidget(self.disconnect_button)

        self.cfon_checkbox = QCheckBox('CFON Mode', self)
        self.cfon_checkbox.setStyleSheet("QCheckBox {color: white;text-align: center;}QCheckBox::indicator {width: 20px;height: 20px;}QCheckBox::indicator:checked {image: url({CHECK});}QCheckBox::indicator:unchecked {image: url({REMOVE});}".replace('{REMOVE}', GetPath('media/remove.png')).replace('{CHECK}', GetPath('media/check.png')))
        self.cfon_checkbox.setChecked(True)
        layout.addWidget(self.cfon_checkbox, alignment=Qt.AlignCenter)
        self.cfon_checkbox.stateChanged.connect(self.cfon_state)

        self.scan_checkbox = QCheckBox('SCAN Mode', self)
        self.scan_checkbox.setStyleSheet("QCheckBox {color: white;text-align: center;}QCheckBox::indicator {width: 20px;height: 20px;}QCheckBox::indicator:checked {image: url({CHECK});}QCheckBox::indicator:unchecked {image: url({REMOVE});}".replace('{REMOVE}', GetPath('media/remove.png')).replace('{CHECK}', GetPath('media/check.png')))
        layout.addWidget(self.scan_checkbox, alignment=Qt.AlignCenter)

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
        self.textbox_grid.setContentsMargins(0,0,0,0)
        self.textbox_grid.addWidget(self.warpkey_textbox, 0, 0)
        self.textbox_grid.addWidget(self.port_textbox, 0, 1)
        grouper.setLayout(self.textbox_grid)
        layout.addWidget(grouper)

        self.country_list = QListWidget(self)
        self.country_list.setStyleSheet("QListWidget {border: 4px solid #111;color: white;background-color: #111;border-radius: 8px;}QListWidget:focus {outline: none;}QListWidget::item:hover {background-color: #474747;color: black;border-radius: 8px;}QListView::item:selected {border-radius: 8px;background-color:#474747;color: black;}QScrollBar:vertical {background: #111;border-radius: 8px;}QScrollBar::handle:vertical {background: #474747;border-radius: 8px;}QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {background: #111;}QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: none;border: none;}")
        self.populate_country_list()
        layout.addWidget(self.country_list)
        self.country_list.setCurrentRow(0)

        self.made_by = QLabel("2024 | feelded.t.me | test-1.1", self)
        self.made_by.setStyleSheet("QLabel {color: white;}")
        layout.addWidget(self.made_by, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.show()
    

    #Check cfon box
    def cfon_state(self, state):
        if state == 0: self.country_list.hide()
        else: self.country_list.show()
    
    #Countries
    def populate_country_list(self):
        countries = ["Automatic", "Austria (AT)", "Belgium (BE)", "Bulgaria (BG)", "Brazil (BR)", "Canada (CA)", "Switzerland (CH)", "Czech Republic (CZ)", "Germany (DE)", "Denmark (DK)", "Estonia (EE)", "Spain (ES)", "Finland (FI)", "France (FR)", "United Kingdom (GB)", "Hungary (HU)", "Ireland (IE)", "India (IN)", "Italy (IT)", "Japan (JP)", "Latvia (LV)", "Netherlands (NL)", "Norway (NO)", "Poland (PL)", "Romania (RO)", "Serbia (RS)", "Sweden (SE)", "Singapore (SG)", "Slovakia (SK)", "Ukraine (UA)", "United States (US)"]
        for country in countries:
            item = QListWidgetItem(country)
            self.country_list.addItem(item)
    
    #Connect Button
    def connect_clicked(self):
        cmd = GetPath('tool\\VoxCore.exe')+f' -b 127.0.0.1:{self.port_textbox.value()}'
        if self.warpkey_textbox.text() != "": cmd += f' -k "{self.warpkey_textbox.text()}"'
        else: cmd += ' -k "notset"'
        if self.scan_checkbox.isChecked(): cmd += ' -scan'
        if self.cfon_checkbox.isChecked(): cmd += ' -cfon'
        if self.country_list.isVisible() == True and self.country_list.selectedItems() and self.country_list.selectedItems()[0].text() != 'Automatic': cmd += f" -country {re.search(r'\((\w+)\)', self.country_list.selectedItems()[0].text()).group(1)}"
        self.disconnect_button.setEnabled(True)
        self.connect_button.setEnabled(False)
        self.worker_thread.run = lambda: os.system(cmd)
        self.worker_thread.start()
        SetProxy('127.0.0.1', self.port_textbox.value())
    
    #Disconnect button
    def disconnect_clicked(self):
        self.disconnect_button.setEnabled(False)
        self.connect_button.setEnabled(True)
        UnsetProxy()
        os.system('taskkill /F /IM VoxCore.exe')

#Run
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VPNApp()
    sys.exit(app.exec_())
