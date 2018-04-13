#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import os.path
import glob
from xmlhandle import Parsexml
from xmlhandle import Parsetxt
from PyQt5.QtWidgets import QWidget, QApplication,QLabel,QGridLayout,QPushButton,QFileDialog,QMessageBox,QSlider
from PyQt5.QtGui import QPainter, QColor, QFont,QImage,QPixmap,QPen
from PyQt5.QtCore import Qt,QRect,QDir,QPoint
from PyQt5.QtCore import QObject, pyqtSignal


def getjpgname(abpath):
	try:
		basename=os.path.basename(abpath)
		return basename.split('.',2)[0]+'.jpg'
	except Exception as e:
		print (e)

def getxmlname(abpath):
	try:
		basename=os.path.basename(abpath)
		return basename.split('.',2)[0]+'.xml'
	except Exception as e:
		print (e)

def getdirname(filename):
	return os.path.dirname(filename)

class ImageLabel(QLabel):
	def __init__(self):
		super().__init__()
		self.name=''
		self.msg={}
		self.darkflag=False
		self.darkrects=[]
		self.rate=[]
		self.alarmobjects=[]
		self.output=[]
		self.tmpimage=QImage()
		self.image=QImage()
		self.orimage=QImage()
		self.startpos=QPoint(0,0)
		self.curpos=QPoint(0,0)
		self.saveflag=False
		self.compareflag=False
		self.pensize=20
		self.initUI()

	def initUI(self):
		self.show()

	def paintEvent(self, event):
		if self.image:
			qp = QPainter()
			if self.saveflag:
				qp.begin(self.orimage)
				qp.setPen(QPen(Qt.black, 3))
				qp.setBrush(Qt.black)
				for rect in self.darkrects:
					x=rect.topLeft().x()/self.rate[0]
					y=(rect.topLeft().y()-self.yoffset)/self.rate[1]
					width=rect.width()/self.rate[0]
					height=rect.height()/self.rate[1]
					qp.drawRect(x,y,width,height)
				self.orimage.save(self.name,'JPG',100)
				self.darkrects.clear()
				self.saveflag=False
				self.image=self.orimage
				qp.end()

			qp.begin(self.image)
			qp.setPen(QPen(Qt.red, 3))
			if self.alarmobjects:
				for ob in self.alarmobjects:
					xmin=int(float(ob['rect'][0]))
					ymin=int(float(ob['rect'][1]))
					xmax=int(float(ob['rect'][2]))
					ymax=int(float(ob['rect'][3]))
					arect=QRect(xmin,ymin,xmax,ymax)
					qp.drawRect(arect)
					qp.setFont(QFont('Decorative', self.pensize))
					qp.drawText(QRect(xmin,ymin-self.pensize,self.image.width(),self.image.height()), Qt.AlignLeft, ob['type'])

			if self.compareflag:
				if self.output:
					qp.setPen(QPen(Qt.green, 2))
					qp.setFont(QFont('Decorative', self.pensize))
					for n in self.output:
						qp.drawRect(n[1],n[2],n[3],n[4])
						qp.drawText(QRect(n[1],n[2]-self.pensize,self.image.width(),self.image.height()), Qt.AlignLeft, n[0])
			qp.end()

			showimage=self.image.scaled(self.width(),self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			if showimage.width():
					self.rate=[float(showimage.width())/self.image.width(),float(showimage.height())/self.image.height()]

			qp.begin(self)
			self.yoffset=(self.height()-showimage.height())/2
			qp.drawImage(0,self.yoffset, showimage);



			if self.darkflag:
				if self.darkrects:
					qp.setPen(QPen(Qt.black, 3))
					for rect in self.darkrects:
						qp.drawRect(rect)
				qp.setPen(QPen(Qt.black, 3))
				qp.drawRect(self.startpos.x(),self.startpos.y(),self.curpos.x()-self.startpos.x(),self.curpos.y()-self.startpos.y())
			qp.end()


	def mousePressEvent (self,event):
		if self.darkflag:
			self.startpos=event.pos()
			self.curpos=event.pos()

	def	mouseReleaseEvent (self, event):
		if self.darkflag:
			self.curpos=event.pos()
			self.tmprect=QRect(self.startpos.x(),self.startpos.y(),self.curpos.x()-self.startpos.x(),self.curpos.y()-self.startpos.y())
			self.darkrects.append(self.tmprect)
			self.startpos=QPoint(0,0)
			self.curpos=QPoint(0,0)

	def mouseMoveEvent(self, event):
		if self.darkflag:
			self.curpos=event.pos()
			self.update()

	def on_comparebtn(self):
		self.compareflag=not self.compareflag
		self.image=self.tmpimage.copy()
		self.repaint()

	def on_darkbtn(self):
		self.darkflag=not self.darkflag
		self.update()

	def on_revokebtn(self):
		if self.darkrects:
			self.darkrects.pop()
			self.update()

	def on_submitbtn(self):
		self.saveflag=not self.saveflag
		self.update()

	def on_setpensize(self,width):
		self.pensize=width
		self.image=self.tmpimage.copy()
		self.update()


	def loadimage(self,pix):
		try:
			self.name=pix
			self.image=QImage(pix)
			self.orimage=QImage(pix)
			self.tmpimage=QImage(pix)
			print ('--->',pix)

			self.txtname=getdirname(pix)+'/result.txt'
			self.output=Parsetxt(self.txtname).getmsg(self.name)
			print(self.output)

			self.msg=Parsexml(getdirname(pix)+'/'+getxmlname(pix))
			self.alarmobjects=self.msg['objects'][0]
			self.update()
		except Exception as e:
			print (e)



class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.index=0
		self.initUI() #界面绘制交给InitUi方法

	def initUI(self):
		self.setWindowTitle('图片预览')
		self.imagelabel=ImageLabel()
		layout = QGridLayout(self)
		layout.addWidget(self.imagelabel,0,0,8,8)

		self.setStyleSheet("QPushButton{border-style:none;padding:10px;border-radius:5px;background-color:#1ABC9C;color:#34495E;font-size:20px;}"
                                 "QPushButton:hover {color:#4E6D8C background-color:#F0F0F0;}"
                                 "QPushButton:pressed {color:#2D3E50;background:#B8C6D1;}")

		openbtn=QPushButton("open")
		openbtn.setStyleSheet("QPushButton{background-color:#E6F8F5;border:none;color:#1ABC9C;font-size:20px;}"
			"QPushButton:hover{background-color:#333333;}")
		openbtn.clicked.connect(self.on_openbtn)
		layout.addWidget(openbtn,0,8,1,1)

		opendirbtn=QPushButton("opendir")
		opendirbtn.setStyleSheet("QPushButton{background-color:#E6F8F5;border:none;color:#1ABC9C;font-size:20px;}"
			"QPushButton:hover{background-color:#333333;}")
		opendirbtn.clicked.connect(self.on_opendirbtn)
		layout.addWidget(opendirbtn,1,8,1,1)

		pribtn=QPushButton("privious")
		pribtn.setStyleSheet("QPushButton{background-color:#E6F8F5;border:none;color:#1ABC9C;font-size:20px;}"
			"QPushButton:hover{background-color:#333333;}")
		pribtn.clicked.connect(self.on_pribtn)
		layout.addWidget(pribtn,2,8,1,1)

		nextbtn=QPushButton('next')
		nextbtn.setStyleSheet("QPushButton{background-color:#E6F8F5;border:none;color:#1ABC9C;font-size:20px;}"
			"QPushButton:hover{background-color:#333333;}")
		nextbtn.clicked.connect(self.on_nextbtn)
		layout.addWidget(nextbtn,3,8,1,1)

		comparebtn=QPushButton('compare')
		comparebtn.setStyleSheet("QPushButton{background-color:#E6F8F5;border:none;color:#1ABC9C;font-size:20px;}"
			"QPushButton:hover{background-color:#333333;}")
		comparebtn.clicked.connect(self.imagelabel.on_comparebtn)
		layout.addWidget(comparebtn,4,8,1,1)

		darkbtn=QPushButton('black')
		darkbtn.setStyleSheet("QPushButton{background-color:#E6F8F5;border:none;color:#1ABC9C;font-size:20px;}"
			"QPushButton:hover{background-color:#333333;}")
		darkbtn.clicked.connect(self.imagelabel.on_darkbtn)
		layout.addWidget(darkbtn,5,8,1,1)

		revokebtn=QPushButton('revoke')
		revokebtn.setStyleSheet("QPushButton{background-color:#E6F8F5;border:none;color:#1ABC9C;font-size:20px;}"
			"QPushButton:hover{background-color:#333333;}")
		revokebtn.clicked.connect(self.imagelabel.on_revokebtn)
		layout.addWidget(revokebtn,6,8,1,1)

		submitbtn=QPushButton('submit')
		submitbtn.setStyleSheet("QPushButton{background-color:#E6F8F5;border:none;color:#1ABC9C;font-size:20px;}"
			"QPushButton:hover{background-color:#333333;}")
		submitbtn.clicked.connect(self.imagelabel.on_submitbtn)
		layout.addWidget(submitbtn,7,8,1,1)

		sizeLabel=QLabel()
		sizeLabel.setText('文字大小：')
		layout.addWidget(sizeLabel,8,0,1,1)

		sizeslider=QSlider(Qt.Horizontal,self)
		sizeslider.setMinimum(20)
		sizeslider.setMaximum(100)
		sizeslider.valueChanged.connect(self.imagelabel.on_setpensize)
		layout.addWidget(sizeslider,8,1,1,2)

		self.namelabel=QLabel()
		layout.addWidget(self.namelabel,8,4,1,5)
		self.setLayout(layout)

#自定义信号
	imagerecieved = pyqtSignal(str)

	def on_openbtn(self):
		file= QFileDialog.getOpenFileName(self,"open file dialog","./","xml files(*.xml)")
		self.path=getdirname(file[0])
		if file:
			self.imagerecieved.connect(self.imagelabel.loadimage)
			jpgname=self.path+'/'+getjpgname(file[0])
			if jpgname:
				self.namelabel.setText(jpgname)
				self.imagerecieved.emit(jpgname)
			else:
				print("jpg not exists!")
		else:
			print ("open failed!")

	def on_opendirbtn(self):
		path=QFileDialog.getExistingDirectory(self,"open file dialog","./")
		if path:
			self.path=path
			self.L= [file for file in glob.glob(self.path+'/'+'*.xml')]
			self.index=0
			file=self.L[self.index]
			self.imagerecieved.connect(self.imagelabel.loadimage)
			jpgname=self.path+'/'+getjpgname(file)
			self.namelabel.setText(jpgname)
			self.imagerecieved.emit(jpgname)
		else:
			return

	def on_pribtn(self):
		try:
			if(self.index>0):
				self.index-=1
				file=self.L[self.index]
				jpgname=self.path+'/'+getjpgname(file)
				self.namelabel.setText(jpgname)
				self.imagerecieved.emit(jpgname)
		except Exception as e:
			self.index+=1

	def on_nextbtn(self):
		try:
			self.index+=1
			file=self.L[self.index]
			jpgname=self.path+'/'+getjpgname(file)
			self.namelabel.setText(jpgname)
			self.imagerecieved.emit(jpgname)
		except Exception as e:
			self.index-=1

	def closeEvent(self,event):
		reply = QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
			self.deleteLater()
		else:
			event.ignore()




if (__name__=="__main__"):
	app=QApplication(sys.argv)
	w=MainWindow()
	w.resize(860,500)
	w.show()
	sys.exit(app.exec_())