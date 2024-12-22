import sys
import os, time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QIcon,QFont
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsPixmapItem
from PyQt5.QtCore import Qt  # Import Qt for alignment
from .interactive.myUtils import CustomGraphicsView
from .layouts import ui_Timing      
from .utilities.devThread import Command
import numpy as np
class Expt(QtWidgets.QWidget, ui_Timing.Ui_Form):
    def __init__(self, device, **kwargs):
        super().__init__()
        self.setupUi(self)
        time.sleep(0.2)
        self.last_counts = 0
        self.start_time = time.time()

        self.scope_thread = None
        if 'scope_thread' in kwargs:
            self.scope_thread = kwargs['scope_thread']
            self.scope_thread.add_command(Command('set_sqr1',{'frequency':1000,'duty_cycle':0.5}))
            self.scope_thread.counts_ready.connect(self.updateTiming)

        self.showMessage = kwargs.get('showMessage',print)

        if 'set_status_function' in kwargs:
            self.set_status_function(kwargs['set_status_function'])


        image_widget = QtWidgets.QWidget()  # Placeholder for the image        

        self.scene = QGraphicsScene(self)
        self.view = CustomGraphicsView(self.scene)
        self.view.setFrameShape(QtWidgets.QFrame.NoFrame)  # Remove the frame border

        imagepath = os.path.join(os.path.dirname(__file__),'interactive/timings.jpeg')
        mypxmp = QPixmap(imagepath)
        myimg = QGraphicsPixmapItem(mypxmp)
        myimg.setTransformationMode(Qt.SmoothTransformation)
        self.scene.addItem(myimg)

        self.imageLayout.addWidget(self.view)

    def makeMeasurement(self):
        i1 = self.IN1Box.currentIndex()
        i2 = self.IN2Box.currentIndex()
        if i1 ==0 or i2 == 0:
            self.showMessage("Please select inputs/actions",3000)
            return

        print(i1,i2)

    def set_status_function(self,func):
        self.showMessage = func

    def fetch_counts(self):
        if not self.running: return
        self.scope_thread.add_command(Command('get_counts',{}))

    def updateTiming(self,interval):
        self.showMessage(f"Counts: {interval}")
        self.datapoints += 1


    def set_sqr1(self):
        f = self.sqr1_freq.value()
        self.scope_thread.add_command(Command('set_sqr1',{'frequency':f,'duty_cycle':0.5}))
        self.SQ1Box.blockSignals(True)
        if f == 0:
            self.sqr1_label.setText('SQR1 Frequency : ALWAYS ON')
            self.SQ1Box.setChecked(True)
        else:
            self.sqr1_label.setText(f'SQR1 Frequency ( 0 = ALWAYS ON) : {f} Hz')
            self.SQ1Box.setChecked(False)
        self.SQ1Box.blockSignals(False)
