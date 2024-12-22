# Скрипт для пересборки стилистического файла после его генерации
import os

os.system(f'pyuic5 untitled.ui -o style.py')

new_code: list[str, ...] = []
with open('style.py', mode='r', encoding='UTF-8') as file:
    while True:
        if '.png' in (line := file.readline()):
            line = ''.join(list(map(lambda x: f"os.path.join(os.path.dirname(__file__), 'Picture', '{x.split('/')[1]}')"
                                    if '.png' in x else x, line.split('"'))))
        new_code.append(line)
        if line == 'from PyQt5 import QtCore, QtGui, QtWidgets\n':
            new_code.append('from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings\n')
            new_code.append('from .data.mouse import Tracker\n')
            new_code.append('import os\n')
        if line == '        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)\n':
            del new_code[-1]
            new_code.append("        self.webEngineView = QWebEngineView(self.MainWidget)\n")
            new_code.append("        self.webEngineView.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)\n")
            new_code.append("        self.gridLayout_3.addWidget(self.webEngineView, 1, 1, 1, 1)\n")
            break
    while True:
        if file.readline() == "        self.pushButton_2 = QtWidgets.QPushButton(self.widget)\n":
            new_code.append("        self.pushButton_2 = Tracker(self.widget)\n")
            new_code.append("        self.pushButton_2.interaction(self)\n")
            break
        continue
    for line in file.readlines():
        if '.png' in line:
            line = ''.join(list(map(lambda x: f"os.path.join(os.path.dirname(__file__), 'Picture', '{x.split('/')[1]}')"
                                    if '.png' in x else x, line.split('"'))))
        new_code.append(line)
with open('style.py', mode='w', encoding='UTF-8') as file:
    file.writelines(new_code)
