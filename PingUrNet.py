from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QTextEdit, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox, QProgressBar, QDesktopWidget, qApp, QLabel)
from PyQt5.QtCore import (QBasicTimer, QRegExp)
from PyQt5.QtGui import (QIcon, QRegExpValidator)
from os import system
from ipaddress import ip_address as ip

__author__ = 'Ruslan Messian Ovcharenko'
__email__ = 'TheSuperRuslan@gmail.com'
__version__ = '1.2'


class PingUrNet(QWidget):
	def __init__(self):
		super(PingUrNet, self).__init__()

		self.initUI()
		self.center()

		self.step = 0
		self.count = 0
		self.flag_ = False

		self.resize(500, 300)
		self.setWindowTitle('PingUrNet')
		self.setWindowIcon(QIcon('icon.ico'))
		self.show()

	def initUI(self):
		firstIP = QLabel('First IP address:')
		lastIP = QLabel('Last IP address:')
		resultLabel = QLabel('Result:')

		ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
		ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
		ipValidator = QRegExpValidator(ipRegex, self)

		self.firstIPedit = QLineEdit()
		self.firstIPedit.setPlaceholderText('Example: 192.168.0.1')
		self.firstIPedit.setValidator(ipValidator)
		self.lastIPedit = QLineEdit()
		self.lastIPedit.setPlaceholderText('Example: 192.168.0.25')
		self.lastIPedit.setValidator(ipValidator)

		self.resultEdit = QTextEdit()

		self.pbar = QProgressBar(self)

		quitButton = QPushButton('Quit')
		quitButton.clicked.connect(qApp.quit)
		quitButton.setToolTip('Close application')

		self.startButton = QPushButton('Start')
		self.startButton.clicked.connect(self.doAction)
		self.startButton.setToolTip('Start process')

		self.timer = QBasicTimer()

		grid = QGridLayout()
		grid.setSpacing(10)

		grid.addWidget(firstIP, 1, 0)
		grid.addWidget(self.firstIPedit, 1, 1)
		grid.addWidget(lastIP, 2, 0)
		grid.addWidget(self.lastIPedit, 2, 1)
		grid.addWidget(resultLabel, 3, 0)
		grid.addWidget(self.resultEdit, 3, 1, 5, 1)

		hbox = QHBoxLayout()
		hbox.addWidget(self.startButton)
		hbox.addWidget(self.pbar)
		hbox.addWidget(quitButton)

		vbox = QVBoxLayout()
		vbox.addLayout(grid)
		vbox.addLayout(hbox)

		self.setLayout(vbox)

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
				QMessageBox.warning(self, 'Warning!', 'IP address is incorrect. Enter again.', QMessageBox.Cancel | QMessageBox.NoButton, QMessageBox.Cancel)
				self.startButton.setText('Start')
				return

			if self.count >= 1:
				f_hn = self.temp_f_hn
				l_hn = self.temp_l_hn
				self.valuePBAR = (100 - self.step) / (self.valueIP - self.count2)
				self.step -= self.valuePBAR

			if self.count == 0:
					self.valuePBAR = 100 / (self.valueIP + 1)
					self.resultEdit.setPlainText('')
					self.count2 = 0
					f_hn -= 1

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
				self.resultEdit.append('\nping {}'.format(f_hn))
				if sys.platform == 'win32':
					result = system('ping -n 2 -w 200 {}'.format(f_hn))
				else:
					result = system('ping -c 2 -W 2 {}'.format(f_hn))
				QApplication.processEvents()

				if result == 0:
					self.resultEdit.append('{} - in use'.format(f_hn))
				else:
					self.resultEdit.append('{} - is free'.format(f_hn))
			else:
				self.count = 0
				self.count2 = 0

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	ex = PingUrNet()
	sys.exit(app.exec_())
