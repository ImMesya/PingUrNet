from ipaddress import ip_address as ip
from os import popen
from re import findall
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QTextEdit, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox, QProgressBar, QDesktopWidget, qApp, QLabel)
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QIcon

__author__ = 'Ruslan Messian Ovcharenko'
__email__ = 'TheSuperRuslan@gmail.com'
__version__ = '1.1'


class Example (QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        print('Labels...')
        firstIP = QLabel('First IP address:')
        lastIP = QLabel('Last IP address:')
        resultLabel = QLabel('Result:')

        self.firstIPedit = QLineEdit()
        self.lastIPedit = QLineEdit()
        self.resultEdit = QTextEdit()
        self.flag_ = False

        print('Progress bar...')
        self.pbar = QProgressBar(self)

        print('Buttons...')
        quitButton = QPushButton('Quit', self)
        quitButton.clicked.connect(qApp.quit)
        quitButton.setToolTip('Close application')

        self.startButton = QPushButton('Start', self)
        self.startButton.clicked.connect(self.doAction)
        self.startButton.setShortcut('Enter')
        self.startButton.setToolTip('Start process')

        self.timer = QBasicTimer()
        self.step = 0
        self.count = 0

        print('Labels grid...')
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(firstIP, 1, 0)
        grid.addWidget(self.firstIPedit, 1, 1)

        grid.addWidget(lastIP, 2, 0)
        grid.addWidget(self.lastIPedit, 2, 1)

        grid.addWidget(resultLabel, 3, 0)
        grid.addWidget(self.resultEdit, 3, 1, 5, 1)

        print('Layouts...')
        hbox = QHBoxLayout()
        hbox.addWidget(self.startButton)
        hbox.addWidget(self.pbar)

        hbox.addWidget(quitButton)

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        print('Window...')
        self.center()
        self.resize(500, 300)
        self.setWindowTitle('Ping your network')
        self.setWindowIcon(QIcon('icon.png'))
        self.show()

        print('Done.')

    def center(self):
        # Always set window on the center of monitor
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        # Quit message if pressed 'X' button on top
        reply = QMessageBox.question(self, 'Message', "Are you sure to <b>Quit</b>?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def timerEvent(self, e):
        # Some rules for progress bar
        self.step = self.step + self.valuePBAR
        self.pbar.setValue(self.step)
        if self.step >= 100:
            self.step = 0
            self.timer.stop()
            self.startButton.setText('Finished')
            return

    def doAction(self):
        if self.timer.isActive():
            print('Operation paused...')
            self.startButton.setText('Start')
            self.newPBARvalue = 0

        else:
            self.startButton.setText('Pause')
            try:
                f_hn = ip(self.firstIPedit.text())
                l_hn = ip(self.lastIPedit.text())

                if f_hn > l_hn:
                    f_hn, l_hn = l_hn, f_hn
                if self.count >= 1 and f_hn != self.tmp1:
                    self.count = 0
                if self.count >= 1 and l_hn != self.tmp2:
                    self.temp_l_hn = l_hn
                self.valueIP = int(l_hn) - int(f_hn)
                self.tmp1 = f_hn
                self.tmp2 = l_hn

            except ValueError:
                # Message if user entered incorrect address. Will break function.
                print('IP address is incorrect. Enter again.')
                QMessageBox.warning(self, 'Warning!', 'IP address is incorrect. Enter again.', QMessageBox.Cancel | QMessageBox.NoButton, QMessageBox.Cancel)
                return

            if self.count >= 1:
                f_hn = self.temp_f_hn
                l_hn = self.temp_l_hn
                self.valuePBAR = (100 - self.step) / (self.valueIP - self.count2)
                self.step -= self.valuePBAR
                print('Operation continued...')

            if self.count == 0:
                    self.valuePBAR = 100 / (self.valueIP + 1)
                    self.resultEdit.setPlainText('')
                    self.count2 = 0
                    f_hn -= 1
                    print('Operation started...')

            self.timer.start(100, self)  # Start progress bar
            self.count += 1
            QApplication.processEvents()  # Will update QTextEdit in loop

            while f_hn != l_hn:
                if self.startButton.text() == 'Start':
                    # Remember old values if you pause the application
                    self.temp_f_hn = f_hn
                    self.temp_l_hn = l_hn
                    self.timer.stop()
                    break
                self.count2 += 1
                f_hn += 1
                self.resultEdit.append('\nping ' + str(f_hn))
                result = findall('\d+', popen('ping -n 2 -w 200 ' + str(f_hn)).read())  # Make digit list from ping result
                QApplication.processEvents()
                if len(result) > 15:
                    self.resultEdit.append(str(f_hn) + ' - in use')
                else:
                    self.resultEdit.append(str(f_hn) + ' - is free')
            else:
                self.count = 0
                self.count2 = 0
                print('Operation finished!')

if __name__ == '__main__':
    print('author: ', __author__)
    print('email: ', __email__)
    print('ver. ', __version__)
    print('Starting application...')
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
